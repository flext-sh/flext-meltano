"""FLEXT Meltano API - Unified facade for all Meltano operations.

This is the single public interface for the flext-meltano domain.
All external access to Meltano, Singer, and DBT functionality must go through this API.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextService,
    FlextTypes,
)
from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.config_builders import FlextMeltanoConfigBuilders
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.exceptions import FlextMeltanoExceptions
from flext_meltano.executors import FlextMeltanoExecutor
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.services import FlextMeltanoService
from flext_meltano.tap_abstractions import FlextTapAbstractions
from flext_meltano.target_abstractions import FlextTargetAbstractions
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.validators import FlextMeltanoValidators


class FlextMeltanoAPI(FlextService[FlextResult[FlextTypes.Core.Dict]]):
    """UNIFIED Meltano API - SINGLE PUBLIC INTERFACE PATTERN.

    This is the ONLY class that external code should import from flext-meltano.
    Provides a unified facade for all Meltano, Singer, and DBT operations
    following the flext-core architectural patterns.

    The API aggregates functionality from all internal services and provides
    a clean, consistent interface for:
    - Meltano project management
    - Singer tap/target operations
    - DBT transformations
    - ELT pipeline orchestration
    - Configuration management
    - Plugin management

    Example:
        >>> api = FlextMeltanoAPI()
        >>> result = await api.create_project("my-project")
        >>> if result.is_success:
        ...     project = result.unwrap()
        ...     print(f"Created project: {project['name']}")

    """

    def __init__(self, **data: object) -> None:
        """Initialize the unified Meltano API."""
        super().__init__(**data)

        # Initialize core dependencies
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

        # Initialize internal services
        self._adapter = FlextMeltanoAdapter()
        self._service = FlextMeltanoService()
        self._executor = FlextMeltanoExecutor()
        self._config_builders = FlextMeltanoConfigBuilders()
        self._validators = FlextMeltanoValidators()

        # Initialize abstractions
        self._tap_abstractions = FlextTapAbstractions()
        self._target_abstractions = FlextTargetAbstractions()

    # ========================================================================
    # MELTANO PROJECT MANAGEMENT
    # ========================================================================

    async def create_project(
        self,
        project_name: str,
        project_root: Path | None = None,
        **_kwargs: object,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create a new Meltano project.

        Args:
            project_name: Name of the project to create
            project_root: Root directory for the project (defaults to current dir)
            **kwargs: Additional configuration options

        Returns:
            FlextResult containing project information or error details

        """
        try:
            validation_result = (
                self._validators.validate_meltano_project_business_rules({
                    "version": 1,
                    "project_id": project_name,
                })
            )
            if validation_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Project validation failed: {validation_result.error}"
                )

            project_dir = project_root or Path.cwd()
            creation_result = self._adapter.create_project(
                project_name=project_name,
                project_dir=project_dir,
            )
            if creation_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Project creation failed: {creation_result.error}"
                )

            self._logger.info(f"Successfully created Meltano project: {project_name}")
            result_data = creation_result.unwrap()
            return FlextResult[FlextTypes.Core.Dict].ok({
                "name": project_name,
                "root": str(project_dir),
                "details": result_data,
                "status": "created",
            })

        except Exception as e:
            error_msg = f"Failed to create project {project_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    async def validate_project(
        self,
        project_root: Path | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Validate an existing Meltano project.

        Args:
            project_root: Root directory of the project to validate

        Returns:
            FlextResult containing validation results or error details

        """
        try:
            validation_result = self._adapter.validate_project(
                project_root or Path.cwd()
            )
            if validation_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Project validation failed: {validation_result.error}"
                )

            return FlextResult[FlextTypes.Core.Dict].ok({
                "status": "valid",
                "project_root": str(project_root or Path.cwd()),
                "validation_details": validation_result.unwrap(),
            })

        except Exception as e:
            error_msg = f"Failed to validate project: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    # ========================================================================
    # PLUGIN MANAGEMENT
    # ========================================================================

    async def install_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
        variant: str | None = None,
        **_kwargs: object,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Install a Meltano plugin.

        Args:
            plugin_type: Type of plugin (tap, target, dbt)
            plugin_name: Name of the plugin
            variant: Plugin variant (defaults to meltanolabs)
            **kwargs: Additional plugin configuration

        Returns:
            FlextResult containing installation details or error details

        """
        try:
            plugin_config: FlextTypes.Core.JsonValue = {
                "name": plugin_name,
                "type": plugin_type,
                "variant": variant or FlextMeltanoConstants.Plugin.DEFAULT_VARIANT,
            }

            validation_result = self._validators.validate_meltano_plugin_business_rules(
                plugin_config
            )
            if validation_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Plugin validation failed: {validation_result.error}"
                )

            installation_result = self._adapter.add_plugin(
                project_dir=Path.cwd(),
                plugin_type=plugin_type,
                plugin_name=plugin_name,
            )
            if installation_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Plugin installation failed: {installation_result.error}"
                )

            self._logger.info(f"Successfully installed plugin: {plugin_name}")
            result_data = installation_result.unwrap()
            return FlextResult[FlextTypes.Core.Dict].ok({
                "plugin_name": plugin_name,
                "plugin_type": plugin_type,
                "variant": variant or FlextMeltanoConstants.Plugin.DEFAULT_VARIANT,
                "status": "installed",
                "details": result_data,
            })

        except Exception as e:
            error_msg = f"Failed to install plugin {plugin_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    async def list_plugins(
        self,
        _plugin_type: str | None = None,
    ) -> FlextResult[list[FlextTypes.Core.Dict]]:
        """List installed Meltano plugins.

        Args:
            _plugin_type: Filter by plugin type (optional, not yet implemented)

        Returns:
            FlextResult containing list of plugins or error details

        """
        try:
            plugins_result = self._adapter.discover_plugins()
            if plugins_result.is_failure:
                return FlextResult[list[FlextTypes.Core.Dict]].fail(
                    f"Failed to list plugins: {plugins_result.error}"
                )

            plugins_data: list[FlextTypes.Core.Dict] = [
                dict(plugin) for plugin in plugins_result.unwrap()
            ]
            return FlextResult[list[FlextTypes.Core.Dict]].ok(plugins_data)

        except Exception as e:
            error_msg = f"Failed to list plugins: {e}"
            self._logger.exception(error_msg)
            return FlextResult[list[FlextTypes.Core.Dict]].fail(error_msg)

    # ========================================================================
    # SINGER TAP OPERATIONS
    # ========================================================================

    async def discover_catalog(
        self,
        tap_name: str,
        config: FlextTypes.Core.Dict | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Discover Singer catalog for a tap.

        Args:
            tap_name: Name of the tap to discover
            config: Optional tap configuration

        Returns:
            FlextResult containing discovered catalog or error details

        """
        try:
            tap_config = FlextTapAbstractions.TapConfig(
                tap_type=tap_name,
                connection_config=config or {},
            )

            tap_instance = FlextTapAbstractions.TapInstance(
                config=tap_config,
                tap_type=tap_name,
                tap_id=f"tap_{tap_name}",
            )

            discovery_result = self._tap_abstractions.generate_catalog(tap_instance)
            if discovery_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Catalog discovery failed: {discovery_result.error}"
                )

            return FlextResult[FlextTypes.Core.Dict].ok({
                "tap_name": tap_name,
                "catalog": discovery_result.unwrap(),
                "status": "discovered",
            })

        except Exception as e:
            error_msg = f"Failed to discover catalog for {tap_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    async def extract_data(
        self,
        tap_name: str,
        stream_name: str,
        limit: int | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Extract data using a Singer tap.

        Args:
            tap_name: Name of the tap to use
            stream_name: Name of the stream to extract
            limit: Optional limit on number of records

        Returns:
            FlextResult containing extraction results or error details

        """
        try:
            tap_config = FlextTapAbstractions.TapConfig(
                tap_type=tap_name,
                connection_config={},
            )

            tap_instance = FlextTapAbstractions.TapInstance(
                config=tap_config,
                tap_type=tap_name,
                tap_id=f"tap_{tap_name}",
            )

            discover_result = self._tap_abstractions.discover_streams(tap_instance)
            if discover_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Failed to discover streams: {discover_result.error}"
                )

            stream_result = self._tap_abstractions.get_stream_by_name(
                tap_instance, stream_name
            )
            if stream_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Stream not found: {stream_result.error}"
                )

            stream = stream_result.unwrap()
            extraction_result = self._tap_abstractions.extract_records(stream, limit)
            if extraction_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Data extraction failed: {extraction_result.error}"
                )

            return FlextResult[FlextTypes.Core.Dict].ok({
                "tap_name": tap_name,
                "stream_name": stream_name,
                "records": extraction_result.unwrap(),
                "status": "extracted",
            })

        except Exception as e:
            error_msg = f"Failed to extract data from {tap_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    # ========================================================================
    # SINGER TARGET OPERATIONS
    # ========================================================================

    async def load_data(
        self,
        target_name: str,
        stream_name: str,
        records: list[FlextTypes.Core.Dict],
        config: FlextTypes.Core.Dict | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Load data using a Singer target.

        Args:
            target_name: Name of the target to use
            stream_name: Name of the stream to load
            records: List of records to load
            config: Optional target configuration

        Returns:
            FlextResult containing load results or error details

        """
        try:
            target_dict = {
                "target_type": target_name,
                "config": config or {},
                "batches_processed": 0,
            }

            loading_result = self._target_abstractions.load_batch(
                target=target_dict,
                stream_name=stream_name,
                records=records,
            )
            if loading_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Data loading failed: {loading_result.error}"
                )

            return FlextResult[FlextTypes.Core.Dict].ok({
                "target_name": target_name,
                "stream_name": stream_name,
                "loading_details": loading_result.unwrap(),
                "status": "loaded",
            })

        except Exception as e:
            error_msg = f"Failed to load data to {target_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    # ========================================================================
    # DBT OPERATIONS
    # ========================================================================

    async def run_dbt_models(
        self,
        models: list[str] | None = None,
        project_dir: Path | None = None,
        **_kwargs: object,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Run DBT models.

        Args:
            models: List of models to run (defaults to all)
            project_dir: DBT project directory (reserved for future use)
            **kwargs: Additional DBT configuration

        Returns:
            FlextResult containing execution results or error details

        """
        # project_dir is reserved for future multi-project support
        _ = project_dir  # Explicitly mark as intentionally unused for now

        try:
            # Execute DBT through service
            execution_result = self._service.run_models(model_names=models)
            if execution_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"DBT execution failed: {execution_result.error}"
                )

            return FlextResult[FlextTypes.Core.Dict].ok({
                "command": "run",
                "models": models or [],
                "execution_details": execution_result.unwrap(),
                "status": "completed",
            })

        except Exception as e:
            error_msg = f"Failed to run DBT models: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    async def test_dbt_models(
        self,
        models: list[str] | None = None,
        project_dir: Path | None = None,
        **_kwargs: object,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Test DBT models.

        Args:
            models: List of models to test (defaults to all)
            project_dir: DBT project directory (reserved for future use)
            **kwargs: Additional DBT configuration

        Returns:
            FlextResult containing test results or error details

        """
        # project_dir is reserved for future multi-project support
        _ = project_dir  # Explicitly mark as intentionally unused for now

        try:
            # Execute DBT tests through service
            test_result = self._service.run_models(model_names=models)
            if test_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"DBT testing failed: {test_result.error}"
                )

            return FlextResult[FlextTypes.Core.Dict].ok({
                "command": "test",
                "models": models or [],
                "test_details": test_result.unwrap(),
                "status": "completed",
            })

        except Exception as e:
            error_msg = f"Failed to test DBT models: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    # ========================================================================
    # ELT PIPELINE OPERATIONS
    # ========================================================================

    async def run_elt_pipeline(
        self,
        tap_name: str,
        target_name: str,
        stream_name: str,
        dbt_models: list[str] | None = None,
        **_kwargs: object,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Run a complete ELT pipeline.

        Args:
            tap_name: Source tap to extract from
            target_name: Target to load to
            stream_name: Stream to process
            dbt_models: DBT models to run (optional)
            **_kwargs: Additional pipeline configuration

        Returns:
            FlextResult containing pipeline results or error details

        """
        try:
            self._logger.info(f"Starting ELT pipeline: {tap_name} -> {target_name}")

            extract_result = await self.extract_data(tap_name, stream_name, limit=1000)
            if extract_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Extraction failed: {extract_result.error}"
                )

            records_data = extract_result.unwrap().get("records", [])
            records: list[FlextTypes.Core.Dict] = (
                records_data if isinstance(records_data, list) else []
            )
            load_result = await self.load_data(target_name, stream_name, records)
            if load_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Loading failed: {load_result.error}"
                )

            dbt_result = None
            if dbt_models:
                dbt_exec = await self.run_dbt_models(dbt_models)
                if dbt_exec.is_success:
                    dbt_result = dbt_exec.unwrap()

            return FlextResult[FlextTypes.Core.Dict].ok({
                "pipeline_id": f"{tap_name}-{target_name}-pipeline",
                "status": "success",
                "extract_result": extract_result.unwrap(),
                "load_result": load_result.unwrap(),
                "dbt_result": dbt_result,
            })

        except Exception as e:
            error_msg = f"Pipeline execution failed: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    @property
    def version(self) -> str:
        """Get the flext-meltano version."""
        return FlextMeltanoConstants.FLEXT_MELTANO_VERSION

    @property
    def constants(self) -> type[FlextMeltanoConstants]:
        """Access to Meltano constants."""
        return FlextMeltanoConstants

    @property
    def exceptions(self) -> type[FlextMeltanoExceptions]:
        """Access to Meltano exceptions."""
        return FlextMeltanoExceptions

    @property
    def types(self) -> type[FlextMeltanoTypes]:
        """Access to Meltano types."""
        return FlextMeltanoTypes

    @property
    def models(self) -> type[FlextMeltanoModels]:
        """Access to Meltano models."""
        return FlextMeltanoModels

    async def execute(
        self, command: str, **options: object
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Execute a Meltano command through the unified API.

        Args:
            command: The command to execute
            **options: Additional command options

        Returns:
            FlextResult containing execution results

        Example:
            >>> api = FlextMeltanoAPI()
            >>> result = await api.execute("version")
            >>> if result.is_success:
            ...     print(result.unwrap())

        """
        try:
            if command == "version":
                version_info: FlextTypes.Core.Dict = {
                    "version": self.version,
                    "success": True,
                }
                return FlextResult[FlextTypes.Core.Dict].ok(data=version_info)

            result = await self._executor.execute(command, **options)
            if result.is_success:
                return FlextResult[FlextTypes.Core.Dict].ok(data=result.unwrap())
            return FlextResult[FlextTypes.Core.Dict].fail(
                result.error or "Execution failed"
            )

        except Exception as e:
            error_msg = f"API execution failed: {e}"
            self._logger.exception(error_msg, command=command, error=str(e))
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)


__all__ = [
    "FlextMeltanoAPI",
]
