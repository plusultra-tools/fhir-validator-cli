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

## [0.1.0] - 2026-05-14

### Added
- Initial release: CLI surface (`validate`, `list-igs`, `manifest` subcommands).
- Manifest format for bundled IG packs (name, version, source URL, sha256, last-updated).
- Placeholder IGs for hl7-europe-base, ips-international, mcsd, ehds-skeleton-pending.
- Structural + minimum-cardinality validation for Patient, Bundle, Observation, Encounter, Condition.
- Structured-error JSON on stdout (CI-friendly).
- MIT license.
- pytest matrix on py3.10/3.11/3.12.
