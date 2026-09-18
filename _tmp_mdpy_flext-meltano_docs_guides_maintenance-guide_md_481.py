# from flext-meltano_docs/guides/maintenance-guide.md:481
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
