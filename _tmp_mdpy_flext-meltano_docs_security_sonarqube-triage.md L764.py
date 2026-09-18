# from flext-meltano/docs/security/sonarqube-triage.md:764
      206          def sync_all(self) -> None:
      207              """Execute sync for all selected streams."""
      208              ...
      209
>>>   210      SingerTapSdkBackend = SingerTapBackend
      211      SingerTapSettingsBackend = SingerTapBackend
      212
      213      @runtime_checkable
      214      class SingerDrainSink(Protocol):
