# from flext-meltano_docs/security/sonarqube-triage.md:785
      207              """Execute sync for all selected streams."""
      208              ...
      209
      210      SingerTapSdkBackend = SingerTapBackend
>>>   211      SingerTapSettingsBackend = SingerTapBackend
      212
      213      @runtime_checkable
      214      class SingerDrainSink(Protocol):
      215          """Typed sink contract for target service drain and record operations.
