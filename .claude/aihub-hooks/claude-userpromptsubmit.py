#!/usr/bin/env python3
"""AI Hub governance hook projection: claude userpromptsubmit.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

# Copyright (c) 2025 FLEXT Team. All rights reserved.
"""AI Hub governance hook projection: claude userpromptsubmit."""
from __future__ import annotations

import json
import sys

payload = json.load(sys.stdin)
if not isinstance(payload, dict):
    msg = "hook input must be a JSON object"
    raise TypeError(msg)
response = json.loads(
    ('{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","addit'
         'ionalContext":"<!-- AIHUB-GOVERNANCE-CAPSULE v1 sha256:5888ee9f8'
         '147f63364a4f7cd6906e9d837f58cb8a8546844760c526ecb1a303b -->\\n# '
         'Generated session governance capsule\\n\\nThis projection is der'
         'ived by `agentsctl sync`; edit canonical `AGENTS.md`, `rules/`, '
         '`skills/`, or `commands/`, never this output. The operator\'s ne'
         'west request has precedence. Provider hooks are delivery mechani'
         'sms, not policy owners.\\n\\n## Rule `architecture/engineering-c'
         'ore`\\n\\n# Engineering core\\n\\nFor every implementation:\\n\\'
         'n1. Research repository owners, dependencies, and canonical docu'
         'mentation.\\n2. Remove scope without a current requirement or co'
         'nsumer (YAGNI).\\n3. Elect one writable authority; every other c'
         'opy is a generated projection\\n   (SSOT).\\n4. Apply SOLID only'
         ' to a responsibility or dependency boundary under change.\\n5. I'
         'mplement through the owner and simplify without weakening behavi'
         'or.\\n6. Remove duplication and god components; recheck YAGNI, S'
         'SOT, SOLID.\\n7. Exercise runtime behavior, run every applicable'
         ' native gate, and complete\\n   the approved landing cycle befor'
         'e changing phase.\\n\\nAt a cross-boundary failure, prove the pr'
         'oducer contract and output. Fix its\\nowner when invalid or the '
         'receiver when it conforms. Never alter a correct\\nadjacent owne'
         'r for an invalid consumer; symptom workarounds are defects.\\n\\'
         'nHardcodes, normalized failure, failover, retry, fallback, compa'
         'tibility,\\npartial execution, keyring, and unevidenced success '
         'are defects. Typed owners\\nkeep defaults. The first exception e'
         'scapes its CLI with traceback and cause.\\n\\nGit, runtime, buil'
         'd, and tests are baseline. Auxiliary tracking is a capability.\\'
         'nAuxiliary capabilities apply only when authorized and selected;'
         ' installation\\nnever selects. Do not load, probe, or gate dorma'
         'nt capabilities. Invalid\\nselected authorization, configuration'
         ', readiness, or result fails without\\nfallback. Require only no'
         'n-derivable values.\\n\\nAn external token validation without it'
         's token is not executed and is recorded\\nas `NOT EXECUTED`, nev'
         'er green; it does not block offline gates, landing, or\\npost-me'
         'rge proof. Direct invocation selects it: the token becomes requi'
         'red and\\nany failure escapes without skip, catch, fallback, or '
         'normalization.\\n\\nCompose with `generalized ownership` (rule f'
         'ile),\\n`strict execution` (rule file),\\n`runtime evidence` (ru'
         'le file),\\n`storage isolation` (rule file),\\n`security closure'
         '` (rule file).\\n\\n## Rule `coordination/operator-precedence`\\'
         'n\\n# Newest operator instruction wins; adjust artifacts to it\\'
         'n\\nAuthority order: operator request > declared orchestration c'
         'ontract > canonical\\ntracker > ADRs > skills > docs, and newest'
         ' supersedes oldest. On conflict,\\nadjust the lower or older art'
         'ifact to match; never override the operator to\\nsatisfy stale g'
         'uidance.\\n\\nWhile orchestration and tracker runtimes are suspe'
         'nded, do not invoke them.\\nCreate no substitute tracker or ledg'
         'er, preserve implementation evidence only\\nin separately author'
         'ized Git/PR/CI, and leave phase closure open.\\n\\nExact operato'
         'r authorization naming targets, disposition, recovery, and\\nval'
         'idation survives interruption, divergence, and red gates; re-pre'
         'flight and\\ncontinue. Ask only when the effect expands beyond i'
         't or two evidenced current\\nintentions conflict. State alone pr'
         'oves no intention, actor, or process.\\n\\n## Rule `ethics/profe'
         'ssional-integrity`\\n\\n# Professional integrity is absolute\\n\\'
         'nNever lie, fabricate evidence, hide a blocker, bypass a gate, o'
         'r patch a symptom\\nonly to make a check pass. Fix the generaliz'
         'ed root cause with full context and\\nreport exact command, work'
         'ing directory, exit code and decisive output.\\n\\n## Rule `runt'
         'ime/strict-execution`\\n\\n# Strict execution is universal and n'
         'on-optional\\n\\nEvery project and projected agent applies all o'
         'f these policies together:\\n\\n- `fail loud` (rule file);\\n- `'
         'no fallback` (rule file);\\n- `preflight before effects` (rule f'
         'ile);\\n- `required environment` (rule file);\\n- `atomic effect'
         's` (rule file);\\n- `causal subprocess propagation` (rule file);'
         '\\n- `no keyring` (rule file);\\n- `zero residue` (rule file).\\'
         'n\\nThe policies are cumulative. A project rule may make them na'
         'rrower or reject\\nmore inputs; it cannot relax, catch, normaliz'
         'e, skip, defer, or route around any\\nof them. Existing opposing'
         ' behavior is a blocking violation to exterminate at\\nits owner,'
         ' never grandfathered compatibility.\\n\\nResolve gate applicabil'
         'ity before invocation. A dormant external-token gate is\\nnot ex'
         'ecuted; selecting or invoking it applies every policy above.\\n\\'
         'n## Capability indexes\\n\\nSkills: caveman, context-canary, fix'
         '-forward-collaboration, governance-audit, operator-correction-le'
         'arning, plan-focus-recovery, sprint-closure, strategic-compact, '
         'verification-loop\\nCommands: add-language-rules, database-migra'
         'tion, feature-development, ghi-list, pr-list, ralph-loop, securi'
         'ty-triage, synthesize-governance\\n"}}'),

)
json.dump(response, sys.stdout, ensure_ascii=False, separators=(",", ":"))
sys.stdout.write("\n")
