"""Command-line entry point for fhirv."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from fhir_validator_cli import __version__
from fhir_validator_cli.igs import list_igs, load_manifest
from fhir_validator_cli.validator import validate_resource


def _cmd_validate(args: argparse.Namespace) -> int:
    """Validate a FHIR resource file against a named IG."""
    resource_path = Path(args.resource)
    if not resource_path.exists():
        print(json.dumps({"error": f"file not found: {resource_path}"}), file=sys.stderr)
        return 2
    try:
        with resource_path.open("r", encoding="utf-8") as fh:
            resource = json.load(fh)
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": f"invalid JSON: {exc}"}), file=sys.stderr)
        return 2

    result = validate_resource(resource, args.ig)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return result.exit_code


def _cmd_list_igs(_args: argparse.Namespace) -> int:
    """Print bundled IGs as a small human-readable table."""
    igs = list_igs()
    if not igs:
        print("(no IGs bundled)")
        return 0
    print(f"{'NAME':30}{'VERSION':15}{'LAST_UPDATED':15}{'PLACEHOLDER'}")
    for ig in igs:
        flag = "yes" if ig.placeholder else "no"
        print(f"{ig.name:30}{ig.version:15}{ig.last_updated:15}{flag}")
    return 0


def _cmd_manifest(_args: argparse.Namespace) -> int:
    """Dump the raw IG manifest JSON (provenance audit)."""
    manifest = load_manifest()
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argparse parser."""
    parser = argparse.ArgumentParser(
        prog="fhirv",
        description=(
            "Zero-config FHIR R4/R5 validator with bundled EU IG packs "
            "(HL7 Europe Base, IPS, mCSD, EHDS skeleton)."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"fhirv {__version__}"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_validate = subparsers.add_parser(
        "validate",
        help="Validate a FHIR resource JSON file against a bundled IG.",
    )
    p_validate.add_argument("resource", help="Path to a FHIR resource JSON file.")
    p_validate.add_argument(
        "--ig",
        default="hl7-europe-base",
        help="Name of the IG to validate against (default: hl7-europe-base).",
    )
    p_validate.set_defaults(func=_cmd_validate)

    p_list = subparsers.add_parser(
        "list-igs", help="List bundled IGs with version + last-updated."
    )
    p_list.set_defaults(func=_cmd_list_igs)

    p_manifest = subparsers.add_parser(
        "manifest", help="Dump the raw IG manifest JSON for provenance audit."
    )
    p_manifest.set_defaults(func=_cmd_manifest)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Returns process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    exit_code: int = args.func(args)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
