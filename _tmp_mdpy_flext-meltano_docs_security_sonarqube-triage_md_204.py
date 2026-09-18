# from flext-meltano_docs/security/sonarqube-triage.md:204
      394                  failed_stage.error
      395                  if failed_stage is not None and failed_stage.error is not None
      396                  else "Failed to run Meltano pipeline"
      397              )
>>>   398          if completed_result is None:
      399              return r[m.Meltano.CommandExecutionResult].fail(
      400                  "Pipeline execution result missing"
      401              )
      402          return r[m.Meltano.CommandExecutionResult].ok(completed_result)
