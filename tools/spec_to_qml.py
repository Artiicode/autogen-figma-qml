#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def _qml_color(color: str) -> str:
    if not color:
        return "#FFFFFF"
    return color


def _qml_string(value: str) -> str:
    return value.replace("\\\\", "\\\\\\\\").replace("\"", "\\\\\"")


def spec_to_qml(spec: dict) -> str:
    width = spec.get("width", 800)
    height = spec.get("height", 600)
    title = spec.get("name", "Auto GUI")

    lines = [
        "import QtQuick 2.15",
        "import QtQuick.Controls 2.15",
        "",
        "ApplicationWindow {",
        f"    width: {width}",
        f"    height: {height}",
        "    visible: true",
        f"    title: \"{title}\"",
        "",
    ]

    for child in spec.get("children", []):
        ctype = child.get("type")
        if ctype == "rect":
            lines.extend(
                [
                    "    Rectangle {",
                    f"        x: {child.get('x', 0)}",
                    f"        y: {child.get('y', 0)}",
                    f"        width: {child.get('width', 100)}",
                    f"        height: {child.get('height', 100)}",
                    f"        radius: {child.get('radius', 0)}",
                    f"        color: \"{_qml_color(child.get('fill'))}\"",
                    "    }",
                    "",
                ]
            )
        elif ctype == "text":
            text_value = _qml_string(child.get("text", ""))
            lines.extend(
                [
                    "    Text {",
                    f"        x: {child.get('x', 0)}",
                    f"        y: {child.get('y', 0)}",
                    f"        text: \"{text_value}\"",
                    f"        font.pixelSize: {child.get('fontSize', 16)}",
                    f"        color: \"{_qml_color(child.get('color'))}\"",
                    "    }",
                    "",
                ]
            )

    lines.append("}")
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: spec_to_qml.py spec.json out.qml")
        return 2

    spec_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    qml = spec_to_qml(spec)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(qml, encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
