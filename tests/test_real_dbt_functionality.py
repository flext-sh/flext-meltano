"""Comprehensive tests for real DBT functionality using dbt-core.

Tests validate actual DBT model execution, testing, and project operations.
All tests use real dbt-core integration without mocks.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from flext_meltano.core import FlextMeltanoDbtService


class TestFlextMeltanoDbtServiceReal:
    """Test real DBT service functionality with actual dbt-core."""

    @pytest.fixture
    def temp_dbt_project(self) -> Path:
        """Create temporary DBT project with basic structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Create dbt_project.yml
            dbt_project_content = """
name: 'test_project'
version: '1.0.0'
config-version: 2

profile: 'test_profile'

model-paths: ["models",]
analysis-paths: ["analyses",]
test-paths: ["tests",]
seed-paths: ["seeds",]
macro-paths: ["macros",]
snapshot-paths: ["snapshots",]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  test_project:
    +materialized: table
"""
            (project_dir / "dbt_project.yml").write_text(dbt_project_content.strip())

            # Create profiles.yml for testing
            profiles_dir = project_dir / ".dbt"
            profiles_dir.mkdir()
            profiles_content = """
test_profile:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: ':memory:'
      threads: 1
"""
            (profiles_dir / "profiles.yml").write_text(profiles_content.strip())

            # Create models directory with test model
            models_dir = project_dir / "models"
            models_dir.mkdir()

            # Simple test model
            test_model = """
{{ config(materialized='table') },}

select
    1 as id,
    'test' as name,
    current_timestamp as created_at
"""
            (models_dir / "test_model.sql").write_text(test_model.strip())

            # Create test for the model
            tests_dir = project_dir / "tests"
            tests_dir.mkdir()

            test_sql = """
select count(*) as failures
from {{ ref('test_model') },}
where id is null
"""
            (tests_dir / "test_model_not_null.sql").write_text(test_sql.strip())

            yield project_dir

    @pytest.fixture
    def dbt_service(self, temp_dbt_project: Path) -> FlextMeltanoDbtService:
        """Create DBT service with test project."""
        return FlextMeltanoDbtService(temp_dbt_project)

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_run_models_real(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test real DBT model execution with dbt-core."""
        result = await dbt_service.run_models()

        # Should succeed with real DBT project
        assert result.is_success, f"DBT run failed: {(result.error,)}"

        # Should return actual run results
        run_results = result.data
        assert isinstance(run_results, list)

        # With a real model, should have results
        if run_results:
            # Validate result structure
            for run_result in run_results:
                assert hasattr(run_result, "status")
                assert hasattr(run_result, "execution_time")

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_run_specific_models(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test running specific DBT models."""
        result = await dbt_service.run_models(models=["test_model"])

        # Should succeed with specific model
        assert result.is_success, f"DBT run failed: {(result.error,)}"

        run_results = result.data
        assert isinstance(run_results, list)

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_test_models_real(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test real DBT model testing with dbt-core."""
        # First run models to create tables
        run_result = await dbt_service.run_models()
        assert run_result.is_success, f"Model run failed: {(run_result.error,)}"

        # Then test models
        test_result = await dbt_service.test_models()

        # Should succeed with real DBT project
        assert test_result.is_success, f"DBT test failed: {(test_result.error,)}"

        # Should return actual test results
        test_results = test_result.data
        assert isinstance(test_results, list)

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_nonexistent_project(self) -> None:
        """Test DBT service with nonexistent project."""
        nonexistent_dir = Path("/tmp/nonexistent_dbt_project")
        service = FlextMeltanoDbtService(nonexistent_dir)

        result = await service.run_models()

        # Should fail gracefully
        assert not result.is_success
        assert "DBT project not found" in result.error

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_run_with_exclude(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test DBT run with exclude parameter."""
        result = await dbt_service.run_models(exclude=["nonexistent_model"])

        # Should succeed even with exclude
        assert result.is_success, f"DBT run with exclude failed: {(result.error,)}"

    def test_flext_meltano_dbt_get_version(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test getting DBT version."""
        version = dbt_service.get_dbt_version()

        # Should return actual version string
        assert isinstance(version, str)
        assert len(version) > 0
        assert "." in version  # Version should contain dots

    def test_flext_meltano_dbt_service_execute(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test DBT service execute method."""
        result = dbt_service.execute()

        # Should return service info
        assert result.is_success
        data = result.data
        assert isinstance(data, dict)
        assert data["service",] == "dbt"
        assert "project_dir" in data


class TestFlextMeltanoDbtServiceIntegration:
    """Integration tests for DBT service with various scenarios."""

    @pytest.fixture
    def complex_dbt_project(self) -> Path:
        """Create complex DBT project for integration testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Create dbt_project.yml with more complex configuration
            dbt_project_content = """
name: 'complex_test_project'
version: '1.0.0'
config-version: 2

profile: 'complex_profile'

model-paths: ["models",]
test-paths: ["tests",]
seed-paths: ["seeds",]

target-path: "target"

models:
  complex_test_project:
    staging:
      +materialized: view
    marts:
      +materialized: table
"""
            (project_dir / "dbt_project.yml").write_text(dbt_project_content.strip())

            # Create profile
            profiles_dir = project_dir / ".dbt"
            profiles_dir.mkdir()
            profiles_content = """
complex_profile:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: ':memory:'
      threads: 2
"""
            (profiles_dir / "profiles.yml").write_text(profiles_content.strip())

            # Create staging models
            staging_dir = project_dir / "models" / "staging"
            staging_dir.mkdir(parents=True)

            staging_model = """
{{ config(materialized='view') },}

select
    1 as raw_id,
    'raw_data' as raw_name,
    current_timestamp as loaded_at
"""
            (staging_dir / "stg_raw_data.sql").write_text(staging_model.strip())

            # Create marts models
            marts_dir = project_dir / "models" / "marts"
            marts_dir.mkdir()

            marts_model = """
{{ config(materialized='table') },}

select
    raw_id as id,
    upper(raw_name) as clean_name,
    loaded_at
from {{ ref('stg_raw_data') },}
"""
            (marts_dir / "dim_data.sql").write_text(marts_model.strip())

            yield project_dir

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_complex_project_run(
        self,
        complex_dbt_project: Path,
    ) -> None:
        """Test DBT with complex project structure."""
        service = FlextMeltanoDbtService(complex_dbt_project)

        # Run all models
        result = await service.run_models()
        assert result.is_success, f"Complex DBT run failed: {(result.error,)}"

        # Should have run multiple models
        run_results = result.data
        assert isinstance(run_results, list)

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_run_staging_only(
        self,
        complex_dbt_project: Path,
    ) -> None:
        """Test running only staging models."""
        service = FlextMeltanoDbtService(complex_dbt_project)

        result = await service.run_models(models=["staging"])
        assert result.is_success, f"Staging models run failed: {(result.error,)}"

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_run_marts_only(
        self,
        complex_dbt_project: Path,
    ) -> None:
        """Test running only marts models."""
        service = FlextMeltanoDbtService(complex_dbt_project)

        # First run staging (dependency)
        staging_result = await service.run_models(models=["staging"])
        assert staging_result.is_success

        # Then run marts
        marts_result = await service.run_models(models=["marts"])
        assert marts_result.is_success, (
            f"Marts models run failed: {(marts_result.error,)}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
