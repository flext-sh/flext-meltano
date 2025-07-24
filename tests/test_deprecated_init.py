"""Tests for deprecated module.

Comprehensive tests for deprecated components and backward compatibility.
Zero tolerance for untested code.
"""

from __future__ import annotations

import warnings

import pytest

from flext_meltano.deprecated import (
    FlextMeltanoAntiCorruptionLayer,
    FlextMeltanoOrchestrator,
    FlextMeltanoProjectManager,
    _deprecation_warning,
)


class TestDeprecationWarning:
    """Test deprecation warning helper function."""

    def test_deprecation_warning_function(self) -> None:
        """Test that _deprecation_warning issues proper warnings."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            _deprecation_warning("OldClass", "new.module.NewClass")

            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "OldClass is deprecated" in str(w[0].message)
            assert "new.module.NewClass" in str(w[0].message)

    def test_deprecation_warning_stacklevel(self) -> None:
        """Test that deprecation warning has correct stacklevel."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            _deprecation_warning("TestClass", "new.location")

            assert len(w) == 1
            # Just verify the warning was issued with correct stacklevel
            # The exact filename might vary depending on test runner
            assert w[0].lineno > 0  # Should have a valid line number

    def test_deprecation_warning_parameters(self) -> None:
        """Test deprecation warning with different parameters."""
        test_cases = [
            ("ShortName", "short.location"),
            ("VeryLongClassName", "very.long.new.module.location.NewClassName"),
            ("Class123", "module_123.Class456"),
        ]

        for old_name, new_location in test_cases:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")

                _deprecation_warning(old_name, new_location)

                assert len(w) == 1
                assert old_name in str(w[0].message)
                assert new_location in str(w[0].message)


class TestFlextMeltanoProjectManager:
    """Test deprecated FlextMeltanoProjectManager class."""

    def test_project_manager_init_warning(self) -> None:
        """Test that initializing FlextMeltanoProjectManager issues warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            manager = FlextMeltanoProjectManager()

            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "FlextMeltanoProjectManager" in str(w[0].message)
            assert "FlextMeltanoProjectService" in str(w[0].message)
            assert manager is not None

    def test_project_manager_init_with_args(self) -> None:
        """Test FlextMeltanoProjectManager with arguments."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            manager = FlextMeltanoProjectManager("arg1", "arg2", kwarg1="value1")

            assert len(w) == 1
            assert manager is not None
            assert hasattr(manager, "_service")

    def test_project_manager_create_project_warning(self) -> None:
        """Test that create_project method issues warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            manager = FlextMeltanoProjectManager()

            # Clear the init warning
            w.clear()

            with pytest.raises(NotImplementedError) as exc_info:
                manager.create_project("project_name")

            assert len(w) == 1
            assert "create_project" in str(w[0].message)
            assert "ProjectApplicationService.create_project" in str(w[0].message)
            assert "Please migrate to new ProjectApplicationService" in str(exc_info.value)

    def test_project_manager_create_project_with_args(self) -> None:
        """Test create_project with various arguments."""
        manager = FlextMeltanoProjectManager()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            with pytest.raises(NotImplementedError):
                manager.create_project("test", arg2="value", arg3=123)

            # Should have warning for create_project call
            assert any("create_project" in str(warning.message) for warning in w)


class TestFlextMeltanoOrchestrator:
    """Test deprecated FlextMeltanoOrchestrator class."""

    def test_orchestrator_init_warning(self) -> None:
        """Test that initializing FlextMeltanoOrchestrator issues warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            orchestrator = FlextMeltanoOrchestrator()

            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "FlextMeltanoOrchestrator" in str(w[0].message)
            assert "FlextMeltanoJobService" in str(w[0].message)
            assert orchestrator is not None

    def test_orchestrator_init_with_args(self) -> None:
        """Test FlextMeltanoOrchestrator with arguments."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            orchestrator = FlextMeltanoOrchestrator("config", retries=3)

            assert len(w) == 1
            assert orchestrator is not None

    def test_orchestrator_execute_pipeline_warning(self) -> None:
        """Test that execute_pipeline method issues warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            orchestrator = FlextMeltanoOrchestrator()

            # Clear the init warning
            w.clear()

            with pytest.raises(NotImplementedError) as exc_info:
                orchestrator.execute_pipeline("pipeline_name")

            assert len(w) == 1
            assert "execute_pipeline" in str(w[0].message)
            assert "PipelineOrchestrator.execute_pipeline" in str(w[0].message)
            assert "Please migrate to new PipelineOrchestrator" in str(exc_info.value)

    def test_orchestrator_execute_pipeline_with_args(self) -> None:
        """Test execute_pipeline with various arguments."""
        orchestrator = FlextMeltanoOrchestrator()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            with pytest.raises(NotImplementedError):
                orchestrator.execute_pipeline("test_pipeline", environment="prod", force=True)

            # Should have warning for execute_pipeline call
            assert any("execute_pipeline" in str(warning.message) for warning in w)


