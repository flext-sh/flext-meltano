#!/usr/bin/env python3
"""
FLEXT-Meltano Documentation Automation Framework

Automated scheduling, CI/CD integration, and continuous maintenance
for documentation quality assurance.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, time
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
import schedule
import time as time_module


class DocumentationAutomation:
    """Automated documentation maintenance and CI/CD integration."""

    def __init__(self, config_path: str = "docs/.maintenance_config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.maintenance_script = Path("scripts/docs_maintenance.py")

        # Ensure maintenance script exists
        if not self.maintenance_script.exists():
            raise FileNotFoundError(f"Maintenance script not found: {self.maintenance_script}")

    def _load_config(self) -> Dict[str, Any]:
        """Load automation configuration."""
        if not self.config_path.exists():
            # Return default configuration
            return {
                'automation': {
                    'enable_scheduled_audits': True,
                    'audit_schedule': 'weekly',
                    'audit_day': 'monday',
                    'audit_time': '09:00'
                },
                'reporting': {
                    'output_directory': 'docs/reports'
                }
            }

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def run_ci_checks(self) -> bool:
        """Run documentation quality checks for CI/CD pipeline."""
        print("🔍 Running CI documentation quality checks...")

        try:
            # Run comprehensive audit
            result = subprocess.run([
                sys.executable, str(self.maintenance_script), '--comprehensive'
            ], capture_output=True, text=True, cwd=Path.cwd())

            if result.returncode != 0:
                print(f"❌ Documentation audit failed: {result.stderr}")
                return False

            # Check quality thresholds
            summary_path = Path(self.config['reporting']['output_directory']) / "docs_quality_summary.json"
            if summary_path.exists():
                with open(summary_path, 'r', encoding='utf-8') as f:
                    summary = json.load(f)

                quality_score = summary.get('quality_score', 0)
                issues = summary.get('issues', {})

                # Check critical issues
                critical_count = issues.get('by_severity', {}).get('critical', 0)
                if critical_count > 0 and self.config.get('automation', {}).get('fail_on_critical_issues', True):
                    print(f"❌ Critical documentation issues found: {critical_count}")
                    return False

                # Check quality score threshold
                min_score = self.config.get('quality_thresholds', {}).get('min_quality_score', 80)
                if quality_score < min_score:
                    print(f"❌ Quality score below threshold: {quality_score} < {min_score}")
                    return False

                print(f"✅ Quality checks passed (Score: {quality_score})")
                return True
            else:
                print("⚠️  Quality summary not generated")
                return False

        except Exception as e:
            print(f"❌ CI check failed: {e}")
            return False

    def schedule_maintenance(self) -> None:
        """Set up scheduled maintenance tasks."""
        automation_config = self.config.get('automation', {})

        if not automation_config.get('enable_scheduled_audits', False):
            print("📅 Scheduled audits disabled in configuration")
            return

        schedule_type = automation_config.get('audit_schedule', 'weekly')

        if schedule_type == 'daily':
            self._schedule_daily(automation_config)
        elif schedule_type == 'weekly':
            self._schedule_weekly(automation_config)
        elif schedule_type == 'monthly':
            self._schedule_monthly(automation_config)

        print("📅 Maintenance scheduling configured")

    def _schedule_daily(self, config: Dict[str, Any]) -> None:
        """Schedule daily maintenance."""
        audit_time = config.get('audit_time', '09:00')
        hour, minute = map(int, audit_time.split(':'))

        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(self._run_scheduled_audit)

    def _schedule_weekly(self, config: Dict[str, Any]) -> None:
        """Schedule weekly maintenance."""
        audit_day = config.get('audit_day', 'monday').lower()
        audit_time = config.get('audit_time', '09:00')
        hour, minute = map(int, audit_time.split(':'))

        # Map day names to schedule methods
        day_methods = {
            'monday': schedule.every().monday,
            'tuesday': schedule.every().tuesday,
            'wednesday': schedule.every().wednesday,
            'thursday': schedule.every().thursday,
            'friday': schedule.every().friday,
            'saturday': schedule.every().saturday,
            'sunday': schedule.every().sunday
        }

        if audit_day in day_methods:
            day_methods[audit_day].at(f"{hour:02d}:{minute:02d}").do(self._run_scheduled_audit)

    def _schedule_monthly(self, config: Dict[str, Any]) -> None:
        """Schedule monthly maintenance."""
        # Run on the 1st of each month
        audit_time = config.get('audit_time', '09:00')
        hour, minute = map(int, audit_time.split(':'))

        schedule.every().month.at(f"{hour:02d}:{minute:02d}").do(self._run_scheduled_audit)

    def _run_scheduled_audit(self) -> None:
        """Run scheduled documentation audit."""
        print(f"📅 Running scheduled documentation audit at {datetime.now()}")

        try:
            result = subprocess.run([
                sys.executable, str(self.maintenance_script), '--comprehensive'
            ], capture_output=True, text=True, cwd=Path.cwd())

            if result.returncode == 0:
                print("✅ Scheduled audit completed successfully")
            else:
                print(f"⚠️  Scheduled audit completed with warnings: {result.stderr}")

        except Exception as e:
            print(f"❌ Scheduled audit failed: {e}")

    def run_continuous_monitoring(self) -> None:
        """Run continuous monitoring loop."""
        print("🔄 Starting continuous documentation monitoring...")

        self.schedule_maintenance()

        try:
            while True:
                schedule.run_pending()
                time_module.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("⏹️  Continuous monitoring stopped")

    def generate_ci_workflow(self) -> str:
        """Generate GitHub Actions workflow for documentation quality."""
        workflow = f"""# Documentation Quality CI/CD Pipeline
