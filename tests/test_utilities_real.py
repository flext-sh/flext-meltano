"""Testes REAIS para utilities - SEM MOCKS.

Este módulo testa as funcionalidades REAIS das utilidades:
- FlextMeltanoUtilities
- validate_config_value
- validate_directory_path
- validate_file_path
- FlextResult patterns
"""

from __future__ import annotations

import math
import shutil
import tempfile
from pathlib import Path

from flext_meltano.utilities import (
    FlextMeltanoUtilities,
    validate_config_value,
    validate_directory_path,
    validate_file_path,
)


class TestFlextMeltanoUtilitiesReal:
    """Testes REAIS das utilities - sem mocks."""

    def test_utilities_save_yaml_config(self) -> None:
        """Testa salvamento de configuração YAML real."""
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w", suffix=".yaml", delete=False
        ) as temp_file:
            config: dict[str, object] = {"test_key": "test_value", "nested": {"key": "value"}}
            temp_path = Path(temp_file.name)

        try:
            result = FlextMeltanoUtilities.save_yaml_config(config, temp_path)

            # Deve retornar sucesso
            assert result.success is True

            # Usando unwrap_or pattern
            success = result.unwrap_or(False)
            assert success is True

            # Arquivo deve existir e ter conteúdo correto
            assert temp_path.exists()

            # Verificar conteúdo lendo de volta
            loaded_result = FlextMeltanoUtilities.load_yaml_config(temp_path)
            assert loaded_result.success is True
            loaded_config = loaded_result.value
            assert loaded_config == config

        finally:
            temp_path.unlink(missing_ok=True)

    def test_utilities_load_yaml_config_real(self) -> None:
        """Testa carregamento de configuração YAML real."""
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w", suffix=".yaml", delete=False
        ) as temp_file:
            temp_file.write("test_key: test_value\nnested:\n  key: value\n")
            temp_path = Path(temp_file.name)

        try:
            result = FlextMeltanoUtilities.load_yaml_config(temp_path)

            # Deve retornar sucesso
            assert result.success is True

            # Usar padrão .value com type assertion segura
            config = result.value
            assert isinstance(config, dict)
            config_dict: dict[str, object] = config
            assert config_dict["test_key"] == "test_value"
            nested = config_dict["nested"]
            assert isinstance(nested, dict)
            assert nested["key"] == "value"

        finally:
            temp_path.unlink(missing_ok=True)

    def test_utilities_create_temp_directory(self) -> None:
        """Testa criação de diretório temporário."""
        temp_dir = FlextMeltanoUtilities.create_temp_directory("test_prefix_")

        assert temp_dir is not None
        assert isinstance(temp_dir, Path)
        assert temp_dir.exists()
        assert temp_dir.is_dir()

        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)


class TestValidateConfigValueReal:
    """Testes REAIS da função validate_config_value."""

    def test_validate_config_value_string(self) -> None:
        """Testa validação de valor string."""
        result = validate_config_value("test_value", str)

        assert result.success is True
        validated_value = result.value
        assert validated_value == "test_value"
        assert isinstance(validated_value, str)

    def test_validate_config_value_int(self) -> None:
        """Testa validação de valor inteiro."""
        result = validate_config_value("42", int)

        assert result.success is True
        validated_value = result.value
        assert validated_value == 42
        assert isinstance(validated_value, int)

    def test_validate_config_value_bool_true(self) -> None:
        """Testa validação de valor booleano True."""
        result = validate_config_value("true", bool)

        assert result.success is True
        validated_value = result.value
        assert validated_value is True
        assert isinstance(validated_value, bool)

    def test_validate_config_value_bool_false(self) -> None:
        """Testa validação de valor booleano False."""
        result = validate_config_value("false", bool)

        assert result.success is True
        validated_value = result.value
        assert validated_value is False
        assert isinstance(validated_value, bool)

    def test_validate_config_value_float(self) -> None:
        """Testa validação de valor float."""
        result = validate_config_value("3.14", float)

        assert result.success is True
        validated_value = result.value
        assert validated_value == 3.14
        assert isinstance(validated_value, float)

    def test_validate_config_value_none_required(self) -> None:
        """Testa validação com valor None obrigatório."""
        result = validate_config_value(None, str, required=True)

        assert result.success is False
        assert result.error is not None
        assert "Required config value is None" in result.error

    def test_validate_config_value_none_optional(self) -> None:
        """Testa validação com valor None opcional."""
        result = validate_config_value(None, str, required=False)

        # Deve aceitar None quando não obrigatório
        assert result.success is True
        validated_value = result.value
        assert validated_value is None

    def test_validate_config_value_unwrap_or_pattern(self) -> None:
        """Testa uso do padrão unwrap_or com validate_config_value."""
        # Valor válido
        result = validate_config_value("123", int)
        value = result.unwrap_or(0)
        assert value == 123

        # Valor inválido
        result = validate_config_value("invalid", int)
        value = result.unwrap_or(0)
        assert value == 0  # Default devido ao erro


class TestPathValidationReal:
    """Testes REAIS de validação de paths."""

    def test_validate_directory_path_existing(self) -> None:
        """Testa validação de diretório existente."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            result = validate_directory_path(str(temp_path))

            assert result is not None  # Função retorna str | None
            assert result == str(temp_path)

    def test_validate_directory_path_non_existing(self) -> None:
        """Testa validação de diretório inexistente."""
        non_existing_path = "/path/that/does/not/exist"

        result = validate_directory_path(non_existing_path)

        assert result is None  # Função retorna None para paths inexistentes

    def test_validate_file_path_existing(self) -> None:
        """Testa validação de arquivo existente."""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            result = validate_file_path(str(temp_path))

            assert result is not None  # Função retorna str | None
            assert result == str(temp_path)

        finally:
            temp_path.unlink(missing_ok=True)

    def test_validate_file_path_non_existing(self) -> None:
        """Testa validação de arquivo inexistente."""
        non_existing_file = "/path/to/non/existing/file.txt"

        result = validate_file_path(non_existing_file)

        assert result is None  # Função retorna None para paths inexistentes
