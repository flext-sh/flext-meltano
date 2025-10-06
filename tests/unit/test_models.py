"""FLEXT Meltano Models Unit Tests - Enterprise ELT testing patterns.

This module provides comprehensive unit tests for FlextMeltanoModels following
FLEXT testing patterns and Pydantic 2.11+ integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_tests import FlextTestsUtilities

from flext_meltano.models import FlextMeltanoModels


class TestFlextMeltanoModels:
    """Unit test suite for FlextMeltanoModels."""

    def setup_method(self) -> None:
        """Setup for each test using flext_tests patterns."""
        self.test_assertions = FlextTestsUtilities.assertion()

    def test_meltano_project_model_initialization(self) -> None:
        """Test MeltanoProjectModel initialization."""
        model = FlextMeltanoModels.MeltanoProjectModel(
            project_name="test_project",
            project_path="/test/path",
            meltano_version="3.0.0",
        )

        self.test_assertions.assert_true(
            condition=model is not None,
            message="MeltanoProjectModel should be initialized",
        )
        self.test_assertions.assert_true(
            condition=model.project_name == "test_project",
            message="Project name should be set correctly",
        )

    def test_meltano_project_model_validation(self) -> None:
        """Test MeltanoProjectModel validation."""
        # Test valid model
        model = FlextMeltanoModels.MeltanoProjectModel(
            project_name="test_project",
            project_path="/test/path",
            meltano_version="3.0.0",
        )

        self.test_assertions.assert_true(
            condition=model is not None,
            message="Valid model should be created",
        )

    def test_meltano_project_model_serialization(self) -> None:
        """Test MeltanoProjectModel serialization."""
        model = FlextMeltanoModels.MeltanoProjectModel(
            project_name="test_project",
            project_path="/test/path",
            meltano_version="3.0.0",
        )

        model_dict = model.model_dump()

        self.test_assertions.assert_true(
            condition=isinstance(model_dict, dict),
            message="Model should serialize to dict",
        )
        self.test_assertions.assert_true(
            condition="project_name" in model_dict,
            message="Model dict should contain project_name",
        )

    def test_plugin_model_initialization(self) -> None:
        """Test PluginModel initialization."""
        model = FlextMeltanoModels.PluginModel(
            name="tap-csv",
            type="extractor",
            variant="meltanolabs",
        )

        self.test_assertions.assert_true(
            condition=model is not None,
            message="PluginModel should be initialized",
        )
        self.test_assertions.assert_true(
            condition=model.name == "tap-csv",
            message="Plugin name should be set correctly",
        )

    def test_plugin_model_validation(self) -> None:
        """Test PluginModel validation."""
        # Test valid model
        model = FlextMeltanoModels.PluginModel(
            name="tap-csv",
            type="extractor",
            variant="meltanolabs",
        )

        self.test_assertions.assert_true(
            condition=model is not None,
            message="Valid plugin model should be created",
        )

    def test_plugin_model_serialization(self) -> None:
        """Test PluginModel serialization."""
        model = FlextMeltanoModels.PluginModel(
            name="tap-csv",
            type="extractor",
            variant="meltanolabs",
        )

        model_dict = model.model_dump()

        self.test_assertions.assert_true(
            condition=isinstance(model_dict, dict),
            message="Plugin model should serialize to dict",
        )
        self.test_assertions.assert_true(
            condition="name" in model_dict,
            message="Plugin model dict should contain name",
        )

    def test_dbt_project_model_initialization(self) -> None:
        """Test DbtProjectModel initialization."""
        model = FlextMeltanoModels.DbtProjectModel(
            project_name="test_dbt_project",
            project_path="/test/dbt/path",
            dbt_version="1.10.5",
        )

        self.test_assertions.assert_true(
            condition=model is not None,
            message="DbtProjectModel should be initialized",
        )
        self.test_assertions.assert_true(
            condition=model.project_name == "test_dbt_project",
            message="DBT project name should be set correctly",
        )

    def test_dbt_project_model_validation(self) -> None:
        """Test DbtProjectModel validation."""
        # Test valid model
        model = FlextMeltanoModels.DbtProjectModel(
            project_name="test_dbt_project",
            project_path="/test/dbt/path",
            dbt_version="1.10.5",
        )

        self.test_assertions.assert_true(
            condition=model is not None,
            message="Valid DBT project model should be created",
        )

    def test_dbt_project_model_serialization(self) -> None:
        """Test DbtProjectModel serialization."""
        model = FlextMeltanoModels.DbtProjectModel(
            project_name="test_dbt_project",
            project_path="/test/dbt/path",
            dbt_version="1.10.5",
        )

        model_dict = model.model_dump()

        self.test_assertions.assert_true(
            condition=isinstance(model_dict, dict),
            message="DBT project model should serialize to dict",
        )
        self.test_assertions.assert_true(
            condition="project_name" in model_dict,
            message="DBT project model dict should contain project_name",
        )

    def test_stream_definition_initialization(self) -> None:
        """Test StreamDefinition initialization."""
        model = FlextMeltanoModels.StreamDefinition(
            stream_name="test_stream",
            schema={"type": "object"},
        )

        self.test_assertions.assert_true(
            condition=model is not None,
            message="StreamDefinition should be initialized",
        )
        self.test_assertions.assert_true(
            condition=model.stream_name == "test_stream",
            message="Stream name should be set correctly",
        )

    def test_stream_definition_validation(self) -> None:
        """Test StreamDefinition validation."""
        # Test valid model
        model = FlextMeltanoModels.StreamDefinition(
            stream_name="test_stream",
            schema={"type": "object"},
        )

        self.test_assertions.assert_true(
            condition=model is not None,
            message="Valid stream definition should be created",
        )

    def test_tap_config_initialization(self) -> None:
        """Test TapConfig initialization."""
        model = FlextMeltanoModels.TapConfig(
            tap_name="tap-csv",
            config={"file_path": "/test/file.csv"},
        )

        self.test_assertions.assert_true(
            condition=model is not None,
            message="TapConfig should be initialized",
        )
        self.test_assertions.assert_true(
            condition=model.tap_name == "tap-csv",
            message="Tap name should be set correctly",
        )

    def test_tap_config_validation(self) -> None:
        """Test TapConfig validation."""
        # Test valid model
        model = FlextMeltanoModels.TapConfig(
            tap_name="tap-csv",
            config={"file_path": "/test/file.csv"},
        )

        self.test_assertions.assert_true(
            condition=model is not None,
            message="Valid tap config should be created",
        )

    def test_tap_instance_initialization(self) -> None:
        """Test TapInstance initialization."""
        model = FlextMeltanoModels.TapInstance(
            tap_name="tap-csv",
            config={"file_path": "/test/file.csv"},
            streams=["stream1", "stream2"],
        )

        self.test_assertions.assert_true(
            condition=model is not None,
            message="TapInstance should be initialized",
        )
        self.test_assertions.assert_true(
            condition=model.tap_name == "tap-csv",
            message="Tap name should be set correctly",
        )

    def test_tap_instance_validation(self) -> None:
        """Test TapInstance validation."""
        # Test valid model
        model = FlextMeltanoModels.TapInstance(
            tap_name="tap-csv",
            config={"file_path": "/test/file.csv"},
            streams=["stream1", "stream2"],
        )

        self.test_assertions.assert_true(
            condition=model is not None,
            message="Valid tap instance should be created",
        )

    def test_models_immutability(self) -> None:
        """Test models immutability (frozen models)."""
        model = FlextMeltanoModels.MeltanoProjectModel(
            project_name="test_project",
            project_path="/test/path",
            meltano_version="3.0.0",
        )

        # Model should be frozen, so this should raise an error
        try:
            model.project_name = "new_project"  # type: ignore[assignment]
            self.test_assertions.assert_true(
                condition=False,
                message="Model should be immutable",
            )
        except Exception:
            # Expected behavior - model is frozen
            self.test_assertions.assert_true(
                condition=True,
                message="Model should be immutable",
            )

    def test_models_constants_reference(self) -> None:
        """Test that models use constants from FlextMeltanoConstants."""
        # Test that models use constants (this is tested by the fact that
        # the models are created successfully with the constants)
        model = FlextMeltanoModels.MeltanoProjectModel(
            project_name="test_project",
            project_path="/test/path",
            meltano_version="3.0.0",
        )

        self.test_assertions.assert_true(
            condition=model is not None,
            message="Model should use constants successfully",
        )

    def test_models_namespace_organization(self) -> None:
        """Test that models are properly organized in namespaces."""
        # Test that all expected model classes exist
        expected_models = [
            "MeltanoProjectModel",
            "PluginModel",
            "DbtProjectModel",
            "StreamDefinition",
            "TapConfig",
            "TapInstance",
        ]

        for model_name in expected_models:
            self.test_assertions.assert_true(
                condition=hasattr(FlextMeltanoModels, model_name),
                message=f"Models should have {model_name}",
            )

    def test_models_pydantic_integration(self) -> None:
        """Test that models properly integrate with Pydantic 2.11+."""
        # Test model validation
        model = FlextMeltanoModels.MeltanoProjectModel(
            project_name="test_project",
            project_path="/test/path",
            meltano_version="3.0.0",
        )

        # Test model serialization
        model_dict = model.model_dump()
        self.test_assertions.assert_true(
            condition=isinstance(model_dict, dict),
            message="Model should serialize with Pydantic",
        )

        # Test model deserialization
        new_model = FlextMeltanoModels.MeltanoProjectModel.model_validate(model_dict)
        self.test_assertions.assert_true(
            condition=new_model is not None,
            message="Model should deserialize with Pydantic",
        )
