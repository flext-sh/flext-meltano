# from flext-meltano/docs/security/sonarqube-triage.md:847
       22
       23      SingerReplicationMethod = c.Meltano.SingerReplicationMethod
       24
       25      # Singer SDK typing wrappers — prevents direct ``singer_sdk.typing`` imports
>>>    26      SingerArrayType = singer_sdk_typing.ArrayType
       27      SingerBooleanType = singer_sdk_typing.BooleanType
       28      SingerCustomType = singer_sdk_typing.CustomType
       29      SingerDateTimeType = singer_sdk_typing.DateTimeType
       30      SingerDateType = singer_sdk_typing.DateType
