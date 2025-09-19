"""Test missing coverage for FlextMeltanoConfigBuilders methods.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_tests import FlextTestsUtilities

from flext_core import FlextResult
from flext_meltano.config_builders import FlextMeltanoConfigBuilders
from flext_meltano.constants import PluginTypes


class TestConfigBuildersMissingCoverage:
    """Test missing coverage for FlextMeltanoConfigBuilders methods."""

    def setup_method(self) -> None:
        """Setup test utilities."""
        self.test_assertions = FlextTestsUtilities.assertion()
        self.builder = FlextMeltanoConfigBuilders()

    def test_create_plugin_config_with_all_parameters(self) -> None:
        """Test create_plugin_config with all parameters."""
        result = self.builder.create_plugin_config(
            plugin_name="test-plugin",
            namespace="test-namespace",
            pip_url="test-pip-url",
            executable="test-executable",
            variant="test-variant",
            config_defaults={"key": "value"},
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

        if result.is_success:
            config = result.value
            self.test_assertions.assert_in(
                item="name",
                container=config,
                message="Should have name field",
            )
            self.test_assertions.assert_in(
                item="namespace",
                container=config,
                message="Should have namespace field",
            )
            self.test_assertions.assert_in(
                item="pip_url",
                container=config,
                message="Should have pip_url field",
            )
            self.test_assertions.assert_in(
                item="executable",
                container=config,
                message="Should have executable field",
            )
            self.test_assertions.assert_in(
                item="variant",
                container=config,
                message="Should have variant field",
            )
            self.test_assertions.assert_in(
                item="config",
                container=config,
                message="Should have config field",
            )

    def test_create_plugin_config_with_minimal_parameters(self) -> None:
        """Test create_plugin_config with minimal parameters."""
        result = self.builder.create_plugin_config(plugin_name="minimal-plugin")

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

        if result.is_success:
            config = result.value
            self.test_assertions.assert_equals(
                actual=config["name"],
                expected="minimal-plugin",
                message="Should have correct name",
            )

    def test_create_extractor_config_with_pip_url(self) -> None:
        """Test create_extractor_config with pip_url."""
        result = self.builder.create_extractor_config(
            tap_name="test-tap",
            pip_url="test-pip-url",
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

        if result.is_success:
            config = result.value
            self.test_assertions.assert_in(
                item="name",
                container=config,
                message="Should have name field",
            )
            self.test_assertions.assert_in(
                item="pip_url",
                container=config,
                message="Should have pip_url field",
            )

    def test_create_extractor_config_with_config_defaults(self) -> None:
        """Test create_extractor_config with config_defaults."""
        result = self.builder.create_extractor_config(
            tap_name="test-tap-config",
            pip_url="test-pip-url",
            config_defaults={"key": "value"},
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

        if result.is_success:
            config = result.value
            self.test_assertions.assert_in(
                item="executable",
                container=config,
                message="Should have executable field",
            )
            self.test_assertions.assert_in(
                item="config",
                container=config,
                message="Should have config field",
            )

    def test_create_loader_config_with_pip_url(self) -> None:
        """Test create_loader_config with pip_url."""
        result = self.builder.create_loader_config(
            target_name="test-target",
            pip_url="test-pip-url",
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

        if result.is_success:
            config = result.value
            self.test_assertions.assert_in(
                item="name",
                container=config,
                message="Should have name field",
            )
            self.test_assertions.assert_in(
                item="pip_url",
                container=config,
                message="Should have pip_url field",
            )

    def test_create_loader_config_with_config_defaults(self) -> None:
        """Test create_loader_config with config_defaults."""
        result = self.builder.create_loader_config(
            target_name="test-target-config",
            pip_url="test-pip-url",
            config_defaults={"key": "value"},
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

        if result.is_success:
            config = result.value
            self.test_assertions.assert_in(
                item="executable",
                container=config,
                message="Should have executable field",
            )
            self.test_assertions.assert_in(
                item="config",
                container=config,
                message="Should have config field",
            )

    def test_create_singer_config_generic_with_all_parameters(self) -> None:
        """Test _create_singer_config_generic with all parameters."""
        result = self.builder._create_singer_config_generic(
            plugin_name="test-singer-plugin",
            plugin_type=PluginTypes.EXTRACTORS.value,
            namespace="test-namespace",
            pip_url="test-pip-url",
            executable="test-executable",
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

        if result.is_success:
            config = result.value
            self.test_assertions.assert_in(
                item="name",
                container=config,
                message="Should have name field",
            )
            self.test_assertions.assert_in(
                item="namespace",
                container=config,
                message="Should have namespace field",
            )
            self.test_assertions.assert_in(
                item="pip_url",
                container=config,
                message="Should have pip_url field",
            )
            self.test_assertions.assert_in(
                item="executable",
                container=config,
                message="Should have executable field",
            )

    def test_create_singer_config_generic_with_minimal_parameters(self) -> None:
        """Test _create_singer_config_generic with minimal parameters."""
        result = self.builder._create_singer_config_generic(
            plugin_name="minimal-singer-plugin",
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

        if result.is_success:
            config = result.value
            self.test_assertions.assert_equals(
                actual=config["name"],
                expected="minimal-singer-plugin",
                message="Should have correct name",
            )

    def test_create_singer_config_generic_with_loaders_type(self) -> None:
        """Test _create_singer_config_generic with loaders type."""
        result = self.builder._create_singer_config_generic(
            plugin_name="test-loader",
            plugin_type=PluginTypes.LOADERS.value,
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

        if result.is_success:
            config = result.value
            self.test_assertions.assert_equals(
                actual=config["name"],
                expected="test-loader",
                message="Should have correct name",
            )

    def test_create_singer_config_generic_with_transforms_type(self) -> None:
        """Test _create_singer_config_generic with transforms type."""
        result = self.builder._create_singer_config_generic(
            plugin_name="test-transformer",
            plugin_type=PluginTypes.TRANSFORMS.value,
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

        if result.is_success:
            config = result.value
            self.test_assertions.assert_equals(
                actual=config["name"],
                expected="test-transformer",
                message="Should have correct name",
            )
