#!/usr/bin/env python3
"""Print the selected proof path only after validating its build identity."""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fontlab.identity import verified_manifest  # noqa: E402
from fontlab.recipes import PROJECT_PATH, load_project  # noqa: E402
from fontlab.inter_source import load_project as load_inter_project  # noqa: E402
import json

parser = argparse.ArgumentParser()
parser.add_argument("--project", type=Path, default=PROJECT_PATH)
parser.add_argument("--output-dir", type=Path, default=ROOT / "build")
args = parser.parse_args()
raw = args.project.read_bytes()
if len(raw) > 65536:
    raise ValueError("project exceeds 65536 bytes")
selected = json.loads(raw.decode("utf-8"))
if not isinstance(selected, dict):
    raise ValueError("project JSON must be an object")
version = selected.get("schemaVersion")
project = load_inter_project(args.project) if version == 3 else load_project(args.project)
instance, manifest = verified_manifest(project, args.output_dir)
print(instance / manifest["proof"])
