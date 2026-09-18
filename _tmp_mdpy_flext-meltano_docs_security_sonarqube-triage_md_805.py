# from flext-meltano_docs/security/sonarqube-triage.md:805
       28      )
       29
       30      type ValidatorInput = t.JsonValue
       31
>>>    32      PluginType = c.Meltano.PluginType
       33
       34      type VariantValue = str | t.StrSequence | t.ScalarMapping | None
       35      """Normalized plugin variant: string, string list, scalar mapping, or null."""
       36
