#!/usr/bin/env python3
"""FLEXT Meltano - Fixed Systematic Helper Application.

Script que aplica correções de lint restantes de forma manual e precisa.
"""

from __future__ import annotations

import re
from pathlib import Path


def fix_remaining_errors() -> None:
    """Fix remaining lint errors manually."""
    project_root = Path.cwd()

    # Fix PT017 in test_real_functionality.py
    test_file = project_root / "tests/test_real_functionality.py"
    if test_file.exists():
      content = test_file.read_text()

      # Fix PT017: pytest.fixture() with empty parentheses
      content = re.sub(r"@pytest\.fixture\(\)", "@pytest.fixture", content)

      test_file.write_text(content)
      print("✅ Fixed PT017 in test_real_functionality.py")

    # Fix import order issues in core_patterns.py
    core_file = project_root / "src/flext_meltano/core_patterns.py"
    if core_file.exists():
      content = core_file.read_text()

      # Fix import order - move from __future__ import to top
      lines = content.split("\n")

      # Find and remove misplaced from __future__ import
      future_import = None
      boilerplate_import = None

      new_lines = []
      for line in lines:
          if (
              line.startswith("from __future__ import annotations")
              and len(new_lines) > 1
          ):
              future_import = line
              continue
          if line.startswith(
              "from flext_meltano.helpers.boilerplate_reducers import",
          ):
              boilerplate_import = line
              continue
          new_lines.append(line)

      # Reconstruct with proper order
      if future_import and boilerplate_import:
          final_lines = [
              new_lines[0],
              "",
              future_import,
              boilerplate_import,
              *new_lines[1:],
          ]
          core_file.write_text("\n".join(final_lines))
          print("✅ Fixed import order in core_patterns.py")

    # Fix similar issues in other files
    files_to_fix = [
      "src/flext_meltano/production_decorators.py",
      "src/flext_meltano/patterns.py",
      "src/flext_meltano/real_singer_integration.py",
      "src/flext_meltano/orchestration/client-b/orchestrator.py",
      "src/flext_meltano/decorators.py",
      "examples/code_reduction_examples.py",
      "src/flext_meltano/flext_meltano_ultra_helpers.py",
      "tests/test_real_functionality.py",
    ]

    for file_path_str in files_to_fix:
      file_path = project_root / file_path_str
      if not file_path.exists():
          continue

      content = file_path.read_text()

      # Fix import order - ensure from __future__ import is first
      lines = content.split("\n")

      # Find docstring end
      docstring_end = 0
      in_docstring = False
      for i, line in enumerate(lines):
          if '"""' in line:
              if not in_docstring:
                  in_docstring = True
              else:
                  docstring_end = i
                  break

      # Find all imports
      future_imports = []
      boilerplate_imports = []
      other_imports = []
      non_import_lines = []

      for i, line in enumerate(lines):
          if i <= docstring_end:
              non_import_lines.append(line)
          elif line.startswith("from __future__ import"):
              future_imports.append(line)
          elif "boilerplate_reducers import" in line:
              boilerplate_imports.append(line)
          elif line.startswith(("import ", "from ")) and not line.startswith(
              "from __future__",
          ):
              other_imports.append(line)
          else:
              non_import_lines.append(line)

      # Reconstruct with proper order
      if future_imports or boilerplate_imports:
          new_lines = []
          new_lines.extend(non_import_lines[: docstring_end + 1,])
          new_lines.append("")
          new_lines.extend(future_imports)
          new_lines.extend(boilerplate_imports)
          new_lines.extend(other_imports)
          new_lines.extend(non_import_lines[docstring_end + 1 :,])

          # Clean up empty lines
          cleaned_lines = []
          prev_empty = False
          for line in new_lines:
              if line.strip() == "":
                  if not prev_empty:
                      cleaned_lines.append(line)
                      prev_empty = True
              else:
                  cleaned_lines.append(line)
                  prev_empty = False

          file_path.write_text("\n".join(cleaned_lines))
          if content != "\n".join(cleaned_lines):
              print(f"✅ Fixed imports in {(file_path_str,)}")


if __name__ == "__main__":
    print("🔧 Fixing remaining lint errors...")
    fix_remaining_errors()
    print("✅ Manual fixes complete!")
    print("\n🧪 Run: make lint to verify fixes")
