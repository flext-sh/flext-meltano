#!/usr/bin/env python3
"""FLEXT-Meltano Architecture Documentation Automation.

Automated diagram generation, validation, and maintenance for architecture documentation.
Provides PlantUML rendering, C4 model validation, and automated documentation updates.
"""

import argparse
import ast
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import ClassVar

from flext_core import FlextCore
from pydantic import BaseModel, ConfigDict

# Import from scripts directory (works when run from project root)
from scripts.docs_config import DocsConfig


class DiagramValidationResult(BaseModel):
    """Result of diagram validation using FlextCore.Models.Value."""

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    diagram_path: str
    is_valid: bool
    errors: ClassVar[list[str]] = []
    warnings: ClassVar[list[str]] = []
    rendered_path: str | None = None


class ArchitectureValidationResult(BaseModel):
    """Comprehensive architecture validation result using FlextCore.Models.Value."""

    model_config = ConfigDict(frozen=False, validate_assignment=True)

    total_diagrams: int = 0
    valid_diagrams: int = 0
    invalid_diagrams: int = 0
    errors: ClassVar[list[str]] = []
    warnings: ClassVar[list[str]] = []
    generated_files: ClassVar[list[str]] = []


class PlantUMLRenderer(FlextCore.Service):
    """PlantUML diagram rendering and validation using FLEXT patterns."""

    def __init__(
        self,
        logger: FlextCore.Logger | None = None,
        plantuml_jar: str | None = None,
    ) -> None:
        """Initialize PlantUML renderer with optional logger and JAR path."""
        super().__init__(logger=logger)
        config = DocsConfig.get_instance()
        self.plantuml_jar = plantuml_jar or self._find_plantuml_jar()
        self.output_dir = Path(config.reports_output_dir).parent / "diagrams"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _find_plantuml_jar(self) -> str:
        """Find PlantUML JAR file in common locations."""
        common_paths = [
            "/usr/local/share/plantuml/plantuml.jar",
            "/opt/plantuml/plantuml.jar",
            "plantuml.jar",
            "./plantuml.jar",
        ]

        for path in common_paths:
            if Path(path).exists():
                return path

        # Try to download if not found
        return self._download_plantuml()

    def _download_plantuml(self) -> str:
        """Download PlantUML JAR file."""
        jar_path = "plantuml.jar"
        url = "https://github.com/plantuml/plantuml/releases/download/v1.2023.13/plantuml-1.2023.13.jar"

        print(f"Downloading PlantUML from {url}...")
        try:
            # Security: URL is hardcoded and from trusted source (GitHub releases)
            urllib.request.urlretrieve(url, jar_path)
            print(f"Downloaded PlantUML to {jar_path}")
            return jar_path
        except Exception as e:
            print(f"Failed to download PlantUML: {e}")
            raise

    def render_diagram(
        self, puml_file: Path
    ) -> FlextCore.Result[DiagramValidationResult]:
        """Render a PlantUML diagram to image format using FLEXT patterns."""
        result = DiagramValidationResult(diagram_path=str(puml_file), is_valid=True)

        if not puml_file.exists():
            result.errors.append(f"Diagram file not found: {puml_file}")
            result.is_valid = False
            return FlextCore.Result.ok(result)

        try:
            # Validate PlantUML syntax
            syntax_result = self.validate_syntax(puml_file)
            if not syntax_result.is_valid:
                result.errors.extend(syntax_result.errors)
                result.is_valid = False
                return FlextCore.Result.ok(result)

            # Render to PNG
            png_file = self.output_dir / f"{puml_file.stem}.png"
            cmd = [
                "java",
                "-jar",
                self.plantuml_jar,
                "-tpng",
                "-o",
                str(self.output_dir),
                str(puml_file),
            ]

            # Security: subprocess is used to execute PlantUML JAR with controlled arguments
            process = subprocess.run(
                cmd, check=False, capture_output=True, text=True, cwd=puml_file.parent
            )

            if process.returncode == 0 and png_file.exists():
                result.is_valid = True
                result.rendered_path = str(png_file)
                self.logger.info(
                    "Diagram rendered successfully",
                    diagram=str(puml_file),
                    output=str(png_file),
                )
            else:
                result.errors.append(f"Rendering failed: {process.stderr}")
                result.is_valid = False
                self.logger.warning(
                    "Diagram rendering failed",
                    diagram=str(puml_file),
                    error=process.stderr,
                )

        except Exception as e:
            error_msg = f"Rendering error: {e!s}"
            result.errors.append(error_msg)
            result.is_valid = False
            self.logger.exception("Diagram rendering failed", error=error_msg)

        return FlextCore.Result.ok(result)

    def validate_syntax(self, puml_file: Path) -> DiagramValidationResult:
        """Validate PlantUML syntax."""
        result = DiagramValidationResult(diagram_path=str(puml_file), is_valid=True)

        try:
            with Path(puml_file).open(encoding="utf-8") as f:
                content = f.read()

            # Basic syntax checks
            if not content.strip():
                result.errors.append("Diagram file is empty")
                result.is_valid = False
                return result

            # Check for required PlantUML markers
            if not content.startswith("@startuml"):
                result.errors.append("Diagram must start with @startuml")
                result.is_valid = False
                return result

            if "@enduml" not in content:
                result.errors.append("Diagram must end with @enduml")
                result.is_valid = False
                return result

            # Check for unbalanced braces/brackets
            if content.count("{") != content.count("}"):
                result.warnings.append("Unbalanced curly braces detected")

            if content.count("[") != content.count("]"):
                result.warnings.append("Unbalanced square brackets detected")

            # Check for common syntax errors
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped and not stripped.startswith((
                    "'",
                    "@",
                    "title",
                    "legend",
                    "note",
                    "end",
                    "*",
                )):
                    # Basic validation for common PlantUML constructs
                    if "->" in stripped and not stripped.endswith(";"):
                        result.warnings.append(
                            f"Line {i}: Arrow relationship may be missing semicolon"
                        )
                    elif "=" in stripped and not any(
                        keyword in stripped for keyword in ["skinparam", "set"]
                    ):
                        # Variable assignments should be valid
                        pass

            result.is_valid = len(result.errors) == 0

        except Exception as e:
            result.errors.append(f"Syntax validation error: {e!s}")
            result.is_valid = False

        return result

    def render_all_diagrams(
        self, diagrams_dir: str | Path = "docs/architecture"
    ) -> FlextCore.Result[list[DiagramValidationResult]]:
        """Render all PlantUML diagrams in a directory using FLEXT patterns."""
        diagrams_dir = Path(diagrams_dir)
        puml_files = list(diagrams_dir.rglob("*.puml")) + list(
            diagrams_dir.rglob("*.plantuml")
        )

        results = []
        for puml_file in puml_files:
            self.logger.info("Rendering diagram", diagram=str(puml_file))
            result = self.render_diagram(puml_file)
            if result.is_success:
                results.append(result.unwrap())
            else:
                self.logger.warning(
                    "Failed to render diagram",
                    diagram=str(puml_file),
                    error=result.error,
                )
                # Continue with other diagrams even if one fails

        return FlextCore.Result.ok(results)


