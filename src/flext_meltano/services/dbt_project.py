"""DBT Project Management — MRO mixin for FlextMeltano facade.

Manifest parsing and model/test discovery.
Converted from standalone FlextMeltanoDbtProjectManager to facade mixin.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_meltano import FlextMeltanoServiceBase, c, m, p, r, t, u


class FlextMeltanoDbtProjectMixin(FlextMeltanoServiceBase):
    """DBT project management mixin for MRO composition on FlextMeltano.

    Manages DBT project manifests and model/test discovery.
    """

    _dbt_project_root: Path | None = u.PrivateAttr(default_factory=lambda: None)
    _dbt_manifest: t.Meltano.DbtManifestData | None = u.PrivateAttr(
        default_factory=lambda: None,
    )

    def fetch_dbt_models(self) -> p.Result[t.SequenceOf[t.Meltano.OptionalScalarMap]]:
        """Get all models from manifest."""
        try:
            model_nodes_result = self._get_dbt_manifest_nodes(
                c.Meltano.DbtResourceType.MODEL,
            )
            if model_nodes_result.failure:
                return r[t.SequenceOf[t.Meltano.OptionalScalarMap]].fail(
                    model_nodes_result.error or "Unknown error",
                )
            models: t.SequenceOf[t.Meltano.OptionalScalarMap] = [
                {
                    "name": str(node.name),
                    "path": str(node.path),
                    "description": node.description
                    if node.description is not None
                    else "",
                    "fqn": node.fqn_string,
                }
                for node in model_nodes_result.value
            ]
            self.logger.info("Models retrieved", count=len(models))
            return r[t.SequenceOf[t.Meltano.OptionalScalarMap]].ok(models)
        except c.Meltano.OPERATION_ERRORS as e:
            self.logger.exception("Failed to get models", error=str(e))
            return r[t.SequenceOf[t.Meltano.OptionalScalarMap]].fail(
                f"Failed to get models: {e}",
            )

    def fetch_dbt_tests(self) -> p.Result[t.SequenceOf[t.AttributeMapping]]:
        """Get all tests from manifest."""
        try:
            test_nodes_result = self._get_dbt_manifest_nodes(
                c.Meltano.DbtResourceType.TEST,
            )
            if test_nodes_result.failure:
                return r[t.SequenceOf[t.AttributeMapping]].fail(
                    test_nodes_result.error or "Unknown error",
                )
            tests: t.SequenceOf[t.AttributeMapping] = [
                {
                    "name": str(node.name),
                    "path": str(node.path),
                    "description": node.description
                    if node.description is not None
                    else "",
                    "fqn": node.fqn_string,
                }
                for node in test_nodes_result.value
            ]
            self.logger.info("Tests retrieved", count=len(tests))
            return r[t.SequenceOf[t.AttributeMapping]].ok(tests)
        except c.EXC_OS_VALIDATION as e:
            self.logger.exception("Failed to get tests", error=str(e))
            return r[t.SequenceOf[t.AttributeMapping]].fail(f"Failed to get tests: {e}")

    def _get_dbt_manifest_nodes(
        self,
        resource_type: str,
    ) -> p.Result[t.SequenceOf[p.Meltano.DbtManifestNode]]:
        def _run__get_dbt_manifest_nodes() -> p.Result[
            t.SequenceOf[p.Meltano.DbtManifestNode]
        ]:
            if not self._dbt_manifest:
                manifest_result = self.load_dbt_manifest()
                if manifest_result.failure:
                    return r[t.SequenceOf[p.Meltano.DbtManifestNode]].fail(
                        manifest_result.error or "Unknown error",
                    )
            if not self._dbt_manifest:
                return r[t.SequenceOf[p.Meltano.DbtManifestNode]].ok([])
            manifest_model = m.Meltano.DbtManifest.model_validate(self._dbt_manifest)
            parsed_nodes = [
                m.Meltano.DbtManifestNode.model_validate(node)
                for node in manifest_model.nodes.values()
            ]
            filtered_nodes = [
                node for node in parsed_nodes if node.resource_type == resource_type
            ]
            return r[t.SequenceOf[p.Meltano.DbtManifestNode]].ok(filtered_nodes)

        try:
            return _run__get_dbt_manifest_nodes()
        except c.EXC_OS_VALIDATION as e:
            return r[t.SequenceOf[p.Meltano.DbtManifestNode]].fail(
                f"Failed to read manifest nodes: {e}",
            )

    def load_dbt_manifest(
        self,
        manifest_path: Path | None = None,
    ) -> p.Result[t.Meltano.DbtManifestData]:
        """Load DBT manifest from file."""
        resolved_manifest_path = manifest_path

        def _run_load_dbt_manifest() -> p.Result[t.Meltano.DbtManifestData]:
            manifest_path_local = resolved_manifest_path
            if manifest_path_local is None:
                if self._dbt_project_root is None:
                    return r[t.Meltano.DbtManifestData].fail("No project loaded")
                manifest_path_local = (
                    self._dbt_project_root
                    / c.Meltano.FILE_PATH_DBT_OUTPUT_DIR
                    / c.Meltano.DBT_MANIFEST_FILE
                )
            if not manifest_path_local.exists():
                return r[t.Meltano.DbtManifestData].fail(
                    f"Manifest not found: {manifest_path_local}",
                )
            parsed_result = u.Cli.files_read_json_model(
                manifest_path_local,
                m.Meltano.DbtManifest,
            )
            if parsed_result.failure:
                return r[t.Meltano.DbtManifestData].fail_op(
                    "Manifest reading",
                    parsed_result.error,
                )
            parsed_manifest = parsed_result.value
            manifest_data: t.Meltano.DbtManifestData = {
                "nodes": {k: v.model_dump() for k, v in parsed_manifest.nodes.items()},
            }
            self._dbt_manifest = manifest_data
            self.logger.info("DBT manifest loaded", file=str(manifest_path))
            return r[t.Meltano.DbtManifestData].ok(self._dbt_manifest)

        try:
            return _run_load_dbt_manifest()
        except c.EXC_ATTR_KEY_OS_TYPE_VALUE as e:
            self.logger.exception("Failed to load manifest", error=str(e))
            return r[t.Meltano.DbtManifestData].fail(f"Failed to load manifest: {e}")

    def load_dbt_project(self, root: Path) -> p.Result[p.Meltano.DbtProjectInfo]:
        """Load a DBT project and discover models/tests from manifest."""

        def _run_load_dbt_project() -> p.Result[p.Meltano.DbtProjectInfo]:
            if not root.exists():
                return r[p.Meltano.DbtProjectInfo].fail(
                    f"DBT project directory not found: {root}",
                )
            self._dbt_project_root = root
            models_count = 0
            tests_count = 0
            manifest_result = self.load_dbt_manifest()
            if manifest_result.success:
                models_result = self.fetch_dbt_models()
                if models_result.success:
                    models_count = len(models_result.value)
                tests_result = self.fetch_dbt_tests()
                if tests_result.success:
                    tests_count = len(tests_result.value)
            info = m.Meltano.DbtProjectInfo(
                root=root,
                name=root.name,
                dbt_version=None,
                models_count=models_count,
                tests_count=tests_count,
            )
            self.logger.info(
                "DBT project loaded",
                root=str(root),
                models=models_count,
                tests=tests_count,
            )
            return r[p.Meltano.DbtProjectInfo].ok(info)

        try:
            return _run_load_dbt_project()
        except c.EXC_ATTR_KEY_OS_TYPE_VALUE as e:
            self.logger.exception("Failed to load DBT project", error=str(e))
            return r[p.Meltano.DbtProjectInfo].fail(f"Failed to load DBT project: {e}")


__all__: list[str] = ["FlextMeltanoDbtProjectMixin"]
