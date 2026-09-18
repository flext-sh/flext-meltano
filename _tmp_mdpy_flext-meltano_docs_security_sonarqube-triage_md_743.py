# from flext-meltano_docs/security/sonarqube-triage.md:743
       13
       14  class FlextMeltanoModelsSources:
       15      """Source and configuration models."""
       16
>>>    17      StreamDefinition: ClassVar[
       18          type[FlextMeltanoModelsSourcesParams.StreamDefinition]
       19      ] = FlextMeltanoModelsSourcesParams.StreamDefinition
       20
       21      class TapConfig(m.Entity):
