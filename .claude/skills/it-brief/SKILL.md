---
name: it-brief
description: Produce a shadow-usage IT brief for one account or every tier-A account in a CSV. Usage: /it-brief <accounts.csv|account_id>
---
# /it-brief $ARGUMENTS

Follow CLAUDE.md zones and hard rules. Steps:
1. If $ARGUMENTS is a CSV, run `python scoring/score_accounts.py <csv>` and take tier A rows; else load the one row.
2. Decide the variant: `count` if flow_users is present, else `public-signal`.
3. Retrieve claims: load claims/library.yaml rows with topic in [governance, privacy, consent, compliance]; list their ids as claims_retrieved.
4. Fill inputs/templates/it-brief.md. Every control cites a claim id and its plan scope. Unknown facts -> "Not found in sources — escalate."
5. Stamp library_hash with `python scripts/stamp.py`. Save to outputs/review/<account_id>/it-brief.md.
6. Run `python verify/check_ids.py <file>`. If it fails, fix and re-run (max 2 rewrites).
7. Invoke the faithfulness-judge subagent on the file; if any line is `unsupported`, rewrite (max 2).
8. Invoke reviewer-it; append its findings under "## Reviewer notes".
9. `python scripts/ledger.py run it-brief <input> <pass|fail> <cost>` then `python scripts/ledger.py state <file> draft claude`.
Never send anything. Never write to a CRM.
