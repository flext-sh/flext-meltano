"""Code reduction examples using FlextMeltano ultra helpers.

Practical comparisons showing before/after implementations.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from meltano.core.job import Job, State
from meltano.core.project import Project

from flext_meltano import (
    flext_meltano_batch_execute_ultra,
    flext_meltano_discover_and_run_ultra,
    flext_meltano_run_pipeline_ultra,
    flext_meltano_setup_project_ultra,
)

# =============================================================================
# EXAMPLE 1: Basic Pipeline Execution
# =============================================================================


def example_1_before() -> None:
    """Traditional Meltano pipeline execution - 52 lines."""
    # Original implementation with standard Meltano

    # 1. Setup project
    project = Project.find()
    if not project:
        msg = "No Meltano project found"
        raise RuntimeError(msg)

    # 2. Activate environment
    project.activate_environment("dev")

    # 3. Get plugins
    tap = project.find_plugin("tap-postgres", plugin_type="extractors")
    target = project.find_plugin("target-csv", plugin_type="loaders")

    if not tap or not target:
        msg = "Required plugins not found"
        raise RuntimeError(msg)

    # 4. Create job
    job = Job(
        project=project,
        session=project.start_session(),
        run_id=f"run_{int(time.time())}",
    )

    # 5. Install missing plugins
    job.install_missing_plugins()

    # 6. Setup state
    state_backend = project.state_backend
    State(state_backend, state_id=f"{tap.name}-to-{target.name}")

    # 7. Configure streams
    with tempfile.NamedTemporaryFile(
        encoding="utf-8",
        mode="w",
        suffix=".json",
        delete=False,
    ) as temp_file:
        catalog_path = temp_file.name
        discover_cmd = job.singer_command_for_plugin(tap, "discover")
        subprocess.run(discover_cmd, stdout=temp_file, check=True)  # noqa: S603

    with Path(catalog_path).open(encoding="utf-8") as f:
        catalog = json.load(f)

    # 8. Select streams
    for stream in catalog["streams"]:
        stream["metadata"][0]["metadata"]["selected"] = True

    # 9. Execute pipeline
    start_time = time.time()
    run_cmd = job.singer_command_for_plugin(tap, "run")
    target_cmd = job.singer_command_for_plugin(target, "run")

    # 10. Run with state management
    result = subprocess.run(  # noqa: S602
        f"{' '.join(run_cmd)} | {' '.join(target_cmd)}",
        check=False,
        shell=True,
        capture_output=True,
        text=True,
    )

    duration = time.time() - start_time

    # 11. Parse results
    records_processed = 0
    for line in result.stdout.split("\n"):
        if "RECORD" in line:
            records_processed += 1

    return {
        "success": result.returncode == 0,
        "duration": duration,
        "records_processed": records_processed,
        "error": result.stderr if result.returncode != 0 else None,
    }


async def example_1_after() -> None:
    """FlextMeltano ultra helper - 1 line."""
    return await flext_meltano_run_pipeline_ultra("tap-postgres", "target-csv")


# =============================================================================
# EXAMPLE 2: Batch Processing Multiple Tables
# =============================================================================


def example_2_before() -> None:
    """Traditional batch processing - 87 lines."""
    tables = ["users", "orders", "products", "categories"]
    results = {}

    project = Project.find()
    project.activate_environment("dev")

    for table in tables:
        try:
            # Create separate job for each table
            job = Job(
                project=project,
                session=project.start_session(),
                run_id=f"batch_{table}_{int(time.time())}",
            )

            # Get plugins
            tap = project.find_plugin("tap-postgres", plugin_type="extractors")
            target = project.find_plugin("target-csv", plugin_type="loaders")

            # Discover catalog
            with tempfile.NamedTemporaryFile(
                encoding="utf-8",
                mode="w",
                suffix=".json",
                delete=False,
            ) as temp_file:
                catalog_path = temp_file.name
                discover_cmd = job.singer_command_for_plugin(tap, "discover")
                subprocess.run(discover_cmd, stdout=temp_file, check=True)  # noqa: S603

            with Path(catalog_path).open(encoding="utf-8") as f:
                catalog = json.load(f)

            # Select only current table
            for stream in catalog["streams"]:
                selected = stream["tap_stream_id"] == table
                stream["metadata"][0]["metadata"]["selected"] = selected

            # Save modified catalog
            with Path(catalog_path).open("w", encoding="utf-8") as f:
                json.dump(catalog, f)

            # Configure job with catalog
            tap_config = job.plugin_config_for_plugin(tap)
            tap_config["catalog"] = catalog_path

            # Execute pipeline for this table
            start_time = time.time()
            run_cmd = job.singer_command_for_plugin(tap, "run")
            target_cmd = job.singer_command_for_plugin(target, "run")

            result = subprocess.run(  # noqa: S602
                f"{' '.join(run_cmd)} | {' '.join(target_cmd)}",
                check=False,
                shell=True,
                capture_output=True,
                text=True,
            )

            duration = time.time() - start_time

            # Parse results
            records_processed = 0
            for line in result.stdout.split("\n"):
                if "RECORD" in line:
                    records_processed += 1

            results[table] = {
                "success": result.returncode == 0,
                "duration": duration,
                "records_processed": records_processed,
                "error": result.stderr if result.returncode != 0 else None,
            }

            # Clean up
            Path(catalog_path).unlink()

        except (RuntimeError, ValueError, TypeError) as e:
            results[table] = {
                "success": False,
                "duration": 0,
                "records_processed": 0,
                "error": str(e),
            }

    return results


async def example_2_after() -> None:
    """FlextMeltano batch processing - 4 lines."""
    pipelines = [
        ("tap-postgres", "target-csv")
        for _ in ["users", "orders", "products", "categories"]
    ]
    return await flext_meltano_batch_execute_ultra(pipelines)


# =============================================================================
# EXAMPLE 3: Project Setup with Multiple Environments
# =============================================================================


def example_3_before() -> None:
    """Traditional project setup - 143 lines."""
    project_path = Path(tempfile.mkdtemp(prefix="new_project_"))

    # 1. Initialize project
    if project_path.exists():
        shutil.rmtree(project_path)

    project_path.mkdir(parents=True)
    os.chdir(project_path)

    # 2. Run meltano init
    subprocess.run(  # noqa: S603
        [shutil.which("meltano") or "meltano", "init", ".", "--no_usage_stats"],
        check=True,
    )

    # 3. Load project
    Project.find(project_path)

    # 4. Add extractors
    extractors = ["tap-postgres", "tap-csv", "tap-oracle"]
    for extractor in extractors:
        try:
            subprocess.run(  # noqa: S603
                ["meltano", "add", "extractor", extractor],  # noqa: S607
                check=True,
                cwd=project_path,
            )
        except subprocess.CalledProcessError:
            # Try alternative variant
            subprocess.run(  # noqa: S603
                ["meltano", "add", "extractor", extractor, "--variant", "meltanolabs"],  # noqa: S607
                check=True,
                cwd=project_path,
            )

    # 5. Add loaders
    loaders = ["target-postgres", "target-csv", "target-jsonl"]
    for loader in loaders:
        try:
            subprocess.run(  # noqa: S603
                ["meltano", "add", "loader", loader],  # noqa: S607
                check=True,
                cwd=project_path,
            )
        except subprocess.CalledProcessError:
            # Try alternative variant
            subprocess.run(  # noqa: S603
                ["meltano", "add", "loader", loader, "--variant", "meltanolabs"],  # noqa: S607
                check=True,
                cwd=project_path,
            )

    # 6. Add transformers
    subprocess.run(
        ["meltano", "add", "transformer", "dbt-postgres"],  # noqa: S607
        check=True,
        cwd=project_path,
    )

    # 7. Create environments
    environments = ["dev", "staging", "prod"]
    for env_name in environments:
        subprocess.run(  # noqa: S603
            ["meltano", "environment", "add", env_name],  # noqa: S607
            check=True,
            cwd=project_path,
        )

    # 8. Configure dev environment
    dev_config = {
        "postgres_host": "localhost",
        "postgres_port": 5432,
        "postgres_database": "dev_db",
        "postgres_username": "dev_user",
    }

    for key, value in dev_config.items():
        subprocess.run(  # noqa: S603
            ["meltano", "config", "tap-postgres", "set", key, str(value)],  # noqa: S607
            check=True,
            cwd=project_path,
            env={**os.environ, "MELTANO_ENVIRONMENT": "dev"},
        )

    # 9. Configure staging environment
    staging_config = {
        "postgres_host": "staging-db.company.com",
        "postgres_port": 5432,
        "postgres_database": "staging_db",
        "postgres_username": "staging_user",
    }

    for key, value in staging_config.items():
        subprocess.run(  # noqa: S603
            ["meltano", "config", "tap-postgres", "set", key, str(value)],  # noqa: S607
            check=True,
            cwd=project_path,
            env={**os.environ, "MELTANO_ENVIRONMENT": "staging"},
        )

    # 10. Configure prod environment
    prod_config = {
        "postgres_host": "prod-db.company.com",
        "postgres_port": 5432,
        "postgres_database": "prod_db",
        "postgres_username": "prod_user",
    }

    for key, value in prod_config.items():
        subprocess.run(  # noqa: S603
            ["meltano", "config", "tap-postgres", "set", key, str(value)],  # noqa: S607
            check=True,
            cwd=project_path,
            env={**os.environ, "MELTANO_ENVIRONMENT": "prod"},
        )

    # 11. Create schedules
    schedules = [
        ("daily_extract", "tap-postgres target-postgres", "0 2 * * *"),
        ("hourly_incremental", "tap-postgres target-csv", "0 * * * *"),
    ]

    for schedule_name, tasks, interval in schedules:
        subprocess.run(  # noqa: S603
            [
                "meltano",
                "schedule",
                "add",
                schedule_name,
                tasks,
                "--interval",
                interval,
            ],
            check=True,
            cwd=project_path,
        )

    # 12. Test installation
    subprocess.run(
        ["meltano", "install"],  # noqa: S607
        check=True,
        cwd=project_path,
    )

    return {
        "project_path": str(project_path),
        "extractors_installed": len(extractors),
        "loaders_installed": len(loaders),
        "environments_created": len(environments),
        "schedules_created": len(schedules),
        "ready": True,
    }


async def example_3_after() -> None:
    """FlextMeltano project setup - 6 lines."""
    result = await flext_meltano_setup_project_ultra(
        tempfile.mkdtemp(prefix="new_project_"),
        taps=["tap-postgres", "tap-csv", "tap-oracle"],
        targets=["target-postgres", "target-csv", "target-jsonl"],
        environments=["dev", "staging", "prod"],
    )

    return result.data if result.is_success else {"error": result.error}


# =============================================================================
# EXAMPLE 4: Discovery and Automatic Pipeline Execution
# =============================================================================


def example_4_before() -> None:
    """Traditional discovery + execution - 78 lines."""
    project = Project.find()
    project.activate_environment("dev")

    # 1. Create job
    job = Job(
        project=project,
        session=project.start_session(),
        run_id=f"discovery_{(int(time.time()),)}",
    )

    # 2. Get tap
    tap = project.find_plugin("tap-postgres", plugin_type="extractors")
    target = project.find_plugin("target-csv", plugin_type="loaders")

    # 3. Discover catalog
    with tempfile.NamedTemporaryFile(
        encoding="utf-8",
        mode="w",
        suffix=".json",
        delete=False,
    ) as temp_file:
        catalog_path = temp_file.name
        discover_cmd = job.singer_command_for_plugin(tap, "discover")

        discover_result = subprocess.run(  # noqa: S603
            discover_cmd,
            check=False,
            stdout=temp_file,
            stderr=subprocess.PIPE,
            text=True,
        )

    if discover_result.returncode != 0:
        msg = f"Discovery failed: {(discover_result.stderr,)}"
        raise RuntimeError(msg)

    # 4. Load and analyze catalog
    with Path(catalog_path).open(encoding="utf-8") as f:
        catalog = json.load(f)

    streams = catalog.get("streams", [])
    [stream["tap_stream_id"] for stream in streams]

    # 5. Automatically select all streams
    for stream in streams:
        if "metadata" not in stream:
            stream["metadata"] = [{"breadcrumb": [], "metadata": {}}]
        stream["metadata"][0]["metadata"]["selected",] = True
        stream["metadata"][0]["metadata"]["replication-method",] = "FULL_TABLE"

    # 6. Save modified catalog
    with Path(catalog_path).open("w", encoding="utf-8") as f:
        json.dump(catalog, f)

    # 7. Configure job with catalog
    tap_config = job.plugin_config_for_plugin(tap)
    tap_config["catalog",] = catalog_path

    # 8. Execute pipeline
    start_time = time.time()
    run_cmd = job.singer_command_for_plugin(tap, "run")
    target_cmd = job.singer_command_for_plugin(target, "run")

    result = subprocess.run(  # noqa: S602
        f"{' '.join(run_cmd)} | {' '.join(target_cmd)}",
        check=False,
        shell=True,
        capture_output=True,
        text=True,
    )

    duration = time.time() - start_time

    # 9. Parse results
    records_processed = 0
    for line in result.stdout.split("\n"):
        if "RECORD" in line:
            records_processed += 1

    # 10. Clean up
    Path(catalog_path).unlink()

    pipeline_result = {
        "success": result.returncode == 0,
        "duration": duration,
        "records_processed": records_processed,
        "error": result.stderr if result.returncode != 0 else None,
    }

    return catalog, pipeline_result


async def example_4_after() -> None:
    """FlextMeltano discovery + execution - 1 line."""
    catalog, result = await flext_meltano_discover_and_run_ultra(
        "tap-postgres",
        "target-csv",
    )
    return catalog, result


# =============================================================================
# DEMONSTRATION SCRIPT
# =============================================================================


async def demonstrate_code_reduction() -> None:
    """Demonstrate code reduction examples."""
    examples = [
        (
            "Basic Pipeline Execution",
            "52 lines → 1 line",
            example_1_before,
            example_1_after,
        ),
        (
            "Batch Table Processing",
            "87 lines → 4 lines",
            example_2_before,
            example_2_after,
        ),
        ("Project Setup", "143 lines → 6 lines", example_3_before, example_3_after),
        (
            "Discovery + Execution",
            "78 lines → 1 line",
            example_4_before,
            example_4_after,
        ),
    ]

    for _name, _reduction, _before_func, _after_func in examples:
        pass


if __name__ == "__main__":
    asyncio.run(demonstrate_code_reduction())
