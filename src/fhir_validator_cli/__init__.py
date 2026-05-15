"""fhir-validator-cli: zero-config FHIR R4/R5 validator with bundled EU IG packs."""

from fhir_validator_cli.validator import ValidationResult, validate_resource
from fhir_validator_cli.igs import list_igs, get_ig, load_manifest

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "ValidationResult",
    "validate_resource",
    "list_igs",
    "get_ig",
    "load_manifest",
]
