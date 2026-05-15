# Contributing to fhir-validator-cli

Thanks for the interest. This is a v0.1 scaffold (see README "Status") — most of the validator does not exist yet, so contributions today are mostly bug reports on the CLI surface, manifest-format feedback, and pointers to EU national IGs for the v0.2 scope.

## Dev install

```bash
git clone https://github.com/plusultra-tools/fhir-validator-cli
cd fhir-validator-cli
python -m pip install -e ".[dev]"
```

## Run tests

```bash
python -m unittest discover -v tests
```

CI runs the same on py3.10 / 3.11 / 3.12 (Linux).

## Reporting bugs

Open a GitHub issue. **Do NOT paste real patient data (PHI).** If a bug only reproduces on a real resource:

1. Strip the resource to the minimum that still triggers the bug.
2. Replace all `Patient.name`, `Patient.identifier`, `Patient.birthDate`, `Patient.address`, `Patient.telecom`, free-text `note`/`comment`/`text.div` fields, and any extension carrying personal data with synthetic values.
3. If you cannot redact without losing the repro, see `SECURITY.md` for the private disclosure channel.

We will close issues that contain unredacted real PHI and ask you to re-open with a synthetic example.

## Code style

- Python 3.10+ type hints required on every public function.
- `from __future__ import annotations` at the top of each module.
- No new runtime dependencies without discussion (pure-stdlib + `jsonschema` is the budget for v0.1; v0.2 may add IG-pack tooling).
- Tests live in `tests/`, named `test_*.py`, use `unittest`.

## PR checklist

- [ ] Tests pass locally (`python -m unittest discover -v tests`).
- [ ] No real PHI in fixtures, examples, or commit messages.
- [ ] CHANGELOG.md updated under `[Unreleased]`.
- [ ] If the PR touches `data/ig-manifest.json`, the sha256 fields are either real digests (not zero) or the `placeholder: true` flag is set.

## License

Contributions are accepted under the MIT license (see LICENSE).
