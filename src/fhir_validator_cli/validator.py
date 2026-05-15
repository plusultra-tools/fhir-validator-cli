"""Thin FHIR resource validator.

v0.1: structural + minimum-cardinality checks via a hand-rolled JSON schema
for the FHIR base types most likely to show up in EHDS submissions. v0.2
will swap this for full StructureDefinition walks against the bundled IG
packs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from fhir_validator_cli.igs import get_ig


# Minimal FHIR R4/R5 base schema covering the fields we can reasonably
# check without the full StructureDefinition. Intentionally permissive so
# valid resources pass; targeted checks fail loud.
_BASE_RESOURCE_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["resourceType"],
    "properties": {
        "resourceType": {"type": "string", "minLength": 1},
        "id": {"type": "string"},
        "meta": {"type": "object"},
        "language": {"type": "string"},
        "text": {"type": "object"},
    },
}


# Per-resourceType extra required fields. Conservative — only the ones
# whose absence is universally an EHDS-submission blocker.
_REQUIRED_FIELDS_BY_TYPE: dict[str, list[str]] = {
    "Patient": [],  # Patient has no truly required fields per spec
    "Bundle": ["type"],
    "Observation": ["status", "code"],
    "Encounter": ["status"],
    "Condition": ["subject"],
}


@dataclass
class ValidationIssue:
    """One validation finding."""

    severity: str  # "error" | "warning" | "information"
    code: str
    path: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "path": self.path,
            "message": self.message,
        }


@dataclass
class ValidationResult:
    """Outcome of validating one resource against one IG."""

    valid: bool
    resource_type: str
    ig_name: str
    ig_version: str
    issues: list[ValidationIssue] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "resourceType": self.resource_type,
            "ig": {"name": self.ig_name, "version": self.ig_version},
            "issues": [i.to_dict() for i in self.issues],
        }

    @property
    def exit_code(self) -> int:
        return 0 if self.valid else 1


def _check_required_fields(resource: dict[str, Any]) -> list[ValidationIssue]:
    rtype = resource.get("resourceType", "")
    required = _REQUIRED_FIELDS_BY_TYPE.get(rtype, [])
    issues: list[ValidationIssue] = []
    for field_name in required:
        if field_name not in resource:
            issues.append(
                ValidationIssue(
                    severity="error",
                    code="required",
                    path=f"{rtype}.{field_name}",
                    message=f"Required field '{field_name}' missing on {rtype}",
                )
            )
    return issues


def _check_schema(resource: dict[str, Any]) -> list[ValidationIssue]:
    validator = Draft202012Validator(_BASE_RESOURCE_SCHEMA)
    issues: list[ValidationIssue] = []
    for err in sorted(validator.iter_errors(resource), key=lambda e: list(e.absolute_path)):
        path = ".".join(str(p) for p in err.absolute_path) or "(root)"
        issues.append(
            ValidationIssue(
                severity="error",
                code="schema",
                path=path,
                message=err.message,
            )
        )
    return issues


def validate_resource(resource: dict[str, Any], ig_name: str) -> ValidationResult:
    """Validate a parsed FHIR resource against a named bundled IG.

    Returns a ValidationResult with .exit_code suitable for CLI use.
    """
    ig = get_ig(ig_name)
    if ig is None:
        return ValidationResult(
            valid=False,
            resource_type=resource.get("resourceType", "(unknown)"),
            ig_name=ig_name,
            ig_version="(not-found)",
            issues=[
                ValidationIssue(
                    severity="error",
                    code="unknown-ig",
                    path="(root)",
                    message=f"Unknown IG '{ig_name}'. Run 'fhirv list-igs' for available IGs.",
                )
            ],
        )

    issues = _check_schema(resource) + _check_required_fields(resource)
    return ValidationResult(
        valid=not any(i.severity == "error" for i in issues),
        resource_type=resource.get("resourceType", "(unknown)"),
        ig_name=ig.name,
        ig_version=ig.version,
        issues=issues,
    )
