# from flext-meltano_docs/architecture/quality-attributes.md:2967
from __future__ import annotations


class APIResource:
    """API resource with progressive disclosure."""

    def __init__(
        self,
        resource_id: str,
        basic_fields: Dict[str, t.JsonValue],
        detailed_fields: Dict[str, t.JsonValue] = None,
    ):
        self.id = resource_id
        self.basic_fields = basic_fields
        self.detailed_fields = detailed_fields or {}

    def to_basic_representation(self) -> Dict[str, t.JsonValue]:
        """Return basic resource representation."""
        return {
            "id": self.id,
            "type": self.__class__.__name__.lower(),
            "links": self._get_basic_links(),
            **self.basic_fields,
        }

    def to_detailed_representation(self) -> Dict[str, t.JsonValue]:
        """Return detailed resource representation."""
        return {
            **self.to_basic_representation(),
            "links": self._get_detailed_links(),
            **self.detailed_fields,
        }

    def to_minimal_representation(self) -> Dict[str, t.JsonValue]:
        """Return minimal resource representation for lists."""
        return {
            "id": self.id,
            "type": self.__class__.__name__.lower(),
            "url": f"/api/v1/{self.__class__.__name__.lower()}s/{self.id}",
        }

    def _get_basic_links(self) -> Dict[str, str]:
        """Get basic HATEOAS links."""
        return {
            "self": f"/api/v1/{self.__class__.__name__.lower()}s/{self.id}",
            "collection": f"/api/v1/{self.__class__.__name__.lower()}s",
        }

    def _get_detailed_links(self) -> Dict[str, str]:
        """Get detailed HATEOAS links."""
        links = self._get_basic_links()

        # Add related resource links
        if hasattr(self, "pipeline_id"):
            links["pipeline"] = f"/api/v1/pipelines/{self.pipeline_id}"

        if hasattr(self, "user_id"):
            links["user"] = f"/api/v1/users/{self.user_id}"

        # Add action links
        links["update"] = f"/api/v1/{self.__class__.__name__.lower()}s/{self.id}"
        links["delete"] = f"/api/v1/{self.__class__.__name__.lower()}s/{self.id}"

        return links```
#### 3. Contextual Help System

