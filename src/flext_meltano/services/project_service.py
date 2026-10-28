"""FLEXT Pipeline Project Service - Enterprise project management foundation.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import tempfile
from collections.abc import Mapping
from pathlib import Path

from flext_meltano import FlextMeltanoServiceBase, c, e, p, r, t, u
from flext_meltano.services import FlextMeltanoAbstractions


class FlextMeltanoProjectService(FlextMeltanoServiceBase):
    """Enterprise pipeline project service with railway-oriented programming."""

    @staticmethod
    def _validate_project_parameters(
        project_id: str | None,
        prefix: str,
    ) -> p.Result[Mapping[str, str]]:
        """Validate temporary project creation parameters.

        Returns:
            The resulting ``p.Result[Mapping[str, str]]``.

        """
        if not prefix or not prefix.strip():
            return e.fail_validation(
                "Project prefix cannot be empty",
                result_type=r[Mapping[str, str]],
            )
        return r[Mapping[str, str]].ok({
            "project_id": project_id or "flext-meltano-project",
            "prefix": prefix.strip(),
        })

    def create_temporary_project(
        self,
        project_id: str | None = None,
        prefix: str = "flext_meltano_",
    ) -> p.Result[t.Meltano.DbtProject]:
        """Create temporary Meltano project with railway-oriented validation.

        Returns:
            The resulting ``p.Result[t.Meltano.DbtProject]``.

        """
        params_r = self._validate_project_parameters(project_id, prefix)
        if params_r.failure:
            return r[t.Meltano.DbtProject].from_failure(params_r)

        params = params_r.value
        try:
            temp_path = Path(tempfile.mkdtemp(prefix=params["prefix"]))
            settings: t.JsonMapping = {
                "requires_meltano": c.Meltano.VERSION_MELTANO_REQUIREMENT,
                "default_environment": c.Meltano.METADATA_DEFAULT_ENVIRONMENTS[0],
                "project_id": params["project_id"],
                "environments": [
                    {
                        "name": c.Meltano.METADATA_DEFAULT_ENVIRONMENTS[0],
                        "settings": {
                            "plugins": {
                                "extractors": [],
                                "loaders": [],
                                "transformers": [],
                            },
                        },
                    },
                ],
            }
            config_file = temp_path / c.Meltano.PATH_MELTANO_PROJECT_FILE
            dump_result = u.Cli.yaml_dump(config_file, settings)
            if dump_result.failure:
                return r[t.Meltano.DbtProject].from_failure(dump_result)
        except OSError as exc:
            return e.fail_operation(
                "Temp project creation",
                exc,
                result_type=r[t.Meltano.DbtProject],
            )

        inst_r = FlextMeltanoAbstractions.find_project(temp_path)
        if inst_r.failure:
            return r[t.Meltano.DbtProject].from_failure(inst_r)

        return r[t.Meltano.DbtProject].ok({
            "name": "meltano_project",
            "root": c.IDENTIFIER_UNKNOWN,
            "settings": "",
            "meltano_version": "",
        })


__all__: list[str] = ["FlextMeltanoProjectService"]
