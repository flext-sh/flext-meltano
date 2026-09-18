# from flext-meltano/docs/security/sonarqube-triage.md:225
       69              error_msg = f"Failed to discover plugins: {e}"
       70              self.logger.exception(error_msg, error=str(e))
       71              return r[t.SequenceOf[t.StrMapping]].fail(error_msg)
       72
>>>    73      def _discover_plugins(
       74          self, project: t.JsonPayload | t.Meltano.DbtProject | None
       75      ) -> p.Result[t.SequenceOf[t.StrMapping]]:
       76          """Discover plugins without owning the exception boundary."""
       77          self.logger.info("Discovering Meltano plugins")
