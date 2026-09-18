# from flext-meltano/docs/security/sonarqube-triage.md:124
       45              c.Meltano.DbtResourceType.MODEL
       46          )
       47          if model_nodes_result.failure:
       48              return r[t.SequenceOf[t.Meltano.OptionalScalarMap]].fail(
>>>    49                  model_nodes_result.error or "Unknown error"
       50              )
       51          try:
       52              models = [
       53                  self._build_manifest_node_summary(node)
