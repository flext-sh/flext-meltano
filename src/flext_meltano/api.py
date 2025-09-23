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
        **kwargs: object,
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
            # Validate project name
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

            # Create project configuration
            config_result = self._config_builders.build_project_config(
                project_name=project_name,
                project_root=project_root or Path.cwd(),
                **kwargs,
            )
            if config_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Config creation failed: {config_result.error}"
                )

            # Execute project creation through adapter
            creation_result = await self._adapter.create_project(config_result.unwrap())
            if creation_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Project creation failed: {creation_result.error}"
                )

            self._logger.info(f"Successfully created Meltano project: {project_name}")
            return FlextResult[FlextTypes.Core.Dict].ok({
                "name": project_name,
                "root": str(project_root or Path.cwd()),
                "config": config_result.unwrap(),
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
            validation_result = await self._adapter.validate_project(
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
        **kwargs: object,
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
            # Validate plugin configuration
            plugin_config = {
                "name": plugin_name,
                "type": plugin_type,
                "variant": variant or FlextMeltanoConstants.Plugin.DEFAULT_VARIANT,
                **kwargs,
            }

            validation_result = self._validators.validate_meltano_plugin_business_rules(
                plugin_config
            )
            if validation_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Plugin validation failed: {validation_result.error}"
                )

            # Install plugin through adapter
            installation_result = await self._adapter.install_plugin(plugin_config)
            if installation_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Plugin installation failed: {installation_result.error}"
                )

            self._logger.info(f"Successfully installed plugin: {plugin_name}")
            return FlextResult[FlextTypes.Core.Dict].ok({
                "plugin_name": plugin_name,
                "plugin_type": plugin_type,
                "variant": variant or FlextMeltanoConstants.Plugin.DEFAULT_VARIANT,
                "status": "installed",
                "details": installation_result.unwrap(),
            })

        except Exception as e:
            error_msg = f"Failed to install plugin {plugin_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    async def list_plugins(
        self,
        plugin_type: str | None = None,
    ) -> FlextResult[list[FlextTypes.Core.Dict]]:
        """List installed Meltano plugins.

        Args:
            plugin_type: Filter by plugin type (optional)

        Returns:
            FlextResult containing list of plugins or error details

        """
        try:
            plugins_result = await self._adapter.discover_plugins()
            if plugins_result.is_failure:
                return FlextResult[list[FlextTypes.Core.Dict]].fail(
                    f"Failed to list plugins: {plugins_result.error}"
                )

            return FlextResult[list[FlextTypes.Core.Dict]].ok(plugins_result.unwrap())

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
            # Create tap configuration
            if config:
                tap_config = FlextMeltanoModels.TapConfig(
                    tap_type=tap_name,
                    connection_config=config,
                )
            else:
                # Use existing tap configuration
                tap_config_result = await self._adapter.get_plugin_info(tap_name)
                if tap_config_result.is_failure:
                    return FlextResult[FlextTypes.Core.Dict].fail(
                        f"Failed to get tap config: {tap_config_result.error}"
                    )

                config_data = tap_config_result.unwrap()
                tap_config = FlextMeltanoModels.TapConfig(
                    tap_type=tap_name,
                    connection_config=config_data.get("config", {}),
                    stream_config=config_data.get("stream_config", {}),
                )

            # Generate catalog through tap abstractions
            discovery_result = await self._tap_abstractions.generate_catalog(
                tap_config.tap_type
            )
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
        catalog: FlextTypes.Core.Dict | None = None,
        state: FlextTypes.Core.Dict | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Extract data using a Singer tap.

        Args:
            tap_name: Name of the tap to use
            catalog: Optional catalog to use (defaults to discovery)
            state: Optional state for incremental extraction

        Returns:
            FlextResult containing extraction results or error details

        """
        try:
            # Get or discover catalog
            if not catalog:
                catalog_result = await self.discover_catalog(tap_name)
                if catalog_result.is_failure:
                    return FlextResult[FlextTypes.Core.Dict].fail(
                        f"Failed to discover catalog: {catalog_result.error}"
                    )
                catalog = catalog_result.unwrap()["catalog"]

            # Execute extraction through tap abstractions
            extraction_result = await self._tap_abstractions.extract_records(
                tap_name, catalog, state
            )
            if extraction_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Data extraction failed: {extraction_result.error}"
                )

            return FlextResult[FlextTypes.Core.Dict].ok({
                "tap_name": tap_name,
                "extraction_details": extraction_result.unwrap(),
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
        data_source: str | FlextTypes.Core.Dict,
        config: FlextTypes.Core.Dict | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Load data using a Singer target.

        Args:
            target_name: Name of the target to use
            data_source: Source of data (file path or data dict)
            config: Optional target configuration

        Returns:
            FlextResult containing load results or error details

        """
        try:
            # Create target configuration if needed
            if config:
                FlextMeltanoModels.TargetConfig(
                    target_type=target_name,
                    connection_config=config,
                )
            else:
                # Use existing target configuration
                target_config_result = await self._adapter.get_plugin_info(target_name)
                if target_config_result.is_failure:
                    return FlextResult[FlextTypes.Core.Dict].fail(
                        f"Failed to get target config: {target_config_result.error}"
                    )

                config_data = target_config_result.unwrap()
                FlextMeltanoModels.TargetConfig(
                    target_type=target_name,
                    connection_config=config_data.get("config", {}),
                )

            # Execute loading through target abstractions
            loading_result = await self._target_abstractions.load_batch(
                target_name, data_source
            )
            if loading_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Data loading failed: {loading_result.error}"
                )

            return FlextResult[FlextTypes.Core.Dict].ok({
                "target_name": target_name,
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
        **kwargs: object,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Run DBT models.

        Args:
            models: List of models to run (defaults to all)
            project_dir: DBT project directory
            **kwargs: Additional DBT configuration

        Returns:
            FlextResult containing execution results or error details

        """
        try:
            # Create DBT execution configuration
            dbt_execution = FlextMeltanoModels.DbtExecutionModel(
                command="run",
                models=models or [],
            )

            # Execute DBT through service
            execution_result = await self._service.run_models(
                dbt_execution, project_dir
            )
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
        **kwargs: object,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Test DBT models.

        Args:
            models: List of models to test (defaults to all)
            project_dir: DBT project directory
            **kwargs: Additional DBT configuration

        Returns:
            FlextResult containing test results or error details

        """
        try:
            # Create DBT execution configuration
            dbt_execution = FlextMeltanoModels.DbtExecutionModel(
                command="test",
                models=models or [],
            )

            # Execute DBT tests through service
            test_result = await self._service.run_models(dbt_execution, project_dir)
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
        dbt_models: list[str] | None = None,
        **_kwargs: object,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Run a complete ELT pipeline.

        Args:
            tap_name: Source tap to extract from
            target_name: Target to load to
            dbt_models: DBT models to run (optional)
            **kwargs: Additional pipeline configuration

        Returns:
            FlextResult containing pipeline results or error details

        """
        try:
            # Create pipeline execution model
            pipeline_result = FlextMeltanoModels.PipelineResult(
                pipeline_id=f"{tap_name}-{target_name}-pipeline",
            )

            # Extract phase
            self._logger.info(f"Starting extraction from {tap_name}")
            extract_result = await self.extract_data(tap_name)
            if extract_result.is_failure:
                pipeline_result.overall_status = "error"
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Extraction failed: {extract_result.error}"
                )

            pipeline_result.tap_result = FlextMeltanoModels.ExecutionResult(
                operation="extract",
                status="success",
                records_processed=int(extract_result.unwrap().get("record_count", 0)),
            )

            # Load phase
            self._logger.info(f"Starting load to {target_name}")
            load_result = await self.load_data(target_name, extract_result.unwrap())
            if load_result.is_failure:
                pipeline_result.overall_status = "error"
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Loading failed: {load_result.error}"
                )

            pipeline_result.target_result = FlextMeltanoModels.ExecutionResult(
                operation="load",
                status="success",
                records_processed=int(load_result.unwrap().get("record_count", 0)),
            )

            # Transform phase (optional)
            if dbt_models:
                self._logger.info("Starting DBT transformations")
                dbt_result = await self.run_dbt_models(dbt_models)
                if dbt_result.is_failure:
                    pipeline_result.overall_status = "partial"
                    pipeline_result.dbt_result = FlextMeltanoModels.ExecutionResult(
                        operation="transform",
                        status="error",
                        error_message=dbt_result.error,
                    )
                else:
                    pipeline_result.dbt_result = FlextMeltanoModels.ExecutionResult(
                        operation="transform",
                        status="success",
                    )

            # Calculate totals
            pipeline_result.overall_status = "success"
            pipeline_result.total_records = (
                pipeline_result.tap_result.records_processed
                if pipeline_result.tap_result
                else 0
            ) + (
                pipeline_result.target_result.records_processed
                if pipeline_result.target_result
                else 0
            )

            self._logger.info(
                f"Pipeline {pipeline_result.pipeline_id} completed successfully"
            )
            return FlextResult[FlextTypes.Core.Dict].ok({
                "pipeline_id": pipeline_result.pipeline_id,
                "status": pipeline_result.overall_status,
                "total_records": pipeline_result.total_records,
                "extract_result": extract_result.unwrap(),
                "load_result": load_result.unwrap(),
                "dbt_result": dbt_result.unwrap()
                if dbt_models and dbt_result.is_success
                else None,
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


__all__ = [
    "FlextMeltanoAPI",
]
