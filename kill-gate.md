# Kill-gate — fhir-validator-cli

**Decision date:** d+30 from public launch (PyPI publish + r/HL7 post + HL7 Europe Slack drop).

**Continue if any of:**

1. **≥40 GitHub stars** on the repo (proxy: someone outside the operator's network found it).
2. **≥3 real-affiliation GitHub issues** opened — issues whose author's profile shows a hospital, regional health authority, HL7 affiliate, EHDS contractor, or named digital-health vendor (not the operator, not generic accounts).
3. **≥10 `pip install` per pypistats** in the trailing 14 days (proxy: someone is actually trying the CLI).
4. **≥1 inbound** — DM, email, or LinkedIn message asking about EHDS, hosted CI, or custom IGs.

**Kill if none of the above.** Move to `archive/fhir-validator-cli/` with a post-mortem covering: what channel produced zero engagement, whether HAPI is too entrenched, whether the EU IG-bundle angle is too niche, whether EHDS timeline is too slow to drive demand.

**Half-life check at d+14:** if the trajectory is <25% of the d+30 thresholds (e.g., <10 stars, 0 issues, <2 installs), do not double down on distribution — preserve calories for the rest of the wave.

**What does NOT count:**

- Operator-created accounts / sock-puppet stars.
- Stars from the personal network (LinkedIn 1st-degree).
- Bot traffic from PyPI mirrors.

**What buys time without continuing:**

- A specific EU national-affiliate (HL7 Spain, HL7 France, etc.) saying "we'd ship this in our CI if it bundled our IG" — that's a fork-point, not a kill, but it changes the roadmap (v0.3 brought forward).
