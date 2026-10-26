"""Compose the supplied SVG icons into one seamless, static background tile."""

from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def main():
    step, height = 100, 65
    strip = ET.Element(f"{{{SVG}}}svg", {
        "width": str(13 * step), "height": str(height),
        "viewBox": f"0 0 {13 * step} {height}",
    })
    for number in range(1, 14):
        icon = ET.parse(ROOT / "user_design" / f"icon_{number}.svg").getroot()
        width, icon_height = float(icon.get("width")), float(icon.get("height"))
        icon.set("x", f"{(number - 1) * step + 75 - width / 2:g}")
        icon.set("y", f"{(height - icon_height) / 2:g}")
        strip.append(icon)
    target = ROOT / "static" / "images" / "technology-strip.svg"
    target.write_text(ET.tostring(strip, encoding="unicode") + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
