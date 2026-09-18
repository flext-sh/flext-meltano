# from flext-meltano_docs/architecture/quality-attributes.md:3307
from __future__ import annotations


class TestableService:
    """Service designed for testability with dependency injection."""

    def __init__(
        self,
        repository: Repository = None,
        validator: Validator = None,
        notifier: Notifier = None,
    ):
        self.repository = repository or DefaultRepository()
        self.validator = validator or DefaultValidator()
        self.notifier = notifier or DefaultNotifier()

    def process_request(self, request: Request) -> Response:
        """Process request with injected dependencies."""
        # Validation
        validation_result = self.validator.validate(request)
        if validation_result.failure:
            return Response.error(validation_result.error)

        # Business logic
        entity = self.repository.get(request.entity_id)
        if not entity:
            return Response.not_found()

        # Processing
        result = self._process_entity(entity, request)

        # Notification
        self.notifier.notify_success(result)

        return Response.success(result)

    # Separate business logic for easy testing
    def _process_entity(self, entity: Entity, request: Request) -> Result:
        """Pure business logic, easy to unit test."""
        # Complex business logic here
        return entity.process(request.data)```
#### 2. Test Data Builders

