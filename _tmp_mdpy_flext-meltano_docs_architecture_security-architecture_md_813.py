# from flext-meltano_docs/architecture/security-architecture.md:813
from __future__ import annotations
class DataPrivacyController:
    """GDPR/CCPA compliance controls."""

    def __init__(self, data_store):
        self.data_store = data_store

    def handle_data_subject_request(self, request: DataSubjectRequest) -> p.Result[ComplianceAction]:
        """Handle data subject access/deletion requests."""

        if request.request_type == 'access':
            # Provide data inventory
            user_data = self._collect_user_data(request.user_id)
            return r.ok(ComplianceAction(
                action_type='data_export',
                data=user_data,
                format='json'
            ))

        elif request.request_type == 'deletion':
            # Delete user data (right to be forgotten)
            deletion_result = self._delete_user_data(request.user_id)
            if deletion_result.success:
                self._audit_data_deletion(request.user_id, request.reason)
                return r.ok(ComplianceAction(
                    action_type='data_deleted',
                    confirmation_id=str(uuid.uuid4())
                ))
            else:
                return deletion_result

        return r.fail(ValidationError("Invalid request type"))

    def _collect_user_data(self, user_id: str) -> Dict[str, t.JsonValue]:
        """Collect all user data for export."""
        return {
            'personal_data': self.data_store.get_user_profile(user_id),
            'pipeline_history': self.data_store.get_user_pipelines(user_id),
            'audit_logs': self.data_store.get_user_audit_logs(user_id),
            'preferences': self.data_store.get_user_preferences(user_id)
        }

    def _delete_user_data(self, user_id: str) -> p.Result[bool]:
        """Delete all user data."""
        try:
            # Anonymize instead of delete for audit purposes
            self.data_store.anonymize_user_data(user_id)
            return r.| ok(value=True)
        except Exception as e:
            return r.fail(DataDeletionError(f"Failed to delete user data: {e}"))```
#### Audit and Reporting

