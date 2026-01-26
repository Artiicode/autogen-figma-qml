#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Tuple


def _load_prompt(prompt_path: Path, context_text: str) -> str:
    template = prompt_path.read_text(encoding="utf-8")
    return template.replace("{{FIGMA_CONTEXT}}", context_text)


def _extract_code_block(text: str) -> str:
    fence = "```"
    if fence not in text:
        return text.strip()
    start = text.find(fence)
    end = text.rfind(fence)
    if end <= start:
        return text.strip()
    block = text[start + len(fence) : end].strip()
    # Strip language tag if present
    if "\n" in block:
        first_line, rest = block.split("\n", 1)
        if first_line.lower().strip() in {"qml", "text"}:
            return rest.strip()
    return block.strip()


async def _open_session(url: str) -> Tuple[Any, Any, Any]:
    try:
        from mcp.client.streamable_http import streamablehttp_client
    except Exception:  # pragma: no cover
        from mcp.client.streamablehttp_client import streamablehttp_client

    return streamablehttp_client(url)


def _read_text_content(result: Any) -> str:
    chunks = []
    if getattr(result, "structuredContent", None) is not None:
        return json.dumps(result.structuredContent, indent=2)

    for item in getattr(result, "content", []) or []:
        text = getattr(item, "text", None)
        if text:
            chunks.append(text)
    return "\n".join(chunks)


def _ollama_generate(prompt: str, model: str) -> str:
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ollama run failed")
    return result.stdout.strip()


async def _run(url: str, tool: str, tool_args: dict, prompt_path: Path, model: str, out_path: Path) -> int:
    from mcp import ClientSession

    async with (await _open_session(url)) as (read, write, _get_session_id):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool, arguments=tool_args)
            context_text = _read_text_content(result)

    prompt = _load_prompt(prompt_path, context_text)
    raw = _ollama_generate(prompt, model)
    qml = _extract_code_block(raw)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(qml, encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Figma MCP -> QML via Ollama")
    parser.add_argument("--url", required=True, help="MCP server URL")
    parser.add_argument("--tool", default="get_design_context", help="Tool name")
    parser.add_argument("--args", default="{}", help="JSON arguments for tool")
    parser.add_argument("--prompt", default="prompts/figma_context_to_qml_prompt.txt")
    parser.add_argument("--model", default=os.environ.get("OLLAMA_MODEL", "qwen3:8b"))
    parser.add_argument("--out", default="qml/from_figma.qml")
    args = parser.parse_args()

    try:
        tool_args = json.loads(args.args)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid --args JSON: {exc}")

    import asyncio

    return asyncio.run(
        _run(args.url, args.tool, tool_args, Path(args.prompt), args.model, Path(args.out))
    )


if __name__ == "__main__":
    raise SystemExit(main())
