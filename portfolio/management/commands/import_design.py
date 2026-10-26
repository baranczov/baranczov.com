from hashlib import sha256
from io import BytesIO
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Experience, Profile
from portfolio.image_optimization import lossless_webp

class Command(BaseCommand):
    help = "Импортировать portrait (или Photo) и tbank из user_design (JPG, PNG, WebP)."

    def add_arguments(self, parser):
        parser.add_argument("--directory", type=Path, default=settings.BASE_DIR / "user_design")

    def handle(self, *args, **options):
        directory = options["directory"]
        if not directory.is_dir():
            raise CommandError(f"Нет папки: {directory}")
        imported = 0
        for stem in ("portrait", "tbank"):
            names = {"portrait", "Photo"} if stem == "portrait" else {stem}
            candidates = sorted(p for p in directory.iterdir() if p.stem in names and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"})
            if not candidates:
                continue
            if len(candidates) > 1:
                raise CommandError(f"Оставьте один файл {stem}: найдено {len(candidates)}.")
            source = candidates[0]
            if source.stat().st_size > 5 * 1024 * 1024:
                raise CommandError(f"{source.name}: максимальный размер — 5 МБ.")
            data = source.read_bytes()
            try:
                with Image.open(BytesIO(data)) as im:
                    if im.format not in {"JPEG", "PNG", "WEBP"}:
                        raise CommandError(f"{source.name}: неподдерживаемый формат.")
                    im.verify()
            except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
                raise CommandError(f"Не удалось прочитать {source.name}: {exc}") from exc
            if stem == "portrait":
                obj, _ = Profile.objects.get_or_create(pk=1)
                field = obj.portrait
            else:
                obj = Experience.objects.filter(company="Т-Банк").first()
                if obj is None:
                    raise CommandError("Сначала выполните seed_portfolio, чтобы создать запись Т-Банка.")
                field = obj.image
            if field:
                with field.open("rb") as existing:
                    existing_digest = sha256(existing.read()).digest()
                    optimized = lossless_webp(data) if Path(field.name).suffix.lower() == ".webp" else None
                    if existing_digest == sha256(optimized or data).digest():
                        self.stdout.write(f"Без изменений: {source.name}")
                        continue
            field.save(source.name, ContentFile(data), save=True)
            imported += 1
            self.stdout.write(self.style.SUCCESS(f"Подключён: {source.name}"))
        self.stdout.write(f"Импортировано файлов: {imported}. Исходники сохранены.")

