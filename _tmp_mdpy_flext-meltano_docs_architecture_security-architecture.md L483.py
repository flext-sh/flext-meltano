# from flext-meltano/docs/architecture/security-architecture.md:483
from __future__ import annotations


@dataclass
class DataClassification:
    """Data classification with handling requirements."""

    level: str  # 'public', 'internal', 'confidential', 'restricted'
    encryption_required: bool = False
    masking_required: bool = False
    retention_period_days: int = 2555  # 7 years default
    audit_required: bool = False

    def get_handling_requirements(self) -> Dict[str, t.JsonValue]:
        """Get data handling requirements based on classification."""
        requirements = {
            "public": {
                "encryption": False,
                "masking": False,
                "audit": False,
                "retention": 365,
            },
            "internal": {
                "encryption": True,
                "masking": False,
                "audit": False,
                "retention": 2555,
            },
            "confidential": {
                "encryption": True,
                "masking": True,
                "audit": True,
                "retention": 2555,
            },
            "restricted": {
                "encryption": True,
                "masking": True,
                "audit": True,
                "retention": 2555,
            },
        }
        return requirements.get(self.level, requirements["internal"])```
______________________________________________________________________

## 🌐 Network Security

### Network Architecture

