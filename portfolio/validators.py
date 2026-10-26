from urllib.parse import urlsplit
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, validate_email

def validate_contact_url(value):
    if not value:
        return
    if any(c.isspace() or ord(c) < 32 for c in value):
        raise ValidationError("В ссылке не должно быть пробелов или управляющих символов.")
    try:
        parsed = urlsplit(value)
    except ValueError as exc:
        raise ValidationError("Некорректный адрес ссылки.") from exc
    if parsed.scheme in {"https", "http"}:
        URLValidator(schemes=["https", "http"])(value)
    elif parsed.scheme == "mailto" and not parsed.query and not parsed.fragment:
        validate_email(parsed.path)
    elif parsed.scheme == "tel" and parsed.path and all(c in "+0123456789-()" for c in parsed.path):
        return
    else:
        raise ValidationError("Используйте https://, http://, mailto: или tel:.")

def validate_upload_size(value):
    if value.size > 5 * 1024 * 1024:
        raise ValidationError("Максимальный размер файла — 5 МБ.")