# Generated by FLEXT-Meltano Documentation Maintenance Framework
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

name: Documentation Quality

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'docs/**'
      - '**.md'
      - 'scripts/docs_maintenance.py'
  pull_request:
    branches: [ main, develop ]
    paths:
      - 'docs/**'
      - '**.md'
      - 'scripts/docs_maintenance.py'
  schedule:
    # Run weekly audit on {self.config.get('automation', {}).get('audit_day', 'monday')} at {self.config.get('automation', {}).get('audit_time', '09:00')} UTC
    - cron: '{self._get_cron_schedule()}'

jobs:
  docs-quality-check:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install PyYAML requests

    - name: Run documentation quality audit
      run: python scripts/docs_maintenance.py --comprehensive

    - name: Check quality thresholds
      run: python scripts/docs_automation.py --ci-check

    - name: Upload quality reports
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: docs-quality-reports
        path: docs/reports/

    - name: Comment PR with quality report
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v7
      with:
        script: |
          const fs = require('fs');
          const path = require('path');

          // Read the quality summary
          const summaryPath = path.join(process.cwd(), 'docs/reports/docs_quality_summary.json');
          if (fs.existsSync(summaryPath)) {{
            const summary = JSON.parse(fs.readFileSync(summaryPath, 'utf8'));

            const qualityScore = summary.quality_score;
            const totalIssues = summary.issues.total;

            const body = `
            ## 📊 Documentation Quality Report

            **Quality Score:** ${{qualityScore}}/100
            **Total Issues:** ${{totalIssues}}

            ### Details
            - Files: ${{summary.metrics.total_files}}
            - Words: ${{summary.metrics.total_words.toLocaleString()}}
            - Links: ${{summary.metrics.total_links}}

            [View detailed report](https://github.com/${{github.repository}}/actions/runs/${{github.run_id}})
            `;

            github.rest.issues.createComment({{
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            }});
          }}
"""
        return workflow

    def _get_cron_schedule(self) -> str:
        """Convert audit schedule to cron format."""
        automation_config = self.config.get('automation', {})
        audit_day = automation_config.get('audit_day', 'monday').lower()
        audit_time = automation_config.get('audit_time', '09:00')

        hour, minute = map(int, audit_time.split(':'))

        # Day mapping for cron (0=Sunday, 1=Monday, etc.)
        day_map = {
            'sunday': 0,
            'monday': 1,
            'tuesday': 2,
            'wednesday': 3,
            'thursday': 4,
            'friday': 5,
            'saturday': 6
        }

        day_num = day_map.get(audit_day, 1)  # Default to Monday

        return f"{minute} {hour} * * {day_num}"

    def create_maintenance_hook(self) -> str:
        """Create Git pre-commit hook for documentation quality."""
        hook_content = """#!/bin/bash
# FLEXT-Meltano Documentation Quality Pre-commit Hook
# Generated by Documentation Maintenance Framework

echo "🔍 Running documentation quality checks..."

# Run documentation audit
python scripts/docs_maintenance.py --audit

# Check if audit passed
if [ $? -ne 0 ]; then
    echo "❌ Documentation quality check failed. Please fix issues before committing."
    echo "Run 'python scripts/docs_maintenance.py --comprehensive' for detailed report."
    exit 1
fi

