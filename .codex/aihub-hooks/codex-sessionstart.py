#!/usr/bin/env python3
"""AI Hub governance hook projection: codex sessionstart.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import sys

payload = json.load(sys.stdin)
if not isinstance(payload, dict):
    msg = "hook input must be a JSON object"
    raise TypeError(msg)
response = json.loads(
    ('{"hookSpecificOutput":{"hookEventName":"SessionStart","additiona'
         'lContext":"<!-- AIHUB-GOVERNANCE-CAPSULE v1 sha256:5888ee9f8147f'
         '63364a4f7cd6906e9d837f58cb8a8546844760c526ecb1a303b -->\\n# Gene'
         'rated session governance capsule\\n\\nThis projection is derived'
         ' by `agentsctl sync`; edit canonical `AGENTS.md`, `rules/`, `ski'
         'lls/`, or `commands/`, never this output. The operator\'s newest'
         ' request has precedence. Provider hooks are delivery mechanisms,'
         ' not policy owners.\\n\\n## Rule `architecture/engineering-core`'
         '\\n\\n# Engineering core\\n\\nFor every implementation:\\n\\n1. '
         'Research repository owners, dependencies, and canonical document'
         'ation.\\n2. Remove scope without a current requirement or consum'
         'er (YAGNI).\\n3. Elect one writable authority; every other copy '
         'is a generated projection\\n   (SSOT).\\n4. Apply SOLID only to '
         'a responsibility or dependency boundary under change.\\n5. Imple'
         'ment through the owner and simplify without weakening behavior.\\'
         'n6. Remove duplication and god components; recheck YAGNI, SSOT, '
         'SOLID.\\n7. Exercise runtime behavior, run every applicable nati'
         've gate, and complete\\n   the approved landing cycle before cha'
         'nging phase.\\n\\nAt a cross-boundary failure, prove the produce'
         'r contract and output. Fix its\\nowner when invalid or the recei'
         'ver when it conforms. Never alter a correct\\nadjacent owner for'
         ' an invalid consumer; symptom workarounds are defects.\\n\\nHard'
         'codes, normalized failure, failover, retry, fallback, compatibil'
         'ity,\\npartial execution, keyring, and unevidenced success are d'
         'efects. Typed owners\\nkeep defaults. The first exception escape'
         's its CLI with traceback and cause.\\n\\nGit, runtime, build, an'
         'd tests are baseline. Auxiliary tracking is a capability.\\nAuxi'
         'liary capabilities apply only when authorized and selected; inst'
         'allation\\nnever selects. Do not load, probe, or gate dormant ca'
         'pabilities. Invalid\\nselected authorization, configuration, rea'
         'diness, or result fails without\\nfallback. Require only non-der'
         'ivable values.\\n\\nAn external token validation without its tok'
         'en is not executed and is recorded\\nas `NOT EXECUTED`, never gr'
         'een; it does not block offline gates, landing, or\\npost-merge p'
         'roof. Direct invocation selects it: the token becomes required a'
         'nd\\nany failure escapes without skip, catch, fallback, or norma'
         'lization.\\n\\nCompose with `generalized ownership` (rule file),'
         '\\n`strict execution` (rule file),\\n`runtime evidence` (rule fi'
         'le),\\n`storage isolation` (rule file),\\n`security closure` (ru'
         'le file).\\n\\n## Rule `coordination/operator-precedence`\\n\\n#'
         ' Newest operator instruction wins; adjust artifacts to it\\n\\nA'
         'uthority order: operator request > declared orchestration contra'
         'ct > canonical\\ntracker > ADRs > skills > docs, and newest supe'
         'rsedes oldest. On conflict,\\nadjust the lower or older artifact'
         ' to match; never override the operator to\\nsatisfy stale guidan'
         'ce.\\n\\nWhile orchestration and tracker runtimes are suspended,'
         ' do not invoke them.\\nCreate no substitute tracker or ledger, p'
         'reserve implementation evidence only\\nin separately authorized '
         'Git/PR/CI, and leave phase closure open.\\n\\nExact operator aut'
         'horization naming targets, disposition, recovery, and\\nvalidati'
         'on survives interruption, divergence, and red gates; re-prefligh'
         't and\\ncontinue. Ask only when the effect expands beyond it or '
         'two evidenced current\\nintentions conflict. State alone proves '
         'no intention, actor, or process.\\n\\n## Rule `ethics/profession'
         'al-integrity`\\n\\n# Professional integrity is absolute\\n\\nNev'
         'er lie, fabricate evidence, hide a blocker, bypass a gate, or pa'
         'tch a symptom\\nonly to make a check pass. Fix the generalized r'
         'oot cause with full context and\\nreport exact command, working '
         'directory, exit code and decisive output.\\n\\n## Rule `runtime/'
         'strict-execution`\\n\\n# Strict execution is universal and non-o'
         'ptional\\n\\nEvery project and projected agent applies all of th'
         'ese policies together:\\n\\n- `fail loud` (rule file);\\n- `no f'
         'allback` (rule file);\\n- `preflight before effects` (rule file)'
         ';\\n- `required environment` (rule file);\\n- `atomic effects` ('
         'rule file);\\n- `causal subprocess propagation` (rule file);\\n-'
         ' `no keyring` (rule file);\\n- `zero residue` (rule file).\\n\\n'
         'The policies are cumulative. A project rule may make them narrow'
         'er or reject\\nmore inputs; it cannot relax, catch, normalize, s'
         'kip, defer, or route around any\\nof them. Existing opposing beh'
         'avior is a blocking violation to exterminate at\\nits owner, nev'
         'er grandfathered compatibility.\\n\\nResolve gate applicability '
         'before invocation. A dormant external-token gate is\\nnot execut'
         'ed; selecting or invoking it applies every policy above.\\n\\n##'
         ' Capability indexes\\n\\nSkills: caveman, context-canary, fix-fo'
         'rward-collaboration, governance-audit, operator-correction-learn'
         'ing, plan-focus-recovery, sprint-closure, strategic-compact, ver'
         'ification-loop\\nCommands: add-language-rules, database-migratio'
         'n, feature-development, ghi-list, pr-list, ralph-loop, security-'
         'triage, synthesize-governance\\n"}}'),

)
json.dump(response, sys.stdout, ensure_ascii=False, separators=(",", ":"))
sys.stdout.write("\n")
