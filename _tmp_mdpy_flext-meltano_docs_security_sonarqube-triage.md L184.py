# from flext-meltano/docs/security/sonarqube-triage.md:184
      317              )
      318          except c.Meltano.OPERATION_ERRORS as e:
      319              return r[m.Meltano.CommandExecutionResult].fail(str(e))
      320
>>>   321      def execute_pipeline(
      322          self, tap_name: str, target_name: str, config: t.JsonMapping | None = None
      323      ) -> p.Result[m.Meltano.CommandExecutionResult]:
      324          """Execute a complete ELT pipeline."""
      325          prepared_command: t.StrSequence | None = None
