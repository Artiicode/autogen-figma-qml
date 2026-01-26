figma.showUI(__html__, { width: 520, height: 420 });

function hexToRgb(hex) {
  if (!hex) return { r: 1, g: 1, b: 1 };
  const normalized = hex.replace("#", "");
  if (normalized.length !== 6) return { r: 1, g: 1, b: 1 };
  const intVal = parseInt(normalized, 16);
  return {
    r: ((intVal >> 16) & 255) / 255,
    g: ((intVal >> 8) & 255) / 255,
    b: (intVal & 255) / 255,
  };
}

function applySolidFill(node, hex) {
  const rgb = hexToRgb(hex);
  node.fills = [{ type: "SOLID", color: rgb }];
}

async function buildFromSpec(spec) {
  const frame = figma.createFrame();
  frame.name = spec.name || "Frame";
  frame.resize(spec.width || 800, spec.height || 600);
  frame.layoutMode = "NONE";
  frame.clipsContent = true;
  applySolidFill(frame, "#FFFFFF");

  const center = figma.viewport.center;
  frame.x = center.x - frame.width / 2;
  frame.y = center.y - frame.height / 2;

  const children = Array.isArray(spec.children) ? spec.children : [];
  for (const child of children) {
    if (child.type === "rect") {
      const rect = figma.createRectangle();
      rect.name = child.name || "Rectangle";
      rect.x = child.x || 0;
      rect.y = child.y || 0;
      rect.resize(child.width || 100, child.height || 100);
      if (typeof child.radius === "number") {
        rect.cornerRadius = child.radius;
      }
      if (child.fill) {
        applySolidFill(rect, child.fill);
      }
      frame.appendChild(rect);
    }

    if (child.type === "text") {
      const text = figma.createText();
      text.name = child.name || "Text";
      text.x = child.x || 0;
      text.y = child.y || 0;
      const fontSize = child.fontSize || 16;
      await figma.loadFontAsync({ family: "Inter", style: "Regular" });
      text.fontName = { family: "Inter", style: "Regular" };
      text.fontSize = fontSize;
      text.characters = child.text || "";
      if (child.color) {
        applySolidFill(text, child.color);
      }
      frame.appendChild(text);
    }
  }

  figma.currentPage.appendChild(frame);
  figma.viewport.scrollAndZoomIntoView([frame]);
}

figma.ui.onmessage = async (msg) => {
  if (msg.type !== "build") return;
  try {
    const spec = JSON.parse(msg.payload || "{}");
    await buildFromSpec(spec);
    figma.ui.postMessage({ type: "status", payload: "Done" });
  } catch (err) {
    figma.ui.postMessage({ type: "status", payload: String(err) });
  }
};
