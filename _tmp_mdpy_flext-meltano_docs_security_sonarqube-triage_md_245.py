# from flext-meltano_docs/security/sonarqube-triage.md:245
       66          try:
       67              singer_command = self._tap.get_singer_command()
       68              _ = singer_command.main(args=list(args), prog_name=prog_name)
       69              return 0
>>>    70          except SystemExit as exc:
       71              return exc.code if isinstance(exc.code, int) else 1
       72
       73      def discover_streams(self) -> t.SequenceOf[p.Meltano.SingerStreamInfo]:
       74          """Delegate stream discovery to the raw Singer tap."""
