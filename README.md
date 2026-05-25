# fhir-validator-cli

[![tests](https://github.com/plusultra-tools/fhir-validator-cli/actions/workflows/test.yml/badge.svg)](https://github.com/plusultra-tools/fhir-validator-cli/actions/workflows/test.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha%20scaffold-orange)](#status)

> v0.1 scaffold for a CLI that will validate FHIR R4/R5 resources against bundled EU Implementation Guide packs. **Today this is NOT a conformance validator** — see [Status](#status) below.

---

## Status (read this first)

**v0.1 is a CLI scaffold and manifest format.** It does not perform real IG conformance validation. Specifically:

- The 4 bundled IGs declared in the manifest (`hl7-europe-base`, `ips-international`, `mcsd`, `ehds-skeleton-pending`) are **placeholders** with `sha256 = 0` and `placeholder: true`. No StructureDefinition content ships.
- The validator runs a minimal structural sanity check: every resource must have a `resourceType` field plus a tiny hand-coded required-field map covering 5 resource types (Patient, Bundle, Observation, Encounter, Condition) with a total of ~6 required fields. No terminology check, no cardinality beyond required/not-required, no slicing, no fixed-value, no must-support, no invariants, no profile walk.
- Almost any resource you throw at it will return `"valid": true`. That is **expected behaviour for v0.1**, not a bug.

**Use this today only as:** a smoke test for the CLI surface, an example of the manifest format, a fixture for downstream tooling that needs *some* `fhirv`-compatible binary on `$PATH`. Do **not** rely on `"valid": true` as evidence of IG conformance.

Real IG-level validation is scheduled for v0.2.

If you need production-grade FHIR validation today, use **HAPI FHIR ValidationCLI** ([docs](https://hapifhir.io/hapi-fhir/docs/validation/instance_validator.html)) or **Firely .NET SDK / firely-terminal**.

---

## Install

```bash
pip install fhir-validator-cli   # not yet on PyPI; install from source for now
```

From source:

```bash
git clone https://github.com/plusultra-tools/fhir-validator-cli
cd fhir-validator-cli
pip install -e ".[dev]"
```

## CLI surface (v0.1)

```bash
fhirv validate patient.json --ig hl7-europe-base   # base-shape check only (see Status)
fhirv list-igs                                     # list bundled IGs (all placeholders today)
fhirv manifest                                     # dump the raw IG manifest JSON
fhirv --version
```

Exit code `0` on pass, `1` on fail, `2` on user error (file not found / invalid JSON).

## What v0.1 does NOT do

- Does **not** walk StructureDefinitions.
- Does **not** ship real EU IG content — all bundled IGs are placeholders.
- Does **not** do terminology expansion (`$expand`, SNOMED CT, LOINC, ICD-10).
- Does **not** cover most of the ~150 FHIR R4 resources — only 5 have any required-field rules.
- Does **not** validate against `meta.profile`.
- Does **not** offer `--strict`, `--profile`, `--severity-filter` flags.
- Does **not** replace HAPI FHIR validator, Firely .NET SDK / firely-terminal, or Inferno.

## Roadmap

- **v0.1 (this release)** — CLI surface + manifest format + base structural sanity check.
- **v0.2** — Real EU IG packs bundled (hl7-europe-base first), full StructureDefinition walk, `--strict`, `--profile` flags, generated required-fields map from FHIR R4 metadata covering all resources.
- **v0.3** — Optional terminology-server plug (`--tx-server`), SNOMED CT subset validation, custom-profile loading.
- **v1.0** — Stable wire format for structured-error JSON, semver guarantees.

## Why this might eventually exist

The European Health Data Space (EHDS) regulation (entered into force 2025; phased in 2026-2031) will require FHIR resources conformant to a stack of EU-flavoured IGs (HL7 Europe Base, IPS, mCSD, an EHDS-specific submission profile). Today the toolchain for that workflow is fragmented: HAPI FHIR validator (Java, heavy, requires fetching each IG pack from `simplifier.net` / national registries) and the Firely .NET stack (Windows-first, .NET runtime).

The wedge — *if* this venture survives to v0.2 — is a pure-Python wheel with EU IG packs bundled, suitable for `pip install && fhirv validate` in a Linux CI runner with no JVM and no first-run network fetch. v0.1 ships only the wrapper.

## Audience (target, not validated)

FHIR engineers at EU hospital integration teams who already run Python in CI and want a faster smoke test than spinning up HAPI.

Until at least one such engineer files an issue or starts a discussion, the target audience is **hypothetical**. See `kill-gate.md` (operator-internal) for the 30-day demand-signal threshold.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues welcome, especially:

- Bug reports against the v0.1 CLI surface (`--help`, exit codes, JSON output shape).
- Feedback on the manifest format before v0.2 locks it in.
- Pointers to EU national IGs (Spain HL7-ES, France ANS, Germany MIO/KBV) that should be in scope for v0.2.

## Security

See [SECURITY.md](SECURITY.md) for the vulnerability disclosure policy.

## License

MIT. See [LICENSE](LICENSE).

## Trademarks

FHIR® and HL7® are registered trademarks of Health Level Seven International. This project is not affiliated with HL7. References to IPS, mCSD, and EHDS are nominative use of standard names.
