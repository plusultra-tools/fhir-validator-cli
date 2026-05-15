# Carrd landing-page copy — fhir-validator-cli

## Hero

**Validate FHIR against EU IGs in one `pip install`.**

`fhirv validate patient.json --ig hl7-europe-base` — exit 0 if valid, structured-error JSON if not. HL7 Europe Base, IPS, mCSD, EHDS skeleton: bundled, sha256-verified, no IG-fetching scavenger hunt.

[Install from PyPI →](https://pypi.org/project/fhir-validator-cli/)  [GitHub →](https://github.com/plusultra/fhir-validator-cli)

---

## Sub-hero (one paragraph)

The HAPI FHIR validator is excellent — and a Java dependency, plus a half-day of fetching IG packages from six registries before the first run. `fhirv` is the CLI-first complement: pure Python, no JVM, EU IGs in the wheel, designed for CI pipelines that need to fail builds on non-conformant resources. MIT-licensed, hosted CI-as-a-service planned (€19–49/mo).

---

## Three-card row

**Zero config.** `pip install fhir-validator-cli`. No simplifier.net account. No `package.json` for FHIR registries. Bundled IGs ship inside the wheel.

**EHDS-aware.** HL7 Europe Base, IPS, mCSD ship today. EHDS secondary-use skeleton tracked from draft. The IGs your CI will need next year.

**CI-native.** Stdout is JSON. Exit code is 0 or 1. Drop it in GitHub Actions, GitLab CI, Jenkins. No daemons, no servers.

---

## Audience CTA

Built FHIR pipelines for an EU hospital / regional authority / national EHDS contact point?

[Tell me what IG you wish was bundled →](mailto:plusultra.dev@proton.me?subject=fhir-validator-cli)

---

## Footer

MIT-licensed. Built for r/HL7 and HL7 Europe Slack. v0.1 ships the manifest + CLI surface; v0.2 bundles real EU IG packs.
