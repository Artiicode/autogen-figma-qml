#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
from pathlib import Path


def _load_prompt(prompt_path: Path, requirements: str) -> str:
    template = prompt_path.read_text(encoding="utf-8")
    return template.replace("{{REQUIREMENTS}}", requirements)


def _extract_code_block(text: str) -> str:
    fence = "```"
    if fence not in text:
        return text
    start = text.find(fence)
    end = text.rfind(fence)
    if end <= start:
        return text
    block = text[start + len(fence) : end].strip()
    if "\n" in block:
        first, rest = block.split("\n", 1)
        if first.strip().lower() in {"json", "text"}:
            return rest.strip()
    return block.strip()


def _extract_json_objects(text: str) -> list[str]:
    objects = []
    depth = 0
    start = None
    in_string = False
    escape = False

    for i, ch in enumerate(text):
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == "\"":
                in_string = False
            continue

        if ch == "\"":
            in_string = True
            continue
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    objects.append(text[start : i + 1])
                    start = None

    return objects


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
    if not raw:
        raise RuntimeError("ollama returned empty output. Check that the model is pulled and running.")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        cleaned = _extract_code_block(raw)
        objects = _extract_json_objects(cleaned)
        for candidate in reversed(objects):
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue

        debug_path = Path("specs/last_ollama_output.txt")
        debug_path.parent.mkdir(parents=True, exist_ok=True)
        debug_path.write_text(raw, encoding="utf-8")
        raise ValueError(
            f"Failed to parse JSON from model output. Raw output saved to {debug_path}."
        )


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
