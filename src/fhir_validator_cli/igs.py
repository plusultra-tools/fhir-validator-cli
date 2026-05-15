"""Implementation Guide pack metadata + manifest loading.

The manifest is the single source of truth for which IGs the wheel ships,
their versions, source URLs, and tamper-evident sha256 of each pack.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class IgPack:
    """Metadata for one bundled Implementation Guide pack."""

    name: str
    version: str
    source_url: str
    sha256: str
    last_updated: str
    description: str
    placeholder: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "source_url": self.source_url,
            "sha256": self.sha256,
            "last_updated": self.last_updated,
            "description": self.description,
            "placeholder": self.placeholder,
        }


def _manifest_path() -> Path:
    """Return the path to the bundled ig-manifest.json."""
    with resources.as_file(
        resources.files("fhir_validator_cli.data").joinpath("ig-manifest.json")
    ) as p:
        return Path(p)


def load_manifest() -> dict[str, Any]:
    """Load and return the raw manifest JSON."""
    path = _manifest_path()
    with path.open("r", encoding="utf-8") as fh:
        result: dict[str, Any] = json.load(fh)
        return result


def list_igs() -> list[IgPack]:
    """Return the list of IG packs declared in the bundled manifest."""
    manifest = load_manifest()
    return [IgPack(**entry) for entry in manifest.get("igs", [])]


def get_ig(name: str) -> IgPack | None:
    """Look up a single IG by name."""
    for ig in list_igs():
        if ig.name == name:
            return ig
    return None


def compute_sha256(data: bytes) -> str:
    """Compute sha256 hex digest of arbitrary bytes (used for pack provenance)."""
    return hashlib.sha256(data).hexdigest()


def verify_pack_integrity(
    name: str, pack_bytes: bytes, *, allow_placeholder: bool = False
) -> bool:
    """Check that a pack's bytes match the manifest-declared sha256.

    Fail-closed by default: when an IG is flagged ``placeholder: true`` in the
    manifest, integrity CANNOT be verified (no real digest exists) and this
    function returns ``False``. Callers must opt in to the placeholder path
    with ``allow_placeholder=True`` and handle the "no verification possible"
    case explicitly — this prevents a supply-chain hole where an attacker
    re-flags a tampered real pack as placeholder to bypass verification.

    Returns:
        ``True``  iff the pack's sha256 matches the manifest entry AND the
                  manifest entry is not a placeholder.
        ``False`` for unknown IGs, placeholder IGs (unless explicitly opted-in,
                  in which case still ``False`` — placeholders have no integrity
                  claim by construction), or sha256 mismatches.
    """
    ig = get_ig(name)
    if ig is None:
        return False
    if ig.placeholder:
        # Placeholder entries carry sha256 = "0" * 64 (no real digest).
        # Even if a caller opts in, we cannot truthfully say "verified",
        # so we always return False and let the caller branch on the
        # placeholder flag via get_ig(name).placeholder if it wants to
        # accept the pack without verification.
        return False
    return compute_sha256(pack_bytes) == ig.sha256
