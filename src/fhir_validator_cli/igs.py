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


def verify_pack_integrity(name: str, pack_bytes: bytes) -> bool:
    """Check that a pack's bytes match the manifest-declared sha256.

    Returns True for placeholder packs (no integrity claim) when the manifest
    flag is set, otherwise compares against the declared digest.
    """
    ig = get_ig(name)
    if ig is None:
        return False
    if ig.placeholder:
        return True
    return compute_sha256(pack_bytes) == ig.sha256
