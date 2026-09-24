"""Content identity for compiled proofs and their generating code."""

from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE_FILES = (
    "fontlab/recipes.py",
    "fontlab/recipes_v1.py",
    "fontlab/identity.py",
    "fontlab/inter_source.py",
    "tools/build_font.py",
    "tools/build_inter_font.py",
    "vendor/inter/InterVariable.ttf",
    "vendor/inter/LICENSE.txt",
    "web/fonts/PFLSansVariable.woff2",
    "requirements.lock",
)


def engine_hash(root: Path = ROOT, files: tuple[str, ...] = ENGINE_FILES) -> str:
    digest = sha256()
    for name in files:
        digest.update(name.encode("utf-8") + b"\0")
        digest.update((root / name).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def build_id(project_hash: str, revision: str) -> str:
    return sha256(f"{project_hash}:{revision}".encode("ascii")).hexdigest()


def verified_manifest(project: dict, output_dir: Path, revision: str | None = None) -> tuple[Path, dict]:
    from fontlab.recipes import source_hash

    project_hash = source_hash(project)
    revision = revision or engine_hash()
    identity = build_id(project_hash, revision)
    instance = output_dir / identity
    try:
        manifest = json.loads((instance / "manifest.json").read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError("compiled proof is missing or stale; run npm run export for this project and engine") from error
    if (manifest.get("project"), manifest.get("sourceHash"), manifest.get("engineHash"), manifest.get("buildId")) != (project["id"], project_hash, revision, identity):
        raise ValueError("compiled proof identity differs from selected project or engine")
    paths = manifest.get("fonts", [])
    hashes = manifest.get("binaryHashes", {})
    if not paths or not any(path.endswith(".woff2") for path in paths):
        raise ValueError("compiled proof lacks a WOFF2 font")
    for name in paths:
        path = (instance / name).resolve()
        if not path.is_relative_to(instance.resolve()):
            raise ValueError("compiled font path escapes its instance")
        if not path.is_file() or sha256(path.read_bytes()).hexdigest() != hashes.get(name):
            raise ValueError(f"compiled font is missing or changed: {name}")
    proof = (instance / manifest.get("proof", "")).resolve()
    if not proof.is_relative_to(instance.resolve()) or not proof.is_file():
        raise ValueError("compiled specimen is missing")
    if sha256(proof.read_bytes()).hexdigest() != manifest.get("proofHash"):
        raise ValueError("compiled specimen was changed")
    if manifest.get("licenseFile"):
        license_path = (instance / manifest["licenseFile"]).resolve()
        if not license_path.is_relative_to(instance.resolve()) or not license_path.is_file() or sha256(license_path.read_bytes()).hexdigest() != manifest.get("licenseHash"):
            raise ValueError("compiled font license is missing or changed")
    return instance, manifest
