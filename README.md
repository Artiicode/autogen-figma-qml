# Auto GUI (Figma -> QML)

This repo provides a lightweight pipeline to:

1) turn a structured design spec into a Figma file (via a small Figma plugin)
2) test generated QML without a commercial Qt license (via Qt for Python)

Notes:
- The official Figma MCP server exposes read-only design context tools (no create/update tools). To create designs programmatically, Figma recommends using the Plugin API, so this repo includes a minimal plugin that can build a frame from JSON spec input.
- For QML preview without a commercial Qt license, you can use the Qt for Python Community Edition (PySide6) which provides QML runtimes and the `pyside6-qml` tool.

## Contents

- `figma_plugin/`: Figma plugin that creates a frame from JSON spec.
- `prompts/`: prompt template for generating JSON spec from requirements.
- `specs/`: example JSON spec.
- `qml/`: sample QML file.
- `tools/run_qml.py`: QML runner using PySide6.
- `tools/gen_spec_ollama.py`: generate JSON spec from requirements via Ollama.
- `tools/spec_to_qml.py`: convert JSON spec to QML.
- `tools/pipeline.py`: end-to-end helper (requirements -> spec -> QML).
- `tools/figma_mcp_fetch.py`: fetch MCP tool output to a file.
- `tools/figma_to_qml.py`: use MCP + Ollama to generate QML from Figma context.
- `tools/interactive_flow.py`: interactive flow for requirements -> spec -> optional QML.
- `docs/mcp.md`: notes on Figma MCP capabilities and constraints.

## Figma plugin (create design from JSON spec)

1) In Figma desktop, open any design file.
2) Menu: Plugins -> Development -> Import plugin from manifest...
3) Select `figma_plugin/manifest.json`.
4) Run the plugin, paste your JSON spec, click Build.

JSON spec example:

{
  "name": "MainFrame",
  "width": 900,
  "height": 600,
  "children": [
    {
      "type": "rect",
      "name": "Hero",
      "x": 40,
      "y": 40,
      "width": 820,
      "height": 240,
      "fill": "#F2F2F2",
      "radius": 24
    },
    {
      "type": "text",
      "name": "Title",
      "x": 60,
      "y": 70,
      "text": "Auto GUI",
      "fontSize": 32,
      "color": "#111111"
    }
  ]
}

## QML preview without commercial Qt

### Install

Create a venv and install dependencies using uv:

- uv venv --allow-existing .venv
- . .venv/bin/activate
- uv sync

### Run QML

Option A: Use the helper script:

- python tools/run_qml.py qml/sample.qml

Option B: Use the official `pyside6-qml` tool:

- pyside6-qml qml/sample.qml

## Generate a design spec from requirements

Use the prompt in `prompts/figma_spec_prompt.txt` with your preferred LLM to output a JSON spec compatible with the plugin.

### Free/local option: Ollama

1) Install Ollama and pull a small model (example):
   - `ollama pull qwen3:8b` (or `qwen2.5:3b` if you prefer a smaller model)
2) Generate a spec from requirements:
   - `python tools/gen_spec_ollama.py --requirements "A 900x600 dashboard with a hero card and CTA" --out specs/out.json`

You can override the model with `--model` or `OLLAMA_MODEL`.

## Convert JSON spec to QML

- `python tools/spec_to_qml.py specs/out.json qml/out.qml`

## End-to-end helper (requirements -> QML)

- `python tools/pipeline.py --requirements "A 900x600 dashboard with a hero card and CTA" --spec-out specs/out.json --qml-out qml/out.qml`

## Interactive flow (requirements -> spec -> optional QML)

- `python tools/interactive_flow.py`
- `python tools/interactive_flow.py --requirements-file requirements/design_requirements.txt`

## Figma MCP (Python, read-only) -> QML

Figma MCP is read-only, so it is best used for exporting design context and translating it to QML. For actual node creation, keep using the plugin.

### Desktop MCP vs Remote MCP

- Desktop MCP (`http://127.0.0.1:3845/mcp`): selection-based context; requires Figma Desktop and a Dev/Full seat.
- Remote MCP (`https://mcp.figma.com/mcp`): link-based context; does not depend on the desktop app and is easier to automate in scripts/CI.

If your workflow doesn't rely on selection-based context, the remote MCP is usually easier to maintain and automate.

### Fetch MCP output

- `python tools/figma_mcp_fetch.py --url https://mcp.figma.com/mcp --tool get_metadata --args '{"link":"<FIGMA_LINK>"}' --out mcp/metadata.txt`

### Figma MCP -> QML (Ollama)

- `python tools/figma_to_qml.py --url https://mcp.figma.com/mcp --tool get_design_context --args '{"link":"<FIGMA_LINK>"}' --out qml/from_figma.qml`
