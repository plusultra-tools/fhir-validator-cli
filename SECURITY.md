# Security policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.1.x   | yes       |
| < 0.1   | no        |

## Reporting a vulnerability

Email **plusultra.dev@proton.me** with subject `[fhir-validator-cli] security`. Do **not** open a public GitHub issue for security findings.

Expected response: best-effort acknowledgement within 72 hours, triage within 7 days, fix or mitigation within 30 days for high-severity issues. Once the EU Cyber Resilience Act (CRA) applies to this product (CRA enforcement from late 2027 for products with digital elements), reporting timelines will align with CRA Annex VII obligations (24 h notification of actively exploited vulnerabilities).

## Threat model

`fhir-validator-cli` is a local CLI that parses FHIR JSON resources supplied by the user. Trust boundaries:

- **Input resources** are assumed potentially adversarial — a malformed or hostile JSON should produce a structured error, never a crash, never code execution.
- **Bundled IG packs** are intended to be verified at the manifest level via sha256. v0.1 ships ONLY placeholder packs (`placeholder: true`, `sha256 = "0" * 64`); `verify_pack_integrity()` deliberately fails closed on placeholders — they have no integrity claim by construction. Real digests + real verification arrive in v0.2 alongside the real IG packs.
- **Manifest tampering** is outside the CLI's defence — verify the wheel signature from PyPI / the GitHub-attested provenance once v0.2 publishes via Trusted Publishing.
- **No network calls** are made by v0.1. v0.3 will introduce optional terminology-server requests; those will require explicit `--tx-server` opt-in.

## Provenance

Bundled IG packs ship with source URL + sha256 in `src/fhir_validator_cli/data/ig-manifest.json`. Run `fhirv manifest` to dump it for supply-chain audit.

## Out-of-scope

- Denial-of-service via extremely large resources is **partially mitigated** in v0.1.1 by the 100 MB input cap (`FHIRV_MAX_RESOURCE_BYTES`); pathological deeply-nested JSON within that cap can still slow validation.
- Side-channel attacks on validation timing.
- Anything involving a FHIR server (this is a CLI; no server surface).

## PHI handling

Issues and pull requests in this repository **must not** contain real patient data. See [CONTRIBUTING.md](CONTRIBUTING.md) for redaction guidance. If a vulnerability report can only be demonstrated against real PHI, email plusultra.dev@proton.me first — do not post the resource in a public issue.
