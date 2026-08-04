# Documentation Maintenance Guide

<!-- TOC START -->
- [🎯 Overview](#overview)
- [🏗️ Architecture](#architecture)
  - [Core Components](#core-components)
  - [Key Features](#key-features)
- [🚀 Quick Start](#quick-start)
  - [1. Run Comprehensive Audit](#1-run-comprehensive-audit)
  - [2. View Quality Reports](#2-view-quality-reports)
  - [3. Set Up Quality Gates](#3-set-up-quality-gates)
- [📋 Quality Metrics](#quality-metrics)
  - [Overall Quality Score (0-100)](#overall-quality-score-0-100)
  - [Issue Classification](#issue-classification)
- [🔧 Maintenance Commands](#maintenance-commands)
  - [Quality Assessment](#quality-assessment)
  - [Automation & CI/CD](#automation-cicd)
  - [Maintenance Tasks](#maintenance-tasks)
- [📊 Quality Thresholds](#quality-thresholds)
  - [Default Configuration](#default-configuration)
  - [CI/CD Quality Gates](#cicd-quality-gates)
- [🔍 Issue Resolution Guide](#issue-resolution-guide)
  - [Common Issues & Solutions](#common-issues-solutions)
- [H2: Section](#h2-section)
  - [H3: Subsection](#h3-subsection)
- [H2: Another Section](#h2-another-section)
- [⚙️ Configuration](#configuration)
  - [Maintenance Configuration](#maintenance-configuration)
  - [Custom Rules](#custom-rules)
- [🔄 Automation Features](#automation-features)
  - [Scheduled Audits](#scheduled-audits)
  - [Pre-commit Hooks](#pre-commit-hooks)
  - [CI/CD Integration](#cicd-integration)
- [📈 Monitoring & Analytics](#monitoring-analytics)
  - [Quality Trends](#quality-trends)
  - [Metrics Dashboard](#metrics-dashboard)
- [🚨 Troubleshooting](#troubleshooting)
  - [Audit Failures](#audit-failures)
  - [Link Validation Issues](#link-validation-issues)
  - [Git Hook Issues](#git-hook-issues)
- [📚 Best Practices](#best-practices)
  - [Content Creation](#content-creation)
  - [Quality Maintenance](#quality-maintenance)
  - [Link Management](#link-management)
- [🎯 Advanced Features](#advanced-features)
  - [Custom Validators](#custom-validators)
  - [Integration APIs](#integration-apis)
- [📞 Support & Resources](#support-resources)
  - [Getting Help](#getting-help)
  - [Related Documentation](#related-documentation)
<!-- TOC END -->

**FLEXT-Meltano Documentation Quality Assurance & Maintenance Framework**

## 🎯 Overview

This guide provides comprehensive documentation for the automated documentation maintenance system implemented for FLEXT-Meltano. The system ensures consistent quality, validates content integrity, and provides automated quality assurance across all documentation.

## 🏗️ Architecture

### Core Components

```
📚 Documentation Maintenance System
├── 🔍 scripts/documentation/audit.py      # Core audit engine (workspace SSOT)
├── ✅ scripts/documentation/validate.py    # Validation gate engine (workspace SSOT)
├── 📊 Quality Reporting        # Automated report generation
├── 🔗 Link Validation         # External/internal link checking
└── 📈 Quality Metrics         # Scoring and trend analysis
```

### Key Features

- **Automated Quality Audits**: Comprehensive content analysis with scoring
- **Link Validation**: External and internal link health monitoring
- **Style Consistency**: Markdown formatting and structure validation
- **CI/CD Integration**: GitHub Actions workflow with quality gates
- **Scheduled Maintenance**: Automated regular quality checks
- **Git Integration**: Pre-commit hooks and quality enforcement

## 🚀 Quick Start

### 1. Run Comprehensive Audit

```bash
# Run full documentation quality assessment
make docs

# Or directly with Python
make docs DOCS_PHASE=all PROJECT=flext-meltano
```

### 2. View Quality Reports

```bash
# View latest quality summary
make docs DOCS_PHASE=audit

# Open detailed report
cat docs/reports/docs_quality_report_*.md
```

### 3. Set Up Quality Gates

```bash
# Install Git hooks for pre-commit quality checks
make docs

# Generate GitHub Actions workflow
make docs
```

## 📋 Quality Metrics

### Overall Quality Score (0-100)

Calculated from weighted components:

| Component             | Weight | Description                          |
| --------------------- | ------ | ------------------------------------ |
| **Content Freshness** | 20%    | File age and update frequency        |
| **Link Health**       | 25%    | Broken link detection and validation |
| **Structure**         | 25%    | Heading hierarchy and organization   |
| **Formatting**        | 15%    | Style consistency and readability    |
| **Accessibility**     | 15%    | Alt text, semantic markup            |

### Issue Classification

- **🚨 Critical**: System-breaking issues (missing files, broken critical links)
- **🔴 High**: Content quality issues (broken links, missing structure)
- **🟡 Medium**: Style and consistency issues
- **🔵 Low**: Minor formatting improvements
- **ℹ️ Info**: Suggestions and best practices

## 🔧 Maintenance Commands

### Quality Assessment

```bash
# Run quality audit only
make docs DOCS_PHASE=audit
make docs DOCS_PHASE=audit PROJECT=flext-meltano

# Validate external links
make docs DOCS_PHASE=validate
make docs DOCS_PHASE=validate PROJECT=flext-meltano

# Generate quality reports
make docs
make docs DOCS_PHASE=audit PROJECT=flext-meltano
```

### Automation & CI/CD

```bash
# Run CI quality checks
make docs
make docs DOCS_PHASE=validate PROJECT=flext-meltano

# Start scheduled monitoring
make docs
make docs DOCS_PHASE=audit PROJECT=flext-meltano

# Set up Git hooks
make docs
make docs
```

### Maintenance Tasks

```bash
# Clean up old reports
make docs

# View comprehensive setup instructions
make docs
```

## 📊 Quality Thresholds

### Default Configuration

```yaml
# docs/.maintenance_config.yaml
quality_thresholds:
  max_file_age_days: 90
  min_words_per_file: 50
  max_broken_links_ratio: 0.05
  max_line_length: 120

rules:
  require_table_of_contents: false
  require_frontmatter: false
  validate_external_links: true
  enforce_heading_case: "title"
  require_alt_text: true
```

### CI/CD Quality Gates

- **Critical Issues**: Must be 0 (blocks commits)
- **Quality Score**: Must be ≥80 (configurable)
- **Link Health**: Broken links ≤5% of total links

## 🔍 Issue Resolution Guide

### Common Issues & Solutions

#### 🔴 High Priority: Broken Internal Links

**Symptoms**: `[text](relative/path.md)` points to non-existent file

**Solution**:

```bash
# Find broken links in reports
grep "broken_internal_link" docs/reports/docs_quality_report_*.md

# Fix by updating link paths or creating missing files
# Re-run audit to verify
make docs
```

#### 🟡 Medium Priority: Missing Structure

**Symptoms**: Files lack proper heading hierarchy

**Solution**:

```markdown
# Good Structure

# H1: Main Title

## H2: Section

### H3: Subsection

## H2: Another Section
```

#### 🔵 Low Priority: Long Lines

**Symptoms**: Lines exceed 120 characters

**Solution**:

```bash
# Auto-format with Prettier or similar
# Or manually break long lines
```

#### ℹ️ Info: TODO Markers

**Symptoms**: `TODO` or `FIXME` found in documentation

**Solution**:

```markdown
<!-- Convert TODOs to actionable items -->

- [ ] Complete API documentation
- [x] Add installation guide
```

## ⚙️ Configuration

### Maintenance Configuration

Edit `docs/.maintenance_config.yaml` to customize:

```yaml
# Quality thresholds
quality_thresholds:
  max_file_age_days: 90 # Flag files older than this

# Automation settings
automation:
  enable_scheduled_audits: true
  audit_schedule: "weekly" # daily, weekly, monthly
  audit_day: "monday"
  audit_time: "09:00" # UTC

# Reporting preferences
reporting:
  output_directory: "docs/reports"
  include_file_details: true
```

### Custom Rules

Add project-specific validation rules:

```yaml
custom_rules:
  flext_patterns:
    - name: "version_consistency"
      pattern: "\\b\\d+\\.\\d+\\.\\d+\\b"
      description: "Version numbers should be consistent"

    - name: "api_references"
      pattern: "`FlextMeltano\\.[a-zA-Z_]+`"
      description: "API references should be properly formatted"
```

## 🔄 Automation Features

### Scheduled Audits

Configure automatic quality checks:

```bash
# Start continuous monitoring
make docs

# Runs according to settings schedule (default: weekly Mondays 09:00 UTC)
```

### Pre-commit Hooks

Automatic quality enforcement:

```bash
# Install Git hooks
make docs

# Now quality checks run before each commit
git commit -m "docs: update api reference"
# -> Quality audit runs automatically
```

### CI/CD Integration

GitHub Actions workflow automatically:

1. Runs on PRs affecting documentation
1. Validates quality thresholds
1. Comments quality report on PRs
1. Blocks merges on critical issues

## 📈 Monitoring & Analytics

### Quality Trends

Track documentation health over time:

```bash
# View quality history
ls -la docs/reports/docs_quality_report_*.md

# Compare quality scores over time
grep "Quality Score" docs/reports/docs_quality_report_*.md
```

### Metrics Dashboard

Key metrics to monitor:

- **Quality Score Trend**: Overall documentation health
- **Issue Count by Type**: Focus areas for improvement
- **File Freshness**: Content update patterns
- **Link Health**: External dependency monitoring

## 🚨 Troubleshooting

### Audit Failures

**Issue**: `scripts/documentation/audit.py` fails

**Solutions**:

```bash
# Check Python environment
python --version  # Should be 3.13+

# Install missing dependencies
pip install PyYAML requests

# Verify script permissions
ls -la scripts/documentation/audit.py

# Check for file encoding issues
file docs/some_file.md  # Should be UTF-8
```

### Link Validation Issues

**Issue**: External link validation fails

**Solutions**:

```bash
# Check network connectivity
curl -I https://example.com

# Update timeout settings in settings
# docs/.maintenance_config.yaml
link_validation_timeout: 15  # Increase timeout

# Skip problematic links temporarily
# Add to docs/.link_skip_list.txt
echo "https://problematic-link.com" >> docs/.link_skip_list.txt
```

### Git Hook Issues

**Issue**: Pre-commit hooks not working

**Solutions**:

```bash
# Check hook installation
ls -la .git/hooks/pre-commit

# Verify hook permissions
chmod +x .git/hooks/pre-commit

# Test hook manually
.git/hooks/pre-commit

# Reinstall hooks
make docs
```

## 📚 Best Practices

### Content Creation

1. **Use Consistent Structure**: Follow established heading hierarchy
1. **Include Examples**: Provide code examples for technical content
1. **Add Cross-references**: Link related documentation sections
1. **Use Alt Text**: Always include descriptive alt text for images
1. **Keep Updated**: Review and update content regularly

### Quality Maintenance

1. **Run Regular Audits**: Schedule weekly comprehensive audits
1. **Fix Issues Promptly**: Address critical and high-priority issues immediately
1. **Monitor Trends**: Track quality metrics over time
1. **Automate Where Possible**: Use CI/CD and hooks for consistent enforcement

### Link Management

1. **Prefer Relative Links**: Use relative paths for internal documentation
1. **Validate Regularly**: Check external links don't break
1. **Use Link Shorteners**: For long URLs that exceed line limits
1. **Document Dependencies**: Note when content depends on external resources

## 🎯 Advanced Features

### Custom Validators

Extend the system with custom validation rules:

```python
from __future__ import annotations

# scripts/custom_validators.py
from docs_maintenance import DocumentationAuditor


class CustomFlextValidator(DocumentationAuditor):
    def _validate_flext_patterns(self, content: str) -> List[str]:
        """Validate FLEXT-specific patterns."""
        issues = []

        # Check for proper import statements
        if "from flext_meltano import" in content:
            if not content.count("from flext_core import"):
                issues.append("Missing flext-core import")

        return issues```
### Integration APIs

Programmatic access to quality data:

```python
from docs_maintenance import DocumentationAuditor

auditor = DocumentationAuditor()
metrics = auditor.audit_all_files()

# Access quality data
score = metrics.quality_score
issues = len(auditor.issues)

# Generate custom reports
auditor.generate_custom_report("api_quality.md")```
## 📞 Support & Resources

### Getting Help

1. **Check This Guide**: Comprehensive troubleshooting section
1. **Run Diagnostics**: `make docs DOCS_PHASE=all PROJECT=flext-meltano`
1. **View Reports**: Check `docs/reports/` for detailed issue analysis
1. **GitHub Issues**: Report bugs or request features

### Related Documentation

- **API Reference**: `docs/api-reference.md`
- **Development Guide**: `docs/development.md`
- **Configuration**: `docs/.maintenance_config.yaml`
- **Quality Reports**: `docs/reports/`

______________________________________________________________________

**Documentation Maintenance Framework v1.0.0**
_Ensuring FLEXT-Meltano documentation excellence through automated quality assurance._
