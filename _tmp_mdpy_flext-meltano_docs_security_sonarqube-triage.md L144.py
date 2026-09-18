# from flext-meltano/docs/security/sonarqube-triage.md:144
       43              try:
       44                  _ = command.main(
       45                      args=list(args), prog_name=prog_name, standalone_mode=False
       46                  )
>>>    47              except SystemExit as exc:
       48                  return exc.code if isinstance(exc.code, int) else 1
       49              return 0
       50
       51          def discover_streams(self) -> t.SequenceOf[p.Meltano.SingerStreamInfo]:
