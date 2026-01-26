# Figma MCP notes

- The official Figma MCP server currently exposes read-only tools (design context, metadata, variables). It does not provide tools to create or edit nodes.
- The remote server uses Figma URLs; the desktop server can provide selection-based context but requires a Dev/Full seat.

## Suggested usage

1) Use MCP to read design context from an existing Figma file.
2) Convert the context into QML (a future agent can map the JSON/structured output to QML).
3) For creation, use the Figma Plugin API (this repo includes a simple plugin to build a frame from JSON).
