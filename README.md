# fhir-validator-cli

**Zero-config FHIR R4/R5 validator with bundled EU Implementation Guide packs.** One `pip install` and you can validate Patient/Encounter/Observation/Bundle resources against HL7 Europe Base, IPS, mCSD, and the EHDS skeleton (when published) — no fetching IGs from six different registries first.

```bash
pip install fhir-validator-cli
fhirv validate patient.json --ig hl7-europe-base
```

---

## Why this exists

The European Health Data Space (EHDS) regulation forces hospitals, regional health authorities, and digital-health vendors to submit FHIR resources conformant to a specific stack of EU-flavoured IGs:

- **HL7 Europe Base** — the floor profile for any EU-wide FHIR exchange.
- **IPS (International Patient Summary)** — cross-border patient summaries.
- **mCSD (Care Services Discovery)** — provider directory exchange.
- **EHDS skeleton** — the secondary-use submission profile (draft as of 2026; will be mandatory).

The existing toolchain is split:

- **HAPI FHIR validator** (Java) — heavy, server-grade, mature, but you have to fetch each IG package yourself from `simplifier.net` / `build.fhir.org` / various national registries. Wires up in 1-2 days the first time.
- **fhir.js / fhirpath.js** (Node) — runtime-validation oriented, no CLI-first DX.
- **Inferno** — testing harness for FHIR servers, not a CLI.

We close the gap. `fhirv` ships **the EU IG packs bundled inside the wheel**, with a tamper-evident manifest (sha256 of each pack + provenance URL), so CI pipelines can do `pip install && fhirv validate` and get a meaningful exit code in <2 seconds.

## What it does

1. `pip install fhir-validator-cli` — single dependency, pure Python, no JVM.
2. `fhirv validate resource.json --ig hl7-europe-base` — validates a FHIR resource or Bundle against a named bundled IG.
3. Exit code `0` if valid; exit code `1` and structured-error JSON to stdout if not. Designed for CI: redirect stdout, parse with `jq`, fail the build.
4. `fhirv list-igs` — prints the bundled IGs with version + last-updated + sha256.
5. `fhirv manifest` — dumps the full IG manifest (source URL, version, sha256 of each pack) so you can audit provenance in your supply chain.

## What it does NOT do

- Not a replacement for **HAPI FHIR validator** when you need server-side, terminology-server-backed, real-time validation. HAPI remains the reference for that path.
- No bundled FHIR server, no REST endpoints, no UI. CLI-first, single binary mindset.
- No terminology expansion against external $expand operations in v0.1. (v0.3 will allow plugging a tx-server URL.)
- No code-system normalisation. Garbage in, garbage out at the terminology layer.

## Bundled IGs (v0.1)

> v0.1 ships the manifest format and **one placeholder IG** (`hl7-europe-base@0.0.1-placeholder`) so the CLI surface is exercised end-to-end. v0.2 will bundle the real packs once the legal review on redistribution clears. The schedule below is the target for v0.2.

| Name | Version | Source URL | sha256 (target v0.2) |
|---|---|---|---|
| `hl7-europe-base` | 0.1.0 (v0.2 target: 1.0.0) | https://build.fhir.org/ig/hl7-eu/base/ | (pending v0.2) |
| `ips-international` | 0.1.0 (v0.2 target: 2.0.0-ballot) | https://hl7.org/fhir/uv/ips/ | (pending v0.2) |
| `mcsd` | 0.1.0 (v0.2 target: 1.0.0) | https://hl7.org/fhir/uv/mcsd/ | (pending v0.2) |
| `ehds-skeleton-pending` | 0.0.1 | https://health.ec.europa.eu/ehealth-digital-health-and-care/european-health-data-space_en | (skeleton, EHDS profile not yet published) |

The actual values are kept in `src/fhir_validator_cli/data/ig-manifest.json`, which is the single source of truth. Run `fhirv manifest` to dump it.

## Roadmap

- **v0.1 (this release)** — CLI surface, manifest format, placeholder IG, structured validation errors, JSON-Schema-level checks.
- **v0.2** — Real EU IG packs bundled, full StructureDefinition walk.
- **v0.3** — Optional terminology-server plug, SNOMED CT subset validation, custom-profile loading.
- **v1.0** — Stable wire format for the structured-error JSON; semver guarantees.

## Pricing

- **CLI: MIT, free, forever.**
- **Hosted CI-as-a-service (planned)** — €19/mo (solo) to €49/mo (team). Same validation, but webhook-driven, dashboards, slack alerts, audit log. Stripe-billed when the demand signal justifies it.

## Audience

- FHIR engineers at EU hospital groups, regional health authorities, EHDS National Contact Points.
- HL7 Europe affiliate working groups.
- Digital-health vendors integrating to EU FHIR endpoints.
- Distribution channels: **r/HL7**, **HL7 Europe Slack**, **dev.to**, **awesome-fhir** GitHub list, EHDS engineering mailing lists.

## Contributing

Open an issue with a real resource that fails validation but should pass (or vice versa). PRs welcome — especially for additional EU national IGs (Spain HL7-ES, France ANS, Germany MIO/KBV).

## License

MIT. See [LICENSE](LICENSE).
