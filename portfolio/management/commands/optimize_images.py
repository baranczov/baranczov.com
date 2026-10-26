from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from portfolio.image_optimization import lossless_webp, optimize_svg
from portfolio.models import Experience, Profile, Project


class Command(BaseCommand):
    help = "Losslessly compress PNG covers and embedded SVG PNGs offline. Originals in user_design and media are kept."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="Save optimized copies and update image references.")
        parser.add_argument("--static-directory", type=Path, default=settings.BASE_DIR / "static" / "images")

    def handle(self, *args, **options):
        saved, count = 0, 0
        for model, field_name in ((Profile, "portrait"), (Experience, "image"), (Project, "image")):
            for record in model.objects.all().iterator():
                field = getattr(record, field_name)
                if not field or Path(field.name).suffix.lower() != ".png":
                    continue
                try:
                    with field.open("rb") as source:
                        data = source.read()
                except FileNotFoundError:
                    self.stderr.write(f"Missing file (unchanged): {field.name}")
                    continue
                optimized = lossless_webp(data)
                if optimized is None:
                    continue
                self.stdout.write(f"{field.name}: {len(data)} -> {len(optimized)} bytes")
                saved += len(data) - len(optimized)
                count += 1
                if options["apply"]:
                    field.save(Path(field.name).with_suffix(".webp").name, ContentFile(optimized), save=True)
        for path in sorted(options["static_directory"].rglob("*.svg")):
            data = path.read_bytes()
            optimized = optimize_svg(data)
            if optimized is None:
                continue
            self.stdout.write(f"{path.name}: {len(data)} -> {len(optimized)} bytes")
            saved += len(data) - len(optimized)
            count += 1
            if options["apply"]:
                temporary = path.with_suffix(".svg.tmp")
                temporary.write_bytes(optimized)
                temporary.replace(path)
        self.stdout.write(f"{'Saved' if options['apply'] else 'Would save'} {saved} bytes across {count} images.")
