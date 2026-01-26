#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.gen_spec_ollama import generate_spec
from tools.spec_to_qml import spec_to_qml


def main() -> int:
    parser = argparse.ArgumentParser(description="Requirements -> spec -> QML")
    parser.add_argument("--requirements", help="Requirements text")
    parser.add_argument("--requirements-file", help="Path to a text file with requirements")
    parser.add_argument("--prompt", default="prompts/figma_spec_prompt.txt")
    parser.add_argument("--model", default=None)
    parser.add_argument("--spec-out", default="specs/out.json")
    parser.add_argument("--qml-out", default="qml/out.qml")
    args = parser.parse_args()

    if not args.requirements and not args.requirements_file:
        parser.error("Provide --requirements or --requirements-file")

    requirements = args.requirements
    if args.requirements_file:
        requirements = Path(args.requirements_file).read_text(encoding="utf-8").strip()

    model = args.model or os.environ.get("OLLAMA_MODEL", "qwen3:8b")

    prompt_path = Path(args.prompt)
    spec = generate_spec(requirements, prompt_path, model)

    spec_out = Path(args.spec_out)
    spec_out.parent.mkdir(parents=True, exist_ok=True)
    spec_out.write_text(__import__("json").dumps(spec, indent=2), encoding="utf-8")

    qml_out = Path(args.qml_out)
    qml_out.parent.mkdir(parents=True, exist_ok=True)
    qml_out.write_text(spec_to_qml(spec), encoding="utf-8")

    print(f"Wrote {spec_out}")
    print(f"Wrote {qml_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
