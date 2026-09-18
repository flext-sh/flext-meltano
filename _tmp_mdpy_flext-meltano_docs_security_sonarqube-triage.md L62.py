# from flext-meltano/docs/security/sonarqube-triage.md:62
      108      ) -> p.Result[t.StrSequence]:
      109          config_result = self._load_pipeline_config(pipeline_name)
      110          if config_result.failure:
      111              return r[t.StrSequence].fail(
>>>   112                  config_result.error or "Pipeline execution not configured"
      113              )
      114          command_value = config_result.value.get("command")
      115          if not isinstance(command_value, t.SEQUENCE_PAIR_TYPES):
      116              return r[t.StrSequence].fail("Pipeline execution not configured")
