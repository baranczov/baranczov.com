from hashlib import sha256
from functools import lru_cache
from pathlib import Path
import re

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join

register = template.Library()
BIO_EMPHASIS = re.compile(r"\*\*([^*\n]+)\*\*")


@register.filter
def biography(value):
    """Support **emphasis** only; escape all content, including inside emphasis."""
    parts = BIO_EMPHASIS.split(str(value or ""))
    return format_html_join("", "{}", (
        (format_html("<strong>{}</strong>", part) if index % 2 else part,)
        for index, part in enumerate(parts)
    ))

@lru_cache(maxsize=256)
def file_version(path, modified_ns, size):
    return sha256(Path(path).read_bytes()).hexdigest()[:12]

@register.simple_tag
def versioned_static(path):
    url = static(path)
    # Production already uses manifest hashes. Give local edits a new URL too.
    if settings.DEBUG and (source := finders.find(path)):
        info = Path(source).stat()
        version = file_version(source, info.st_mtime_ns, info.st_size)
        return f"{url}?v={version}"
    return url

@register.filter
def localized(obj, field_language):
    field, language = field_language.split(":", 1)
    return getattr(obj, f"{field}_{language}", "")

@register.filter
def lines(value):
    return [line.strip() for line in value.splitlines() if line.strip()]

