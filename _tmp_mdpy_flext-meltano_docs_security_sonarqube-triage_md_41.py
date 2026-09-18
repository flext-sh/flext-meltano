# from flext-meltano_docs/security/sonarqube-triage.md:41
       98                  "values": config_result.value
       99              })
      100          except ValueError as exc:
      101              return e.fail_validation(
>>>   102                  "pipeline configuration JSON", error=exc, result_type=r[t.JsonMapping]
      103              )
      104          return r[t.JsonMapping].ok(config_mapping.values)
      105
      106      def _pipeline_command(