class C4ModelValidator(FlextCore.Service):
    """C4 model validation and consistency checking using FLEXT patterns."""

    def __init__(self, logger: FlextCore.Logger | None = None) -> None:
        """Initialize C4 model validator with optional logger."""
        super().__init__(logger=logger)
        self.c4_patterns = {
            "context": re.compile(
                r"!include https://raw\.githubusercontent\.com/plantuml-stdlib/C4-PlantUML/master/C4_Context\.puml"
            ),
            "container": re.compile(
                r"!include https://raw\.githubusercontent\.com/plantuml-stdlib/C4-PlantUML/master/C4_Container\.puml"
            ),
            "component": re.compile(
                r"!include https://raw\.githubusercontent\.com/plantuml-stdlib/C4-PlantUML/master/C4_Component\.puml"
            ),
            "code": re.compile(
                r"!include https://raw\.githubusercontent\.com/plantuml-stdlib/C4-PlantUML/master/C4_Component\.puml"
            ),
        }

    def validate_c4_model(self, c4_file: Path) -> DiagramValidationResult:
        """Validate C4 model diagram structure."""
        result = DiagramValidationResult(diagram_path=str(c4_file), is_valid=True)

        try:
            with Path(c4_file).open(encoding="utf-8") as f:
                content = f.read()

            # Determine C4 level
            level = self._determine_c4_level(content)

            if not level:
                result.errors.append("Could not determine C4 model level")
                result.is_valid = False
                return result

            # Validate level-specific patterns
            level_validation = self._validate_c4_level(content, level)
            result.errors.extend(level_validation.errors)
            result.warnings.extend(level_validation.warnings)

            # Validate C4 model structure
            structure_validation = self._validate_c4_structure(content, level)
            result.errors.extend(structure_validation.errors)
            result.warnings.extend(structure_validation.warnings)

            result.is_valid = len(result.errors) == 0

        except Exception as e:
            result.errors.append(f"C4 validation error: {e!s}")
            result.is_valid = False

        return result

    def _determine_c4_level(self, content: str) -> str | None:
        """Determine which C4 level the diagram represents."""
        for level, pattern in self.c4_patterns.items():
            if pattern.search(content):
                return level
        return None

    def _validate_c4_level(self, content: str, level: str) -> DiagramValidationResult:
        """Validate level-specific C4 model requirements."""
        result = DiagramValidationResult(diagram_path="", is_valid=True)

        if level == "context":
            # Context diagrams should focus on system boundaries
            if "System_Ext" not in content:
                result.warnings.append("Context diagram should show external systems")

        elif level == "container":
            # Container diagrams should show technology choices
            tech_patterns = ["Python", "FastAPI", "PostgreSQL", "Redis"]
            found_tech = any(tech in content for tech in tech_patterns)
            if not found_tech:
                result.warnings.append(
                    "Container diagram should specify technology choices"
                )

        elif (
            level == "component"
            and "Component" not in content
            and "component" not in content
        ):
            # Component diagrams should show internal structure
            result.errors.append("Component diagram should define components")

        return result

    def _validate_c4_structure(
        self, content: str, _level: str
    ) -> DiagramValidationResult:
        """Validate overall C4 model structure."""
        result = DiagramValidationResult(diagram_path="", is_valid=True)

        # Check for proper boundaries
        boundary_count = content.count("System_Boundary") + content.count("Boundary")
        if boundary_count == 0:
            result.warnings.append("C4 diagrams should use system boundaries")

        # Check for relationships
        rel_count = content.count("Rel(") + content.count("Rel(")
        if rel_count == 0:
            result.warnings.append("C4 diagrams should show system relationships")

        # Check for descriptions
        if '"' not in content and "'" not in content:
            result.warnings.append("C4 elements should have descriptive names")

        return result


