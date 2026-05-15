# Changelog

All notable changes to this project will be documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned for v0.2
- Bundle real EU IG packs (hl7-europe-base, ips-international, mcsd) with sha256 provenance.
- Full StructureDefinition walk (replacing the v0.1 JSON-Schema-level checks).
- `--strict` mode that promotes warnings to errors.

### Planned for v0.3
- Optional terminology-server URL for `$expand`-backed code validation.
- Custom-profile loading from a local IG directory.
- SNOMED CT subset validation hooks.

## [0.1.0] - 2026-05-15

### Added
- Initial release: CLI surface (`validate`, `list-igs`, `manifest` subcommands).
- Manifest format for bundled IG packs (name, version, source URL, sha256, last-updated).
- Placeholder IGs for hl7-europe-base, ips-international, mcsd, ehds-skeleton-pending
  (no real StructureDefinition content; see README "Status").
- Minimal structural sanity check for Patient, Bundle, Observation, Encounter, Condition.
  NOT a conformance validator — see README.
- Structured-error JSON on stdout (CI-friendly).
- MIT license.
- pytest matrix on py3.10/3.11/3.12.

### Security
- `verify_pack_integrity()` now fails closed on placeholder packs (previously
  returned True for any bytes when `placeholder=true`; would have been a
  supply-chain hole in v0.2 once real packs ship).
- GitHub Actions SHA-pinned (`actions/checkout`, `actions/setup-python`).
- Dependabot enabled for github-actions + pip ecosystems.
