# from flext-meltano_docs/security/sonarqube-triage.md:83
      145      ) -> p.Result[str]:
      146          """Create and persist a named pipeline configuration."""
      147          name_result = self._normalize_pipeline_name(pipeline_name)
      148          if name_result.failure:
>>>   149              return r[str].fail(name_result.error or "Pipeline name is invalid")
      150          if config_payload is None:
      151              return r[str].fail("Pipeline creation not configured")
      152          try:
      153              config_mapping = m.Meltano.ConfigMappingPayload.model_validate({
