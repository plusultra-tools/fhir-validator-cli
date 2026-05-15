# Security policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.1.x   | yes       |
| < 0.1   | no        |

## Reporting a vulnerability

Email **plusultra.dev@proton.me** with subject `[fhir-validator-cli] security`. Do **not** open a public GitHub issue for security findings.

Expected response: acknowledgement within 72 hours, triage within 7 days, fix or mitigation within 30 days for high-severity issues.

## Threat model

`fhir-validator-cli` is a local CLI that parses FHIR JSON resources supplied by the user. Trust boundaries:

- **Input resources** are assumed potentially adversarial — a malformed or hostile JSON should produce a structured error, never a crash, never code execution.
- **Bundled IG packs** are signed at the manifest level via sha256. Tampering with a bundled pack will be detected by `verify_pack_integrity()`. Tampering with the manifest itself is outside the CLI's defence — verify the wheel signature from PyPI.
- **No network calls** are made by v0.1. v0.3 will introduce optional terminology-server requests; those will require explicit `--tx-server` opt-in.

## Provenance

Bundled IG packs ship with source URL + sha256 in `src/fhir_validator_cli/data/ig-manifest.json`. Run `fhirv manifest` to dump it for supply-chain audit.

## Out-of-scope

- Denial-of-service via extremely large resources (we recommend a 100 MB input cap in your own pipeline).
- Side-channel attacks on validation timing.
- Anything involving a FHIR server (this is a CLI; no server surface).
