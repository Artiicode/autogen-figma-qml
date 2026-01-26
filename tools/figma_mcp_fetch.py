#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any, Tuple


async def _open_session(url: str) -> Tuple[Any, Any, Any]:
    try:
        from mcp.client.streamable_http import streamablehttp_client
    except Exception:  # pragma: no cover - fallback for SDK name variations
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


def _parse_json_arg(value: str) -> dict:
    if not value:
        return {}
    return json.loads(value)


async def _run(url: str, tool: str, args: dict, out_path: Path) -> int:
    from mcp import ClientSession

    async with (await _open_session(url)) as (read, write, _get_session_id):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool, arguments=args)
            text = _read_text_content(result)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(text, encoding="utf-8")
            print(f"Wrote {out_path}")
            return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Figma MCP tool output to a file")
    parser.add_argument("--url", required=True, help="MCP server URL")
    parser.add_argument("--tool", default="get_metadata", help="Tool name")
    parser.add_argument("--args", default="{}", help="JSON arguments for tool")
    parser.add_argument("--out", default="mcp/out.txt", help="Output file path")
    args = parser.parse_args()

    try:
        tool_args = _parse_json_arg(args.args)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid --args JSON: {exc}")

    import asyncio

    return asyncio.run(_run(args.url, args.tool, tool_args, Path(args.out)))


if __name__ == "__main__":
    raise SystemExit(main())
