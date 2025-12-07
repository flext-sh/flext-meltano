# Documentation Maintenance Quick Start

**Get started with automated documentation quality assurance in 5 minutes**

## 🚀 Quick Setup

### 1. Install Maintenance System

The maintenance system is already included in FLEXT-Meltano. All tools are ready to use:

```bash
# Verify installation
ls scripts/docs_maintenance.py scripts/docs_automation.py
```

### 2. Run Your First Audit

```bash
# Run comprehensive quality audit
make docs-comprehensive

# View results
make docs-view-report
```

### 3. Set Up Quality Gates

```bash
# Install Git hooks (recommended)
make docs-hooks

# Generate CI/CD workflow
make docs-workflow
```

## 📊 Understanding Your Results

### Quality Score Interpretation

- **90-100**: Excellent documentation quality
- **80-89**: Good quality with minor issues
- **70-79**: Needs improvement, address high-priority issues
- **<70**: Requires immediate attention

### Issue Priority Guide

| Priority    | Action Required | Example Issues                            |
| ----------- | --------------- | ----------------------------------------- |
| 🚨 Critical | Fix immediately | Missing critical files, broken navigation |
| 🔴 High     | Fix this week   | Broken internal links, missing structure  |
| 🟡 Medium   | Fix this month  | Style inconsistencies, long lines         |
| 🔵 Low      | Nice to fix     | Minor formatting improvements             |
| ℹ️ Info     | Optional        | Suggestions for enhancement               |

## 🔧 Common Fixes

### Fix Broken Internal Links

```bash
# Find broken links
grep "broken_internal_link" docs/reports/docs_quality_report_*.md

# Fix example: change [text](old/path.md) to [text](correct/path.md)
```

### Add Missing Structure

```markdown
# Before (missing structure)

Content without headings

# After (proper structure)

# Main Topic

## Section 1

Content here

## Section 2

More content
```

### Fix Long Lines

```markdown
# Before (too long)

This is a very long line that exceeds the recommended 120 character limit and makes documentation harder to read.

# After (proper length)

This is a very long line that exceeds the recommended
120 character limit and makes documentation harder to read.
```

## 📈 Monitoring Progress

### Daily Checks

```bash
# Quick quality check
make docs-audit

# View summary
make docs-view-report
```

### Weekly Maintenance

```bash
# Comprehensive audit
make docs-comprehensive

# Review and fix issues
# Check docs/reports/ for detailed reports
```

### CI/CD Status

The system automatically runs quality checks on:

- Pull requests affecting documentation
- Pushes to main/develop branches
- Weekly scheduled audits

## 🎯 Quality Targets

### Minimum Standards

- ✅ Quality Score: ≥80
- ✅ Critical Issues: 0
- ✅ Broken Links: ≤5% of total links
- ✅ File Freshness: Updated within 90 days

### Excellence Targets

- ✅ Quality Score: ≥95
- ✅ All Issues: Addressed within 1 week
- ✅ External Links: 100% valid
- ✅ Accessibility: WCAG AA compliant

## 🚨 Getting Help

### Quick Diagnosis

```bash
# Check system status
python scripts/docs_maintenance.py --audit

# View configuration
cat docs/.maintenance_config.yaml

# Check recent reports
ls -la docs/reports/
```

### Common Issues

**Audit fails to run:**

```bash
# Check Python version (requires 3.13+)
python --version

# Install dependencies
pip install PyYAML requests
```

**Git hooks not working:**

```bash
# Reinstall hooks
make docs-hooks

# Check permissions
ls -la .git/hooks/pre-commit
```

**Reports not generating:**

```bash
# Check output directory
mkdir -p docs/reports

# Run with verbose output
python scripts/docs_maintenance.py --comprehensive
```

## 📚 Advanced Usage

### Custom Configuration

Edit `docs/.maintenance_config.yaml`:

```yaml
quality_thresholds:
  max_file_age_days: 60 # Stricter freshness check
  min_words_per_file: 100 # Require more content

automation:
  audit_schedule: "daily" # More frequent audits
```

### Scheduled Maintenance

```bash
# Start continuous monitoring
make docs-schedule

# Runs automatically according to schedule
```

### Custom Validators

Extend with project-specific rules by modifying the maintenance scripts.

## 🎉 Success Metrics

Track these indicators of maintenance success:

- **Quality Score Trend**: Improving over time
- **Issue Resolution Time**: Critical issues fixed within 24 hours
- **CI/CD Pass Rate**: 100% quality gate compliance
- **Team Adoption**: Regular use of maintenance commands

## 📞 Next Steps

1. **Run your first comprehensive audit**: `make docs-comprehensive`
2. **Review and fix high-priority issues** from the report
3. **Set up automated quality gates**: `make docs-setup`
4. **Monitor quality trends** weekly
5. **Customize configuration** as needed

---

**Ready to maintain documentation excellence!** ✨

_For detailed documentation, see `docs/MAINTENANCE_GUIDE.md`_
