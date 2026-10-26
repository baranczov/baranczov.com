"""Offline lossless compression; never encode images while serving a page."""

from base64 import b64decode, b64encode
from io import BytesIO
from xml.etree import ElementTree as ET

from PIL import Image


def lossless_webp(data):
    with Image.open(BytesIO(data)) as source:
        if source.format != "PNG" or getattr(source, "is_animated", False):
            return None
        output = BytesIO()
        source.save(output, "WEBP", lossless=True, exact=True, method=6,
                    icc_profile=source.info.get("icc_profile", b""),
                    exif=source.info.get("exif", b""))
    compressed = output.getvalue()
    return compressed if len(compressed) < len(data) * .95 else None


def optimize_svg(data):
    """Keep SVG geometry and native image resolution; recompress embedded PNGs."""
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    root = ET.fromstring(data)
    changed = False
    for image in root.iter("{http://www.w3.org/2000/svg}image"):
        for attribute in ("href", "{http://www.w3.org/1999/xlink}href"):
            href = image.get(attribute, "")
            if not href.startswith("data:image/png;base64,"):
                continue
            optimized = lossless_webp(b64decode(href.split(",", 1)[1]))
            if optimized:
                image.set(attribute, "data:image/webp;base64," + b64encode(optimized).decode("ascii"))
                changed = True
    return ET.tostring(root, encoding="utf-8") if changed else None
