# from flext-meltano_docs/security/sonarqube-triage.md:826
       19      External library wrappers (singer_sdk.typing) are kept to prevent
       20      direct imports by consumer projects.
       21      """
       22
>>>    23      SingerReplicationMethod = c.Meltano.SingerReplicationMethod
       24
       25      # Singer SDK typing wrappers — prevents direct ``singer_sdk.typing`` imports
       26      SingerArrayType = singer_sdk_typing.ArrayType
       27      SingerBooleanType = singer_sdk_typing.BooleanType
