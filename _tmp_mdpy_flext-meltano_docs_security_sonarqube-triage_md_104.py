# from flext-meltano_docs/security/sonarqube-triage.md:104
       70      # ------------------------------------------------------------------
       71      # CLI dispatch
       72      # ------------------------------------------------------------------
       73
>>>    74      def cli_main(self, args: t.StrSequence | None = None) -> int:
       75          """Run the main CLI entry point for dbt project."""
       76
       77          def _run_cli_main() -> int:
       78              command_args = list(args) if args else sys.argv[1:]
