#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
from pathlib import Path


def _load_prompt(prompt_path: Path, requirements: str) -> str:
    template = prompt_path.read_text(encoding="utf-8")
    return template.replace("{{REQUIREMENTS}}", requirements)


def _extract_json(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model output.")
    return text[start : end + 1]


def generate_spec(requirements: str, prompt_path: Path, model: str) -> dict:
    prompt = _load_prompt(prompt_path, requirements)
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ollama run failed")

    raw = result.stdout.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        extracted = _extract_json(raw)
        return json.loads(extracted)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Figma JSON spec via Ollama")
    parser.add_argument("--requirements", help="Requirements text")
    parser.add_argument("--requirements-file", help="Path to a text file with requirements")
    parser.add_argument("--prompt", default="prompts/figma_spec_prompt.txt", help="Prompt template path")
    parser.add_argument("--model", default=os.environ.get("OLLAMA_MODEL", "qwen3:8b"))
    parser.add_argument("--out", default="specs/out.json", help="Output JSON path")
    args = parser.parse_args()

    if not args.requirements and not args.requirements_file:
        parser.error("Provide --requirements or --requirements-file")

    requirements = args.requirements
    if args.requirements_file:
        requirements = Path(args.requirements_file).read_text(encoding="utf-8").strip()

    prompt_path = Path(args.prompt)
    spec = generate_spec(requirements, prompt_path, args.model)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
