# from flext-meltano_docs/security/sonarqube-triage.md:355
       27      the canonical m.Meltano.Singer* namespace. Consumers subclass these
       28      instead of importing singer_sdk directly.
       29      """
       30
>>>    31      SingerTapBase = Tap
       32      SingerSinkBase = Sink
       33      SingerStreamBase = Stream
       34      SingerTargetBase = Target
       35      SingerContext = Context
