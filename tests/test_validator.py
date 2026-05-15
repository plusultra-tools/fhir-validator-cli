"""Unit tests for fhir-validator-cli."""

from __future__ import annotations

import json
import unittest

from fhir_validator_cli.igs import list_igs, get_ig, load_manifest
from fhir_validator_cli.validator import validate_resource


VALID_PATIENT = {
    "resourceType": "Patient",
    "id": "example",
    "name": [{"family": "García", "given": ["Ana"]}],
    "gender": "female",
    "birthDate": "1985-03-12",
}

VALID_OBSERVATION = {
    "resourceType": "Observation",
    "id": "obs-1",
    "status": "final",
    "code": {"coding": [{"system": "http://loinc.org", "code": "29463-7"}]},
    "valueQuantity": {"value": 70, "unit": "kg"},
}

INVALID_OBSERVATION_MISSING_STATUS = {
    "resourceType": "Observation",
    "id": "obs-2",
    "code": {"coding": [{"system": "http://loinc.org", "code": "29463-7"}]},
}

INVALID_NO_RESOURCETYPE = {"id": "broken"}


class ValidatorTest(unittest.TestCase):
    def test_valid_patient_passes(self) -> None:
        result = validate_resource(VALID_PATIENT, "hl7-europe-base")
        self.assertTrue(result.valid, msg=f"issues: {result.issues}")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.resource_type, "Patient")

    def test_valid_observation_passes(self) -> None:
        result = validate_resource(VALID_OBSERVATION, "hl7-europe-base")
        self.assertTrue(result.valid, msg=f"issues: {result.issues}")

    def test_observation_missing_status_fails(self) -> None:
        result = validate_resource(INVALID_OBSERVATION_MISSING_STATUS, "hl7-europe-base")
        self.assertFalse(result.valid)
        self.assertEqual(result.exit_code, 1)
        self.assertTrue(any(i.code == "required" and "status" in i.path for i in result.issues))

    def test_missing_resourcetype_fails(self) -> None:
        result = validate_resource(INVALID_NO_RESOURCETYPE, "hl7-europe-base")
        self.assertFalse(result.valid)

    def test_unknown_ig_returns_structured_error(self) -> None:
        result = validate_resource(VALID_PATIENT, "no-such-ig")
        self.assertFalse(result.valid)
        self.assertEqual(result.issues[0].code, "unknown-ig")


class ManifestTest(unittest.TestCase):
    def test_manifest_loads(self) -> None:
        manifest = load_manifest()
        self.assertEqual(manifest["manifest_version"], "1")
        self.assertGreater(len(manifest["igs"]), 0)

    def test_list_igs_returns_expected_names(self) -> None:
        names = {ig.name for ig in list_igs()}
        self.assertIn("hl7-europe-base", names)
        self.assertIn("ips-international", names)
        self.assertIn("ehds-skeleton-pending", names)

    def test_get_ig_roundtrip(self) -> None:
        ig = get_ig("hl7-europe-base")
        self.assertIsNotNone(ig)
        self.assertTrue(ig.placeholder)

    def test_manifest_is_valid_json(self) -> None:
        # round-trip serialisation must not raise
        manifest = load_manifest()
        serialised = json.dumps(manifest)
        self.assertIn("hl7-europe-base", serialised)


if __name__ == "__main__":
    unittest.main()
