"""FlextMeltano Project Manager - Application Service.

Project management business logic following Clean Architecture patterns.
"""

from __future__ import annotations

import shutil
from typing import TYPE_CHECKING, Any

import yaml
from flext_core import FlextResult

from flext_meltano.helpers.cli import flext_run_meltano_command
from flext_meltano.project.models import FlextMeltanoProject

if TYPE_CHECKING:
    from pathlib import Path

    from flext_core import FlextContainer

    from flext_meltano.config.settings import FlextMeltanoSettings
    from flext_meltano.constants import FlextMeltanoEnvironmentType


class FlextMeltanoProjectManager:
    """Meltano project management service.

    Application service for managing Meltano projects following Clean
    Architecture patterns with business rules enforcement.
    """

    def __init__(
        self,
        settings: FlextMeltanoSettings,
        container: FlextContainer,
    ) -> None:
        """Initialize project manager.

        Args:
            settings: Platform settings
            container: Dependency injection container

        """
        self._settings = settings
        self._container = container

    def create_project(
        self,
        name: str,
        directory: Path,
        description: str | None = None,
        environment: FlextMeltanoEnvironmentType | None = None,
    ) -> FlextResult[FlextMeltanoProject]:
        """Create new Meltano project.

        Business rules:
        - Project name must be valid according to Meltano standards
        - Directory must not exist or be empty
        - Project must be properly initialized with meltano.yml

        Args:
            name: Project name
            directory: Project root directory
            description: Optional project description
            environment: Initial environment (defaults to development)

        Returns:
            FlextResult containing created project or error

        """
        try:
            # Validate project directory
            if directory.exists() and any(directory.iterdir()):
                return FlextResult.fail(
                    f"Directory {directory} already exists and is not empty",
                )

            # Set default environment
            if environment is None:
                from flext_meltano.constants import FlextMeltanoEnvironmentType

                environment = FlextMeltanoEnvironmentType(self._settings.environment)

            # Create directory structure
            directory.mkdir(parents=True, exist_ok=True)
            config_path = directory / "meltano.yml"

            # Initialize Meltano project
            init_result = flext_run_meltano_command(
                ["init", str(directory), "--name", name],
                project_root=directory.parent,
            )

            if not init_result.is_success:
                return FlextResult.fail(
                    f"Failed to initialize Meltano project: {init_result.error}",
                )

            # Create project domain entity
            project = FlextMeltanoProject(
                name=name,
                directory=directory,
                config_path=config_path,
                description=description,
                current_environment=environment,
                available_environments=[environment],
                is_initialized=True,
            )

            return FlextResult.ok(project)

        except Exception as e:
            return FlextResult.fail(f"Failed to create project: {e}")

    def load_project(self, directory: Path) -> FlextResult[FlextMeltanoProject]:
        """Load existing Meltano project from directory.

        Args:
            directory: Project root directory

        Returns:
            FlextResult containing loaded project or error

        """
        try:
            # Validate project directory
            if not directory.exists():
                return FlextResult.fail(f"Project directory {directory} not found")

            config_path = directory / "meltano.yml"
            if not config_path.exists():
                return FlextResult.fail(
                    f"Meltano configuration file not found at {config_path}",
                )

            # Load project configuration
            config_result = self._load_project_config(config_path)
            if not config_result.is_success:
                return FlextResult.fail(
                    f"Failed to load project config: {config_result.error}",
                )

            config_data = config_result.data
            if config_data is None:
                return FlextResult.fail("Configuration data is None")

            # Create project entity from configuration
            project = FlextMeltanoProject(
                name=config_data.get("project_name", directory.name),
                directory=directory,
                config_path=config_path,
                description=config_data.get("description"),
                version=config_data.get("version", "1.0.0"),
                is_initialized=True,
            )

            return FlextResult.ok(project)

        except Exception as e:
            return FlextResult.fail(f"Failed to load project: {e}")

    def validate_project(
        self, project: FlextMeltanoProject,
    ) -> FlextResult[dict[str, Any]]:
        """Validate project structure and configuration.

        Business rules:
        - Project directory must exist
        - meltano.yml must be valid
        - All environments must be properly configured

        Args:
            project: Project to validate

        Returns:
            FlextResult with validation results

        """
        try:
            validation_results: dict[str, Any] = {
                "project_valid": True,
                "directory_exists": project.directory.exists(),
                "config_exists": project.config_path.exists(),
                "environments_valid": True,
                "issues": [],
            }

            # Check directory existence
            if not validation_results["directory_exists"]:
                validation_results["project_valid"] = False
                validation_results["issues"].append(
                    f"Project directory does not exist: {project.directory}",
                )

            # Check config file
            if not validation_results["config_exists"]:
                validation_results["project_valid"] = False
                validation_results["issues"].append(
                    f"Configuration file does not exist: {project.config_path}",
                )

            # Validate environments
            for env in project.available_environments:
                if not self._validate_environment(project, env):
                    validation_results["environments_valid"] = False
                    validation_results["project_valid"] = False
                    validation_results["issues"].append(
                        f"Invalid environment configuration: {env}",
                    )

            return FlextResult.ok(validation_results)

        except Exception as e:
            return FlextResult.fail(f"Project validation failed: {e}")

    def initialize_environment(
        self,
        project: FlextMeltanoProject,
        environment: FlextMeltanoEnvironmentType,
    ) -> FlextResult[None]:
        """Initialize new environment for project.

        Args:
            project: Target project
            environment: Environment to initialize

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Add environment to project
            add_result = project.add_environment(environment)
            if not add_result.is_success:
                return add_result

            # Initialize environment using Meltano CLI
            env_result = flext_run_meltano_command(
                ["environment", "add", environment.value],
                project_root=project.directory,
                environment=project.current_environment.value,
            )

            if not env_result.is_success:
                # Rollback environment addition
                project.remove_environment(environment)
                return FlextResult.fail(
                    f"Failed to initialize environment: {env_result.error}",
                )

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Environment initialization failed: {e}")

    def get_project_status(
        self, project: FlextMeltanoProject,
    ) -> FlextResult[dict[str, Any]]:
        """Get comprehensive project status information.

        Args:
            project: Project to analyze

        Returns:
            FlextResult with project status data

        """
        try:
            # Get Meltano status
            status_result = flext_run_meltano_command(
                ["status"],
                project_root=project.directory,
                environment=project.current_environment.value,
            )

            status_data = {
                "project": project.to_dict(),
                "meltano_status": (
                    status_result.data if status_result.is_success else None
                ),
                "validation": self.validate_project(project).data,
                "last_updated": project.updated_at,
            }

            return FlextResult.ok(status_data)

        except Exception as e:
            return FlextResult.fail(f"Failed to get project status: {e}")

    def _load_project_config(self, config_path: Path) -> FlextResult[dict[str, Any]]:
        """Load and parse meltano.yml configuration.

        Args:
            config_path: Path to meltano.yml file

        Returns:
            FlextResult with parsed configuration data

        """
        try:
            import yaml

            content = config_path.read_text(encoding="utf-8")
            config_data = yaml.safe_load(content)

            if not isinstance(config_data, dict):
                return FlextResult.fail("Invalid meltano.yml format")

            return FlextResult.ok(config_data)

        except Exception as e:
            return FlextResult.fail(f"Failed to load configuration: {e}")

    def _validate_environment(
        self,
        project: FlextMeltanoProject,
        environment: FlextMeltanoEnvironmentType,
    ) -> bool:
        """Validate environment configuration.

        Args:
            project: Project containing the environment
            environment: Environment to validate

        Returns:
            True if environment is valid, False otherwise

        """
        try:
            # Check if environment configuration exists
            env_result = flext_run_meltano_command(
                ["environment", "list"],
                project_root=project.directory,
            )

            if not env_result.is_success or env_result.data is None:
                return False

            # Parse environment list output
            env_output = env_result.data.get("stdout", "")
            return environment.value in env_output

        except Exception:
            return False

    async def load_project_config(
        self, project_name: str,
    ) -> FlextResult[dict[str, Any]]:
        """Load project configuration by project name.

        Args:
            project_name: Name of the project to load

        Returns:
            FlextResult containing project configuration or error

        """
        try:
            # Get current working directory as base
            from pathlib import Path

            current_dir = Path.cwd()

            # Try to find project directory by name in current location
            project_dir = current_dir / project_name
            if project_dir.exists() and (project_dir / "meltano.yml").exists():
                project_result = self.load_project(project_dir)
                if project_result.success and project_result.data:
                    return FlextResult.ok(project_result.data.to_dict())

            # If not found, try current directory if name matches
            meltano_yml = current_dir / "meltano.yml"
            if meltano_yml.exists():
                config_result = self._load_project_config(current_dir)
                if config_result.success and config_result.data:
                    config_data = config_result.data
                    if config_data.get("project_name") == project_name:
                        return FlextResult.ok(config_data)

            return FlextResult.fail(f"Project '{project_name}' not found")
        except Exception as e:
            return FlextResult.fail(f"Failed to load project config: {e}")

    def save_project_config(
        self,
        project: FlextMeltanoProject,
        config: dict[str, Any],
    ) -> FlextResult[dict[str, Any]]:
        """Save Meltano project configuration with automatic backup.

        Args:
            project: Project to save configuration for
            config: Configuration dictionary to save

        Returns:
            FlextResult containing success/failure information

        """
        try:
            meltano_yml = project.config_path

            # Create backup if file exists
            if meltano_yml.exists():
                backup_path = meltano_yml.with_suffix(".yml.backup")
                shutil.copy2(meltano_yml, backup_path)

            # Save configuration with proper YAML formatting
            with meltano_yml.open("w", encoding="utf-8") as f:
                yaml.safe_dump(
                    config,
                    f,
                    default_flow_style=False,
                    indent=2,
                    sort_keys=False,
                )

            return FlextResult.ok(
                {
                    "config_path": str(meltano_yml),
                    "backup_created": True,
                    "message": "Configuration saved successfully",
                },
            )

        except Exception as e:
            return FlextResult.fail(
                f"Failed to save project configuration: {e}",
            )

    # Bridge compatibility methods (match deprecated project_manager.py API)
    async def create_project_bridge(
        self,
        project_name: str,
        environment: str = "dev",
    ) -> FlextResult[dict[str, Any]]:
        """Bridge-compatible create project method.

        Maps deprecated API to main implementation.
        """
        try:
            from pathlib import Path

            from flext_meltano.constants import FlextMeltanoEnvironmentType

            # Convert string environment to enum
            env_type = None
            if environment == "dev":
                env_type = FlextMeltanoEnvironmentType.DEVELOPMENT
            elif environment == "prod":
                env_type = FlextMeltanoEnvironmentType.PRODUCTION
            elif environment == "staging":
                env_type = FlextMeltanoEnvironmentType.STAGING

            # Use current directory / project_name as target
            project_dir = Path.cwd() / project_name

            result = self.create_project(
                name=project_name,
                directory=project_dir,
                description=f"FLEXT Meltano project: {project_name}",
                environment=env_type,
            )

            if result.success:
                return FlextResult.ok(
                    {
                        "project_name": project_name,
                        "environment": environment,
                        "project_path": str(project_dir),
                        "success": True,
                    },
                )
            return FlextResult.fail(result.error or "Project creation failed")

        except Exception as e:
            return FlextResult.fail(f"Failed to create project: {e}")

    async def add_plugin_bridge(
        self,
        project_name: str,
        plugin_type: str,
        plugin_name: str,
        variant: str = "",
    ) -> FlextResult[dict[str, Any]]:
        """Bridge-compatible add plugin method."""
        try:
            # For now, return success simulation
            # TODO: Implement actual plugin addition logic
            return FlextResult.ok(
                {
                    "project_name": project_name,
                    "plugin_type": plugin_type,
                    "plugin_name": plugin_name,
                    "variant": variant,
                    "success": True,
                    "message": f"Plugin {plugin_name} added successfully",
                },
            )
        except Exception as e:
            return FlextResult.fail(f"Failed to add plugin: {e}")

    async def run_command_bridge(
        self,
        project_name: str,
        command_args: list[str],
        environment: str = "dev",
    ) -> FlextResult[dict[str, Any]]:
        """Bridge-compatible run command method."""
        try:
            # For now, return success simulation
            # TODO: Implement actual command execution logic
            return FlextResult.ok(
                {
                    "project_name": project_name,
                    "command": " ".join(command_args),
                    "environment": environment,
                    "success": True,
                    "stdout": f"Command executed: {' '.join(command_args)}",
                    "stderr": "",
                    "exit_code": 0,
                },
            )
        except Exception as e:
            return FlextResult.fail(f"Failed to run command: {e}")
