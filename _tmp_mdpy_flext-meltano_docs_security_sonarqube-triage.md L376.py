# from flext-meltano/docs/security/sonarqube-triage.md:376
       28      instead of importing singer_sdk directly.
       29      """
       30
       31      SingerTapBase = Tap
>>>    32      SingerSinkBase = Sink
       33      SingerStreamBase = Stream
       34      SingerTargetBase = Target
       35      SingerContext = Context
       36      SingerRecord = Record
