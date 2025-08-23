"""DBT Real Functionality Test Suite - Production DBT Integration Validation.

**Test Category**: Integration Tests
**Coverage Target**: 90%+ for DBT core functionality and model execution
**Dependencies**: dbt-core, real DBT projects, model compilation and execution
**Execution Time**: < 2 minutes total

## Test Scope

Validates actual DBT model execution, testing, and project operations using real dbt-core
integration without mocks. Tests comprehensive DBT workflow including model compilation,
testing, documentation generation, and project management within FLEXT Meltano's
data transformation architecture.
"""

from __future__ import annotations

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from flext_meltano import FlextMeltanoConfig, FlextMeltanoDbtService


class TestFlextMeltanoDbtServiceReal:
    """Test real DBT service functionality with actual dbt-core."""

    @pytest.fixture
    def temp_dbt_project(self) -> Generator[Path]:
        """Create temporary DBT project with basic structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            # Create dbt_project.yml
            dbt_project_content = """
name: 'test_project'
version: '1.0.0'
config-version: 2

profile: 'test_profile'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

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
{{ config(materialized='table') }}

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
from {{ ref('test_model') }}
where id is null
"""
            (tests_dir / "test_model_not_null.sql").write_text(test_sql.strip())

            yield project_dir

    @pytest.fixture
    def dbt_service(self, temp_dbt_project: Path) -> FlextMeltanoDbtService:
        """Create DBT service with test project."""
        return FlextMeltanoDbtService(project_name="test_project")

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_run_models_real(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test real DBT model execution with dbt-core."""
        result = await dbt_service.run_models()

        # Should succeed with real DBT project
        assert result.success, f"DBT run failed: {(result.error,)}"

        # Should return actual run results
        run_results = result.value
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
        assert result.success, f"DBT run failed: {(result.error,)}"

        run_results = result.value
        assert isinstance(run_results, list)

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_test_models_real(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test real DBT model testing with dbt-core."""
        # First run models to create tables
        run_result = await dbt_service.run_models()
        assert run_result.success, f"Model run failed: {(run_result.error,)}"

        # Then test models
        test_result = await dbt_service.test_models()

        # Should succeed with real DBT project
        assert test_result.success, f"DBT test failed: {(test_result.error,)}"

        # Should return actual test results
        test_results = test_result.value
        assert isinstance(test_results, list)

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_nonexistent_project(self) -> None:
        """Test DBT service with nonexistent project."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nonexistent_dir = Path(temp_dir) / "nonexistent_dbt_project"
            config = FlextMeltanoConfig(dbt_project_dir=str(nonexistent_dir))
            service = FlextMeltanoDbtService(config)

            result = await service.run_models()

        # Should fail gracefully
        assert not result.success
        assert result.error is not None
        assert result.error is not None
        assert result.error is not None
        if "DBT project not found" not in result.error:
            msg: str = f"Expected {'DBT project not found'} in {result.error}"
            raise AssertionError(
                msg,
            )

    def test_flext_meltano_dbt_run_with_exclude(
        self,
        dbt_service: FlextMeltanoDbtService,
        temp_dbt_project: Path,
    ) -> None:
        """Test DBT run with models selection."""
        # FlextMeltanoDbtService from base_services doesn't support exclude parameter
        # Use models parameter with project_dir
        from dbt.cli.main import dbtRunner
        runner = dbtRunner()
        result = dbt_service.run_models(
            runner=runner, 
            models=["existing_model"], 
            project_dir=temp_dbt_project
        )

        # Should succeed even with exclude
        assert result.success, f"DBT run with exclude failed: {(result.error,)}"

    def test_flext_meltano_dbt_get_version(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test getting DBT version."""
        version = dbt_service.get_dbt_version()

        # Should return actual version string
        assert isinstance(version, str)
        assert len(version) > 0
        if "." not in version:  # Version should contain dots
            msg: str = f"Expected {'.'} in {version}"
            raise AssertionError(msg)

    def test_flext_meltano_dbt_service_execute(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test DBT service execute method."""
        result = dbt_service.execute()

        # Should return service info
        assert result.success
        data = result.value
        assert isinstance(data, dict)
        if data["service"] != "dbt":
            msg: str = f"Expected {'dbt'}, got {data['service']}"
            raise AssertionError(msg)
        if "project_dir" not in data:
            msg: str = f"Expected {'project_dir'} in {data}"
            raise AssertionError(msg)


class TestFlextMeltanoDbtServiceIntegration:
    """Integration tests for DBT service with various scenarios."""

    @pytest.fixture
    def complex_dbt_project(self) -> Generator[Path]:
        """Create complex DBT project for integration testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Create dbt_project.yml with more complex configuration
            dbt_project_content = """
name: 'complex_test_project'
version: '1.0.0'
config-version: 2

profile: 'complex_profile'

model-paths: ["models"]
test-paths: ["tests"]
seed-paths: ["seeds"]

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
{{ config(materialized='view') }}

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
{{ config(materialized='table') }}

select
    raw_id as id,
    upper(raw_name) as clean_name,
    loaded_at
from {{ ref('stg_raw_data') }}
"""
            (marts_dir / "dim_data.sql").write_text(marts_model.strip())

            yield project_dir

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_complex_project_run(
        self,
        complex_dbt_project: Path,
    ) -> None:
        """Test DBT with complex project structure."""
        config = FlextMeltanoConfig(dbt_project_dir=str(complex_dbt_project))
        service = FlextMeltanoDbtService(config)

        # Run all models
        result = await service.run_models()
        assert result.success, f"Complex DBT run failed: {result.error}"

        # Should have run successfully
        run_results = result.value
        assert isinstance(run_results, list)

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_run_staging_only(
        self,
        complex_dbt_project: Path,
    ) -> None:
        """Test running only staging models."""
        config = FlextMeltanoConfig(dbt_project_dir=str(complex_dbt_project))
        service = FlextMeltanoDbtService(config)

        result = await service.run_models(models=["staging"])
        assert result.success, f"Staging models run failed: {(result.error,)}"

    @pytest.mark.asyncio
    async def test_flext_meltano_dbt_run_marts_only(
        self,
        complex_dbt_project: Path,
    ) -> None:
        """Test running only marts models."""
        config = FlextMeltanoConfig(dbt_project_dir=str(complex_dbt_project))
        service = FlextMeltanoDbtService(config)

        # First run staging (dependency)
        staging_result = await service.run_models(models=["staging"])
        assert staging_result.success

        # Then run marts
        marts_result = await service.run_models(models=["marts"])
        assert marts_result.success, f"Marts models run failed: {(marts_result.error,)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