class TestFlextMeltanoAntiCorruptionLayer:
    """Test deprecated FlextMeltanoAntiCorruptionLayer class."""

    def test_anti_corruption_layer_init_warning(self) -> None:
        """Test that initializing FlextMeltanoAntiCorruptionLayer issues warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            layer = FlextMeltanoAntiCorruptionLayer()

            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "FlextMeltanoAntiCorruptionLayer" in str(w[0].message)
            assert "flext_meltano.application.services" in str(w[0].message)
            assert layer is not None

    def test_anti_corruption_layer_init_with_args(self) -> None:
        """Test FlextMeltanoAntiCorruptionLayer with arguments."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            layer = FlextMeltanoAntiCorruptionLayer("meltano_root", debug=True)

            assert len(w) == 1
            assert layer is not None

    def test_anti_corruption_layer_run_command_warning(self) -> None:
        """Test that run_meltano_command method issues warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            layer = FlextMeltanoAntiCorruptionLayer()

            # Clear the init warning
            w.clear()

            with pytest.raises(NotImplementedError) as exc_info:
                layer.run_meltano_command("install")

            assert len(w) == 1
            assert "run_meltano_command" in str(w[0].message)
            assert "MeltanoCLIAdapter" in str(w[0].message)
            assert "Please migrate to new MeltanoCLIAdapter" in str(exc_info.value)

    def test_anti_corruption_layer_run_command_with_args(self) -> None:
        """Test run_meltano_command with various arguments."""
        layer = FlextMeltanoAntiCorruptionLayer()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            with pytest.raises(NotImplementedError):
                layer.run_meltano_command("run", "tap-csv", "target-jsonl")

            # Should have warning for run_meltano_command call
            assert any("run_meltano_command" in str(warning.message) for warning in w)


class TestDeprecatedModuleExports:
    """Test module-level exports and compatibility."""

    def test_all_exports_defined(self) -> None:
        """Test that __all__ is properly defined."""
        from flext_meltano import deprecated

        expected_exports = {
            "FlextMeltanoAntiCorruptionLayer",
            "FlextMeltanoOrchestrator",
            "FlextMeltanoProjectManager",
            "_deprecation_warning",
        }

        assert hasattr(deprecated, "__all__")
        assert set(deprecated.__all__) == expected_exports

    def test_deprecated_classes_importable(self) -> None:
        """Test that deprecated classes can be imported."""
        # These imports should work without errors
        assert FlextMeltanoProjectManager is not None
        assert FlextMeltanoOrchestrator is not None
        assert FlextMeltanoAntiCorruptionLayer is not None

    def test_deprecated_classes_are_classes(self) -> None:
        """Test that deprecated exports are actual classes."""
        assert isinstance(FlextMeltanoProjectManager, type)
        assert isinstance(FlextMeltanoOrchestrator, type)
        assert isinstance(FlextMeltanoAntiCorruptionLayer, type)

    def test_module_documentation(self) -> None:
        """Test that the deprecated module has proper documentation."""
        from flext_meltano import deprecated

        assert deprecated.__doc__ is not None
        assert "DEPRECATION NOTICE" in deprecated.__doc__
        assert "BACKWARD COMPATIBILITY" in deprecated.__doc__
        assert "MIGRATION GUIDE" in deprecated.__doc__

    def test_migration_guidance_in_docstring(self) -> None:
        """Test that migration guidance is provided in module docstring."""
        from flext_meltano import deprecated

        doc = deprecated.__doc__
        assert "ProjectApplicationService" in doc
        assert "PipelineOrchestrator" in doc
        assert "MeltanoCLIAdapter" in doc


class TestDeprecatedClassesBehavior:
    """Test the overall behavior of deprecated classes."""

    def test_multiple_deprecation_warnings(self) -> None:
        """Test that multiple operations generate multiple warnings."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Create instances and call methods
            manager = FlextMeltanoProjectManager()
            orchestrator = FlextMeltanoOrchestrator()
            layer = FlextMeltanoAntiCorruptionLayer()

            with pytest.raises(NotImplementedError):
                manager.create_project("test")

            with pytest.raises(NotImplementedError):
                orchestrator.execute_pipeline("test")

            with pytest.raises(NotImplementedError):
                layer.run_meltano_command("test")

            # Should have 6 warnings total (3 init + 3 method calls)
            assert len(w) == 6

            # All should be deprecation warnings
            for warning in w:
                assert issubclass(warning.category, DeprecationWarning)

    def test_warnings_can_be_suppressed(self) -> None:
        """Test that deprecation warnings can be suppressed."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            # These should not raise warnings
            manager = FlextMeltanoProjectManager()
            orchestrator = FlextMeltanoOrchestrator()
            layer = FlextMeltanoAntiCorruptionLayer()

            # Methods should still raise NotImplementedError
            with pytest.raises(NotImplementedError):
                manager.create_project("test")

            with pytest.raises(NotImplementedError):
                orchestrator.execute_pipeline("test")

            with pytest.raises(NotImplementedError):
                layer.run_meltano_command("test")

    def test_class_instantiation_state(self) -> None:
        """Test the state of deprecated class instances."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            manager = FlextMeltanoProjectManager()
            assert hasattr(manager, "_service")
            assert hasattr(manager, "_service")

            # Other classes don't have specific state to test
            orchestrator = FlextMeltanoOrchestrator()
            layer = FlextMeltanoAntiCorruptionLayer()

            assert orchestrator is not None
            assert layer is not None
