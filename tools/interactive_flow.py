#!/usr/bin/env python3
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.gen_spec_ollama import generate_spec
from tools.spec_to_qml import spec_to_qml


def _prompt(text: str) -> str:
    return input(text).strip()


def _yes_no(text: str) -> bool:
    while True:
        value = input(text).strip().lower()
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("y 또는 n으로 입력해주세요.")


def main() -> int:
    print("Figma 디자인 생성용 요구사항을 입력해주세요.")
    print("예: 현재 cpu 사용량, ram 사용량을 보여줄 수 있는 모던한 디자인")
    requirements = _prompt("> ")
    if not requirements:
        print("요구사항이 비어있습니다.")
        return 2

    prompt_path = Path("prompts/figma_spec_prompt.txt")
    model = os.environ.get("OLLAMA_MODEL", "qwen3:8b")
    spec = generate_spec(requirements, prompt_path, model)

    spec_out = Path("specs/out.json")
    spec_out.parent.mkdir(parents=True, exist_ok=True)
    spec_out.write_text(__import__("json").dumps(spec, indent=2), encoding="utf-8")

    print(f"JSON 스펙을 생성했습니다: {spec_out}")
    print("Figma에서 플러그인을 실행해 이 JSON을 붙여넣으면 디자인이 생성됩니다.")

    if _yes_no("생성된 디자인에 맞는 QML을 생성할까요? (y/n) "):
        qml_out = Path("qml/out.qml")
        qml_out.parent.mkdir(parents=True, exist_ok=True)
        qml_out.write_text(spec_to_qml(spec), encoding="utf-8")
        print(f"QML을 생성했습니다: {qml_out}")
        print("미리보기: python tools/run_qml.py qml/out.qml")
    else:
        print("QML 생성은 건너뜁니다.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
