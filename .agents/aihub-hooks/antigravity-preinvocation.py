#!/usr/bin/env python3
"""AI Hub governance hook projection: antigravity preinvocation.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

# Copyright (c) 2025 FLEXT Team. All rights reserved.
"""AI Hub governance hook projection: antigravity preinvocation."""
from __future__ import annotations

import json
import sys

payload = json.load(sys.stdin)
if not isinstance(payload, dict):
    msg = "hook input must be a JSON object"
    raise TypeError(msg)
response = json.loads(
    ('{"injectSteps":[{"ephemeralMessage":"<!-- AIHUB-GOVERNANCE-CAPSU'
         'LE v1 sha256:5888ee9f8147f63364a4f7cd6906e9d837f58cb8a8546844760'
         'c526ecb1a303b -->\\n# Generated session governance capsule\\n\\n'
         'This projection is derived by `agentsctl sync`; edit canonical `'
         'AGENTS.md`, `rules/`, `skills/`, or `commands/`, never this outp'
         'ut. The operator\'s newest request has precedence. Provider hook'
         's are delivery mechanisms, not policy owners.\\n\\n## Rule `arch'
         'itecture/engineering-core`\\n\\n# Engineering core\\n\\nFor ever'
         'y implementation:\\n\\n1. Research repository owners, dependenci'
         'es, and canonical documentation.\\n2. Remove scope without a cur'
         'rent requirement or consumer (YAGNI).\\n3. Elect one writable au'
         'thority; every other copy is a generated projection\\n   (SSOT).'
         '\\n4. Apply SOLID only to a responsibility or dependency boundar'
         'y under change.\\n5. Implement through the owner and simplify wi'
         'thout weakening behavior.\\n6. Remove duplication and god compon'
         'ents; recheck YAGNI, SSOT, SOLID.\\n7. Exercise runtime behavior'
         ', run every applicable native gate, and complete\\n   the approv'
         'ed landing cycle before changing phase.\\n\\nAt a cross-boundary'
         ' failure, prove the producer contract and output. Fix its\\nowne'
         'r when invalid or the receiver when it conforms. Never alter a c'
         'orrect\\nadjacent owner for an invalid consumer; symptom workaro'
         'unds are defects.\\n\\nHardcodes, normalized failure, failover, '
         'retry, fallback, compatibility,\\npartial execution, keyring, an'
         'd unevidenced success are defects. Typed owners\\nkeep defaults.'
         ' The first exception escapes its CLI with traceback and cause.\\'
         'n\\nGit, runtime, build, and tests are baseline. Auxiliary track'
         'ing is a capability.\\nAuxiliary capabilities apply only when au'
         'thorized and selected; installation\\nnever selects. Do not load'
         ', probe, or gate dormant capabilities. Invalid\\nselected author'
         'ization, configuration, readiness, or result fails without\\nfal'
         'lback. Require only non-derivable values.\\n\\nAn external token'
         ' validation without its token is not executed and is recorded\\n'
         'as `NOT EXECUTED`, never green; it does not block offline gates,'
         ' landing, or\\npost-merge proof. Direct invocation selects it: t'
         'he token becomes required and\\nany failure escapes without skip'
         ', catch, fallback, or normalization.\\n\\nCompose with `generali'
         'zed ownership` (rule file),\\n`strict execution` (rule file),\\n'
         '`runtime evidence` (rule file),\\n`storage isolation` (rule file'
         '),\\n`security closure` (rule file).\\n\\n## Rule `coordination/'
         'operator-precedence`\\n\\n# Newest operator instruction wins; ad'
         'just artifacts to it\\n\\nAuthority order: operator request > de'
         'clared orchestration contract > canonical\\ntracker > ADRs > ski'
         'lls > docs, and newest supersedes oldest. On conflict,\\nadjust '
         'the lower or older artifact to match; never override the operato'
         'r to\\nsatisfy stale guidance.\\n\\nWhile orchestration and trac'
         'ker runtimes are suspended, do not invoke them.\\nCreate no subs'
         'titute tracker or ledger, preserve implementation evidence only\\'
         'nin separately authorized Git/PR/CI, and leave phase closure ope'
         'n.\\n\\nExact operator authorization naming targets, disposition'
         ', recovery, and\\nvalidation survives interruption, divergence, '
         'and red gates; re-preflight and\\ncontinue. Ask only when the ef'
         'fect expands beyond it or two evidenced current\\nintentions con'
         'flict. State alone proves no intention, actor, or process.\\n\\n'
         '## Rule `ethics/professional-integrity`\\n\\n# Professional inte'
         'grity is absolute\\n\\nNever lie, fabricate evidence, hide a blo'
         'cker, bypass a gate, or patch a symptom\\nonly to make a check p'
         'ass. Fix the generalized root cause with full context and\\nrepo'
         'rt exact command, working directory, exit code and decisive outp'
         'ut.\\n\\n## Rule `runtime/strict-execution`\\n\\n# Strict execut'
         'ion is universal and non-optional\\n\\nEvery project and project'
         'ed agent applies all of these policies together:\\n\\n- `fail lo'
         'ud` (rule file);\\n- `no fallback` (rule file);\\n- `preflight b'
         'efore effects` (rule file);\\n- `required environment` (rule fil'
         'e);\\n- `atomic effects` (rule file);\\n- `causal subprocess pro'
         'pagation` (rule file);\\n- `no keyring` (rule file);\\n- `zero r'
         'esidue` (rule file).\\n\\nThe policies are cumulative. A project'
         ' rule may make them narrower or reject\\nmore inputs; it cannot '
         'relax, catch, normalize, skip, defer, or route around any\\nof t'
         'hem. Existing opposing behavior is a blocking violation to exter'
         'minate at\\nits owner, never grandfathered compatibility.\\n\\nR'
         'esolve gate applicability before invocation. A dormant external-'
         'token gate is\\nnot executed; selecting or invoking it applies e'
         'very policy above.\\n\\n## Capability indexes\\n\\nSkills: cavem'
         'an, context-canary, fix-forward-collaboration, governance-audit,'
         ' operator-correction-learning, plan-focus-recovery, sprint-closu'
         're, strategic-compact, verification-loop\\nCommands: add-languag'
         'e-rules, database-migration, feature-development, ghi-list, pr-l'
         'ist, ralph-loop, security-triage, synthesize-governance\\n"}]}'),

)
json.dump(response, sys.stdout, ensure_ascii=False, separators=(",", ":"))
sys.stdout.write("\n")