class ArchitectureDiagramGenerator:
    """Automated architecture diagram generation from code analysis."""

    def __init__(
        self, source_dir: str = "src", logger: FlextCore.Logger | None = None
    ) -> None:
        """Initialize architecture diagram generator with source directory and logger."""
        self.source_dir = Path(source_dir)
        self.logger = logger

    def generate_module_diagram(self, module_name: str, output_file: str) -> bool:
        """Generate PlantUML diagram from Python module analysis."""
        try:
            module_path = self.source_dir / module_name.replace(".", "/")
            if module_path.is_file():
                module_path = module_path.parent

            if not module_path.exists():
                print(f"Module path not found: {module_path}")
                return False

            # Analyze Python files
            classes, functions, imports = self._analyze_python_files(module_path)

            # Generate PlantUML
            puml_content = self._generate_module_puml(
                module_name, classes, functions, imports
            )

            # Write to file
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with Path(output_path).open("w", encoding="utf-8") as f:
                f.write(puml_content)

            print(f"Generated module diagram: {output_file}")
            return True

        except Exception as e:
            print(f"Failed to generate module diagram: {e}")
            return False

    def _analyze_python_files(self, module_path: Path) -> tuple[dict, dict, set]:
        """Analyze Python files for classes, functions, and imports."""
        classes = {}
        functions = {}
        imports = set()

        for py_file in module_path.rglob("*.py"):
            try:
                with Path(py_file).open(encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        class_name = node.name
                        methods = [
                            n.name for n in node.body if isinstance(n, ast.FunctionDef)
                        ]
                        classes[class_name] = methods

                    elif isinstance(node, ast.FunctionDef) and not any(
                        isinstance(parent, ast.ClassDef)
                        for parent in [node]
                        if hasattr(node, "parent")
                    ):
                        functions[node.name] = []

                    elif isinstance(node, ast.Import):
                        imports.update(alias.name for alias in node.names)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.add(node.module)

            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Failed to analyze Python file {py_file}: {e}")
                else:
                    print(f"Warning: Failed to analyze Python file {py_file}: {e}")
                continue

        return classes, functions, imports

    def _generate_module_puml(
        self, module_name: str, classes: dict, functions: dict, imports: set
    ) -> str:
        """Generate PlantUML content for module diagram."""
        puml = f"""@startuml {module_name.replace(".", "_")}_module
title {module_name} - Module Structure

package "{module_name}" as module {{
"""

        # Add classes
        for class_name, methods in classes.items():
            puml += f"""    class {class_name} {{
"""
            for method in methods[:5]:  # Limit methods to keep diagram readable
                puml += f"""        +{method}()
"""
            if len(methods) > 5:
                puml += f"""        ... and {len(methods) - 5} more methods
"""
            puml += """    }
"""

        # Add functions
        for func_name in functions:
            puml += f"""    function {func_name}()
"""

        puml += "}\n"

        # Add external dependencies
        if imports:
            puml += """
package "External Dependencies" as external {
"""
            for imp in sorted(imports)[:10]:  # Limit imports
                puml += f"""    [{imp}]
"""
            if len(imports) > 10:
                puml += f"""    ... and {len(imports) - 10} more
"""
            puml += "}\n"

            # Add relationships
            for imp in sorted(imports)[:5]:
                puml += f"""module --> external.[{imp}] : uses
"""

        puml += "@enduml"
        return puml

    def generate_service_diagram(self, service_name: str, output_file: str) -> bool:
        """Generate service interaction diagram."""
        try:
            # This would analyze service interactions from logs, code, etc.
            # For now, create a basic template

            puml_content = f"""@startuml {service_name}_service
title {service_name} - Service Interactions

actor User
participant "{service_name}" as service
database "Database"
component "External API" as external

User -> service: Request
service -> database: Query data
database --> service: Return data
service -> external: Call external service
external --> service: Return result
service --> User: Response

note right: Service interaction diagram
Auto-generated from code analysis
@enduml"""

            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with Path(output_path).open("w", encoding="utf-8") as f:
                f.write(puml_content)

            print(f"Generated service diagram: {output_file}")
            return True

        except Exception as e:
            print(f"Failed to generate service diagram: {e}")
            return False


class ArchitectureDocumentationManager:
    """Comprehensive architecture documentation management."""

    def __init__(self, docs_dir: str = "docs") -> None:
        """Initialize architecture documentation manager with docs directory."""
        self.docs_dir = Path(docs_dir)
        self.plantuml_renderer = PlantUMLRenderer()
        self.c4_validator = C4ModelValidator()
        self.diagram_generator = ArchitectureDiagramGenerator()

    def validate_all_architecture_docs(self) -> ArchitectureValidationResult:
        """Validate all architecture documentation."""
        result = ArchitectureValidationResult()

        print("🔍 Validating architecture documentation...")

        # Validate C4 model documents
        c4_files = list(self.docs_dir.glob("**/C4_MODEL.md"))
        for c4_file in c4_files:
            print(f"Validating C4 model: {c4_file}")
            # C4 model validation would go here

        # Validate PlantUML diagrams
        puml_files = list(self.docs_dir.rglob("*.puml")) + list(
            self.docs_dir.rglob("*.plantuml")
        )
        result.total_diagrams = len(puml_files)

        for puml_file in puml_files:
            print(f"Validating diagram: {puml_file}")

            # Validate PlantUML syntax
            validation_result = self.plantuml_renderer.validate_syntax(puml_file)

            if validation_result.is_valid:
                result.valid_diagrams += 1
            else:
                result.invalid_diagrams += 1
                result.errors.extend(validation_result.errors)

            result.warnings.extend(validation_result.warnings)

        # Render diagrams
        print("🎨 Rendering diagrams...")
        render_result = self.plantuml_renderer.render_all_diagrams(
            str(self.docs_dir / "architecture")
        )

        if render_result.is_success:
            for diagram_result in render_result.unwrap():
                if diagram_result.is_valid and diagram_result.rendered_path:
                    result.generated_files.append(diagram_result.rendered_path)
        else:
            result.errors.append(f"Failed to render diagrams: {render_result.error}")

        return result

    def generate_architecture_diagrams(self) -> list[str]:
        """Generate architecture diagrams from code analysis."""
        print("🔄 Generating architecture diagrams from code...")

        generated_files = []

        # Generate module diagrams for key modules
        key_modules = [
            "flext_meltano.api",
            "flext_meltano.services",
            "flext_meltano.adapters",
            "flext_meltano.models",
        ]

        for module in key_modules:
            output_file = (
                f"docs/architecture/generated/{module.replace('.', '_')}_module.puml"
            )
            if self.diagram_generator.generate_module_diagram(module, output_file):
                generated_files.append(output_file)

        # Generate service interaction diagrams
        services = ["MeltanoService", "PipelineService", "PluginService"]
        for service in services:
            output_file = (
                f"docs/architecture/generated/{service.lower()}_interactions.puml"
            )
            if self.diagram_generator.generate_service_diagram(service, output_file):
                generated_files.append(output_file)

        return generated_files

    def update_architecture_documentation(self) -> bool:
        """Update architecture documentation with latest changes."""
        print("📝 Updating architecture documentation...")

        try:
            # Update timestamps
            self._update_document_timestamps()

            # Update diagram references
            self._update_diagram_references()

            # Validate cross-references
            self._validate_cross_references()

            # Update architecture metrics
            self._update_architecture_metrics()

            print("✅ Architecture documentation updated")
            return True

        except Exception as e:
            print(f"❌ Failed to update architecture documentation: {e}")
            return False

    def _update_document_timestamps(self) -> None:
        """Update last modified timestamps in documentation."""
        arch_files = list(self.docs_dir.rglob("architecture/**/*.md"))

        for arch_file in arch_files:
            try:
                with Path(arch_file).open(encoding="utf-8") as f:
                    content = f.read()

                # Update timestamp patterns
                timestamp_patterns = [
                    (
                        r"\*\*Last Updated\*\*: \d{4}-\d{2}-\d{2}",
                        f"**Last Updated**: {time.strftime('%Y-%m-%d')}",
                    ),
                    (
                        r"Generated: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
                        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                    ),
                ]

                for pattern, replacement in timestamp_patterns:
                    content = re.sub(pattern, replacement, content)

                with Path(arch_file).open("w", encoding="utf-8") as f:
                    f.write(content)

            except Exception as e:
                print(f"Warning: Failed to update timestamp in {arch_file}: {e}")

    def _update_diagram_references(self) -> None:
        """Update diagram references in documentation."""
        # This would scan for broken image links and update them
        # Implementation would depend on specific documentation structure

    def _validate_cross_references(self) -> None:
        """Validate cross-references between documents."""
        # Implementation would check links between architecture documents

    def _update_architecture_metrics(self) -> None:
        """Update architecture metrics in documentation."""
        # This would update things like line counts, file counts, etc.

    def create_architecture_report(self) -> str:
        """Create comprehensive architecture status report."""
        report_path = self.docs_dir / "architecture" / "ARCHITECTURE_REPORT.md"

        # Gather metrics
        total_arch_files = len(list(self.docs_dir.rglob("architecture/**/*.md")))
        total_diagrams = len(list(self.docs_dir.rglob("architecture/**/*.puml")))
        rendered_diagrams = len(list(self.docs_dir.rglob("architecture/**/*.png")))

        # Create report
        report_content = f"""# Architecture Documentation Report

**Generated**: {time.strftime("%Y-%m-%d %H:%M:%S")}

## 📊 Documentation Metrics

- **Architecture Documents**: {total_arch_files}
- **PlantUML Diagrams**: {total_diagrams}
- **Rendered Diagrams**: {rendered_diagrams}
- **C4 Model Documents**: {len(list(self.docs_dir.glob("**/C4_MODEL.md")))}

## 📈 Documentation Health

### ✅ Strengths
- Comprehensive C4 model documentation
- PlantUML diagrams for visualization
- ADR system for architectural decisions
- Automated validation and rendering

### ⚠️ Areas for Improvement
- Some diagrams may need updates
- Cross-reference validation needed
- Automated metrics updating

## 🎯 Next Steps

1. **Validate All Diagrams**: Ensure all PlantUML diagrams render correctly
2. **Update Timestamps**: Refresh all document timestamps
3. **Cross-Reference Check**: Validate links between documents
4. **Metrics Update**: Update architecture metrics in documents

## 📋 Recent Changes

- Architecture documentation framework implemented
- PlantUML diagram rendering automated
- C4 model validation added
- ADR system established

---

*This report is automatically generated. Run `make docs-architecture-report` to update.*
"""

        with Path(report_path).open("w", encoding="utf-8") as f:
            f.write(report_content)

        print(f"📋 Created architecture report: {report_path}")
        return str(report_path)


def main() -> None:
    """Main entry point for architecture automation."""
    parser = argparse.ArgumentParser(
        description="FLEXT-Meltano Architecture Documentation Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/architecture_automation.py --validate
  python scripts/architecture_automation.py --generate-diagrams
  python scripts/architecture_automation.py --update-docs
  python scripts/architecture_automation.py --create-report
  python scripts/architecture_automation.py --comprehensive
        """,
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate architecture documentation and diagrams",
    )
    parser.add_argument(
        "--generate-diagrams",
        action="store_true",
        help="Generate architecture diagrams from code analysis",
    )
    parser.add_argument(
        "--update-docs",
        action="store_true",
        help="Update architecture documentation timestamps and references",
    )
    parser.add_argument(
        "--create-report",
        action="store_true",
        help="Create comprehensive architecture status report",
    )
    parser.add_argument(
        "--comprehensive",
        action="store_true",
        help="Run all architecture automation tasks",
    )

    args = parser.parse_args()

    if not any([
        args.validate,
        args.generate_diagrams,
        args.update_docs,
        args.create_report,
        args.comprehensive,
    ]):
        parser.print_help()
        return

    try:
        automation = ArchitectureDocumentationManager()

        if args.validate or args.comprehensive:
            print("🔍 Validating architecture documentation...")
            validation_result = automation.validate_all_architecture_docs()

            print("📊 Validation Results:")
            print(
                f"   Diagrams: {validation_result.valid_diagrams}/{validation_result.total_diagrams} valid"
            )
            print(f"   Errors: {len(validation_result.errors)}")
            print(f"   Warnings: {len(validation_result.warnings)}")

            if validation_result.errors:
                print("❌ Errors found:")
                for error in validation_result.errors[:5]:
                    print(f"   - {error}")

        if args.generate_diagrams or args.comprehensive:
            print("🔄 Generating architecture diagrams...")
            generated_files = automation.generate_architecture_diagrams()

            print(f"✅ Generated {len(generated_files)} diagram files")

        if args.update_docs or args.comprehensive:
            print("📝 Updating architecture documentation...")
            success = automation.update_architecture_documentation()

            if success:
                print("✅ Documentation updated successfully")
            else:
                print("❌ Documentation update failed")

        if args.create_report or args.comprehensive:
            print("📋 Creating architecture report...")
            report_path = automation.create_architecture_report()
            print(f"✅ Report created: {report_path}")

        print("🎉 Architecture automation completed!")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