# Check for critical issues
if [ -f "docs/reports/docs_quality_summary.json" ]; then
    CRITICAL_ISSUES=$(python -c "
import json
with open('docs/reports/docs_quality_summary.json', 'r') as f:
    data = json.load(f)
    print(data.get('issues', {}).get('by_severity', {}).get('critical', 0))
")

    if [ "$CRITICAL_ISSUES" -gt 0 ]; then
        echo "❌ Critical documentation issues found: $CRITICAL_ISSUES"
        echo "Please fix critical issues before committing."
        exit 1
    fi
fi

echo "✅ Documentation quality checks passed"
exit 0
"""
        return hook_content

    def setup_git_hooks(self) -> None:
        """Set up Git hooks for documentation quality."""
        hooks_dir = Path(".git/hooks")
        if not hooks_dir.exists():
            print("⚠️  Git hooks directory not found. Initialize git repository first.")
            return

        pre_commit_hook = hooks_dir / "pre-commit"

        # Backup existing hook if it exists
        if pre_commit_hook.exists():
            backup_hook = hooks_dir / "pre-commit.backup"
            if not backup_hook.exists():
                pre_commit_hook.rename(backup_hook)
                print(f"📋 Backed up existing pre-commit hook to {backup_hook}")

        # Create new hook
        hook_content = self.create_maintenance_hook()
        pre_commit_hook.write_text(hook_content)
        pre_commit_hook.chmod(0o755)

        print(f"✅ Documentation quality pre-commit hook installed: {pre_commit_hook}")

    def create_makefile_targets(self) -> str:
        """Create Makefile targets for documentation maintenance."""
        makefile_content = """
# Documentation Maintenance Targets
# Generated by FLEXT-Meltano Documentation Maintenance Framework

.PHONY: docs-audit docs-validate docs-report docs-comprehensive docs-ci-check docs-schedule docs-hooks

# Run documentation quality audit
docs-audit:
	@echo "🔍 Running documentation audit..."
	@python scripts/docs_maintenance.py --audit

# Validate external links
docs-validate:
	@echo "🔗 Validating external links..."
	@python scripts/docs_maintenance.py --validate

# Generate quality reports
docs-report:
	@echo "📊 Generating quality reports..."
	@python scripts/docs_maintenance.py --report

# Run comprehensive documentation maintenance
docs-comprehensive:
	@echo "🔄 Running comprehensive documentation maintenance..."
	@python scripts/docs_maintenance.py --comprehensive

# Run CI quality checks
docs-ci-check:
	@echo "🔍 Running CI documentation quality checks..."
	@python scripts/docs_automation.py --ci-check

# Start scheduled maintenance monitoring
docs-schedule:
	@echo "📅 Starting scheduled documentation maintenance..."
	@python scripts/docs_automation.py --schedule

# Set up Git hooks for quality checks
docs-hooks:
	@echo "🔧 Setting up Git hooks for documentation quality..."
	@python scripts/docs_automation.py --setup-hooks

# Generate GitHub Actions workflow
docs-workflow:
	@echo "⚙️  Generating GitHub Actions workflow..."
	@python scripts/docs_automation.py --generate-workflow > .github/workflows/docs-quality.yml
	@echo "✅ Workflow generated: .github/workflows/docs-quality.yml"

# View latest quality report
docs-view-report:
	@echo "📊 Latest Documentation Quality Report"
	@echo "======================================"
	@if [ -f "docs/reports/docs_quality_summary.json" ]; then \\
		python -c "\\
import json\\
with open('docs/reports/docs_quality_summary.json', 'r') as f:\\
    data = json.load(f)\\
    print(f'Quality Score: {data[\"quality_score\"]}/100')\\
    print(f'Total Issues: {data[\"issues\"][\"total\"]}')\\
    print(f'Files: {data[\"metrics\"][\"total_files\"]}')\\
    print(f'Words: {data[\"metrics\"][\"total_words\"]:,}')\\
    print(f'Links: {data[\"metrics\"][\"total_links\"]}')\\
"; \\
	else \\
		echo "No quality report found. Run 'make docs-comprehensive' first."; \\
	fi

# Clean up generated reports
docs-clean:
	@echo "🧹 Cleaning up documentation reports..."
	@rm -rf docs/reports/*
	@echo "✅ Reports cleaned"

# Full documentation maintenance setup
docs-setup: docs-hooks docs-workflow
	@echo "🚀 Documentation maintenance system setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Run 'make docs-comprehensive' to generate initial quality report"
	@echo "2. Review quality report in docs/reports/"
	@echo "3. Address high-priority issues"
	@echo "4. Commit changes to enable pre-commit hooks"
"""
        return makefile_content


def main():
    """Main entry point for documentation automation."""
    parser = argparse.ArgumentParser(
        description="FLEXT-Meltano Documentation Automation Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/docs_automation.py --ci-check
  python scripts/docs_automation.py --schedule
  python scripts/docs_automation.py --setup-hooks
  python scripts/docs_automation.py --generate-workflow
        """
    )

    parser.add_argument('--ci-check', action='store_true',
                       help='Run CI quality checks')
    parser.add_argument('--schedule', action='store_true',
                       help='Start scheduled maintenance monitoring')
    parser.add_argument('--setup-hooks', action='store_true',
                       help='Set up Git hooks for quality checks')
    parser.add_argument('--generate-workflow', action='store_true',
                       help='Generate GitHub Actions workflow')
    parser.add_argument('--generate-makefile', action='store_true',
                       help='Generate Makefile targets')
    parser.add_argument('--config', default='docs/.maintenance_config.yaml',
                       help='Path to configuration file')

    args = parser.parse_args()

    try:
        automation = DocumentationAutomation(args.config)

        if args.ci_check:
            success = automation.run_ci_checks()
            sys.exit(0 if success else 1)

        elif args.schedule:
            automation.run_continuous_monitoring()

        elif args.setup_hooks:
            automation.setup_git_hooks()

        elif args.generate_workflow:
            workflow = automation.generate_ci_workflow()
            print(workflow)

        elif args.generate_makefile:
            makefile = automation.create_makefile_targets()
            print(makefile)

        else:
            parser.print_help()

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()