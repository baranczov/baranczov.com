import re
import json
from io import BytesIO, StringIO
from base64 import b64encode, b64decode
from xml.etree import ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.contrib.auth.models import Permission, User
from django.core.management import call_command
from django.test import TestCase, override_settings
from .models import Contact, Experience, ExperienceTask, Profile, Project, Technology
from .validators import validate_contact_url
from .project_content import PROJECTS

@override_settings(STORAGES={"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"}, "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}})
class PortfolioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_portfolio", stdout=StringIO())

    def test_languages_and_unknown_route(self):
        for lang, title in [("ru", "Рабочий опыт"), ("en", "Work experience")]:
            response = self.client.get(f"/{lang}/")
            self.assertContains(response, title)
            self.assertContains(response, f'<html lang="{lang}"')
            self.assertEqual(response.headers["Content-Language"], lang)
        self.assertEqual(self.client.get("/de/").status_code, 404)

    def test_language_preference_is_validated(self):
        self.client.get("/en/")
        self.assertRedirects(self.client.get("/"), "/en/")
        self.client.cookies["portfolio_language"] = "https://example.com"
        self.assertRedirects(self.client.get("/"), "/ru/")

    def test_local_stylesheet_url_changes_when_styles_change(self):
        def stylesheet_url(language):
            html = self.client.get(f"/{language}/").content.decode()
            return re.search(r'<link rel="stylesheet" href="([^"]+)"', html).group(1)

        with TemporaryDirectory() as directory, override_settings(DEBUG=True, STATICFILES_DIRS=[directory]):
            stylesheet = Path(directory) / "css" / "style.css"
            stylesheet.parent.mkdir()
            stylesheet.write_text(".card-back { background: gray }")
            original = stylesheet_url("ru")
            self.assertEqual(stylesheet_url("en"), original)
            self.assertEqual(stylesheet_url("ru"), original)
            stylesheet.write_text(".card-back { background: blue }")
            updated = stylesheet_url("en")
            self.assertNotEqual(updated, original)
            self.assertEqual(stylesheet_url("ru"), updated)

    def test_experience_has_three_companies_with_localized_tasks_and_dates(self):
        experiences = list(Experience.objects.all())
        self.assertEqual([item.company for item in experiences], ["Т-Банк", "IT_ONE", "ВкусВилл"])
        self.assertEqual(ExperienceTask.objects.count(), 9)
        for language in ("ru", "en"):
            response = self.client.get(f"/{language}/")
            self.assertEqual([card["record"] for card in response.context["experiences"]], experiences)
            self.assertNotContains(response, 'experience-card experience-placeholder')
            for cover in ("t-bank", "it-one", "vkusvill"):
                self.assertContains(response, f'src="/static/images/experience/{cover}.svg"', count=1)
            for experience in experiences:
                self.assertContains(response, getattr(experience, f"period_{language}"))
                self.assertEqual(experience.responsibilities.count(), 3)
                for task in experience.responsibilities.all():
                    self.assertContains(response, getattr(task, f"title_{language}"))
                    self.assertContains(response, getattr(task, f"description_{language}"))

    def test_imported_javascript_gets_a_new_url_after_an_update(self):
        def imports():
            html = self.client.get("/ru/").content.decode()
            return json.loads(re.search(r'<script type="importmap">(.*?)</script>', html, re.S).group(1))["imports"]
        with TemporaryDirectory() as directory, override_settings(DEBUG=True, STATICFILES_DIRS=[directory]):
            script = Path(directory) / "js" / "carousel.js"
            script.parent.mkdir()
            script.write_text("export const revision = 1;")
            before = imports()["/static/js/carousel.js"]
            script.write_text("export const revision = 2;")
            after = imports()["/static/js/carousel.js"]
            self.assertNotEqual(before, after)
            self.assertEqual(imports()["/static/js/carousel.js"], after)

    def test_hidden_companies_and_tasks_do_not_leak_into_the_page(self):
        Experience.objects.filter(company="ВкусВилл").update(published=False)
        task = ExperienceTask.objects.first()
        task.published = False
        task.save()
        response = self.client.get("/ru/")
        self.assertNotContains(response, 'src="/static/images/experience/vkusvill.svg"')
        self.assertNotContains(response, task.description_ru)
        self.assertNotContains(response, task.title_ru)
        self.assertContains(response, 'experience-card experience-placeholder', count=1)

    def test_task_content_is_escaped_in_text_and_attributes(self):
        task = ExperienceTask.objects.first()
        task.title_ru = '<script>alert("title")</script>'
        task.description_ru = '\" onmouseover=\"alert(1) <img src=x onerror=alert(1)>'
        task.save()
        response = self.client.get("/ru/")
        self.assertContains(response, '&lt;script&gt;alert(&quot;title&quot;)&lt;/script&gt;')
        self.assertContains(response, 'data-description="&quot; onmouseover=&quot;alert(1) &lt;img')
        self.assertNotContains(response, '<img src=x')

    def test_projects_include_the_entire_published_collection_in_order(self):
        Project.objects.all().delete()
        projects = [Project.objects.create(title_ru=f"Проект {i}", title_en=f"Project {i}", position=i) for i in range(8)]
        Project.objects.create(title_ru="Черновик", title_en="Draft", position=0, published=False)
        for language in ("ru", "en"):
            response = self.client.get(f"/{language}/")
            self.assertEqual(list(response.context["projects"]), projects)
            self.assertContains(response, 'class="orbit-card project-card"', count=8)
            self.assertNotContains(response, 'Черновик')
            self.assertNotContains(response, 'Draft')

    def test_approved_projects_include_localized_descriptions_and_exact_links(self):
        self.assertEqual(Project.objects.count(), 6)
        for language in ("ru", "en"):
            response = self.client.get(f"/{language}/")
            for project in PROJECTS:
                self.assertContains(response, project[f"title_{language}"])
                self.assertContains(response, project[f"description_{language}"])
                self.assertContains(response, f'href="{project["github_url"]}" target="_blank" rel="noopener noreferrer"', count=1)
                if project["kaggle_url"]:
                    self.assertContains(response, f'href="{project["kaggle_url"]}" target="_blank" rel="noopener noreferrer"', count=1)
            self.assertNotContains(response, 'class="placeholder-index"')

    def test_project_descriptions_are_escaped_and_links_are_optional(self):
        Project.objects.all().delete()
        Project.objects.create(title_ru="Пример", title_en="Example", description_ru='<img src=x onerror="alert(1)">')
        response = self.client.get("/ru/")
        self.assertContains(response, '&lt;img src=x onerror=&quot;alert(1)&quot;&gt;')
        self.assertNotContains(response, '<img src=x')
        section = response.content.decode().split('<section id="projects"', 1)[1].split('<section id="stack"', 1)[0]
        self.assertNotIn('href=', section)

    def test_seed_is_idempotent_and_preserves_edits(self):
        profile = Profile.objects.get()
        profile.bio_ru = "Авторский текст"
        profile.save()
        task = ExperienceTask.objects.first()
        task.description_ru = "Отредактированная задача"
        task.save()
        ExperienceTask.objects.last().delete()
        project = Project.objects.first()
        project.title_ru = "Обновлённое название"
        project.description_ru = "Обновлённое описание"
        project.published = False
        project.save()
        call_command("seed_portfolio", stdout=StringIO())
        self.assertEqual(Profile.objects.get().bio_ru, "Авторский текст")
        self.assertEqual(Experience.objects.count(), 3)
        self.assertEqual(ExperienceTask.objects.count(), 8)
        self.assertEqual(ExperienceTask.objects.get(pk=task.pk).description_ru, "Отредактированная задача")
        self.assertEqual(Technology.objects.count(), 6)
        self.assertEqual(Contact.objects.count(), 7)
        self.assertEqual(Project.objects.count(), 6)
        project.refresh_from_db()
        self.assertEqual(project.description_ru, "Обновлённое описание")
        self.assertEqual(project.title_ru, "Обновлённое название")
        self.assertFalse(project.published)

    def test_contacts_use_saved_links_and_hide_unpublished_records(self):
        response = self.client.get("/ru/")
        self.assertContains(response, 'href="https://github.com/baranczov"')
        self.assertContains(response, 'href="mailto:dbaranczov@gmail.com"')
        self.assertContains(response, 'role="link" aria-disabled="true"', count=2)
        Contact.objects.filter(label="GitHub").update(published=False)
        self.assertNotContains(self.client.get("/ru/"), 'href="https://github.com/baranczov"')
        profile = Profile.objects.get()
        profile.cv.name = "cv/resume.pdf"
        profile.save()
        self.assertContains(self.client.get("/ru/"), 'href="/media/cv/resume.pdf"')

    def test_contact_validation_rejects_script_and_accepts_real_schemes(self):
        for invalid in ["javascript:alert(1)", "data:text/html,x", "//evil.com", "tel:", "mailto:hello\n@example.com", "https://example.com/ bad"]:
            with self.subTest(invalid=invalid), self.assertRaises(ValidationError):
                validate_contact_url(invalid)
        for valid in ["https://github.com/example", "mailto:name@example.com", "tel:+1234567890"]:
            validate_contact_url(valid)

    def test_resume_link_matches_page_language(self):
        profile = Profile.objects.get()
        for russian, english in (("cv/resume-ru.pdf", ""),
                                 ("cv/resume-ru.pdf", "cv/resume-en.pdf"),
                                 ("", "cv/resume-en.pdf")):
            profile.cv.name = russian
            profile.cv_en.name = english
            profile.save(update_fields=["cv", "cv_en"])
            for language, filename in (("ru", russian), ("en", english)):
                with self.subTest(language=language, russian=russian, english=english):
                    response = self.client.get(f"/{language}/")
                    tile = next(item for item in response.context["contact_tiles"] if item["icon"] == "resume")
                    self.assertEqual(tile["url"], f"/media/{filename}" if filename else "")
                    self.assertEqual(tile["label"], "Резюме" if language == "ru" else "CV")
                    if filename:
                        self.assertContains(response, f'href="/media/{filename}"')
                        label = "Открыть резюме" if language == "ru" else "View CV"
                        self.assertContains(response, f'<a class="resume-download" href="/media/{filename}" target="_blank" rel="noopener noreferrer">{label}</a>', html=True)
                    else:
                        self.assertNotContains(response, 'class="resume-download"')

    def test_content_is_escaped_and_drafts_not_shown(self):
        profile = Profile.objects.get()
        profile.bio_ru = '<script>alert("x")</script>'
        profile.save()
        Project.objects.create(title_ru="Скрытый проект", title_en="Hidden project", published=False)
        response = self.client.get("/ru/")
        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, '<script>alert("x")</script>')
        self.assertNotContains(response, "Скрытый проект")

    def test_admin_requires_authentication(self):
        self.assertRedirects(self.client.get("/admin/"), "/admin/login/?next=/admin/")

    def test_biography_emphasis_escapes_html_and_preserves_line_breaks(self):
        profile = Profile.objects.get()
        profile.bio_ru = '**<img src=x onerror="alert(1)">**\nТекст & **акцент** и **незакрыто'
        profile.save()
        response = self.client.get("/ru/")
        self.assertContains(response, '<strong>&lt;img src=x onerror=&quot;alert(1)&quot;&gt;</strong><br>Текст &amp; <strong>акцент</strong> и **незакрыто', html=False)
        self.assertNotContains(response, '<img src=x')

    def test_about_copy_restores_biography_with_ml_introduction(self):
        for language in ("ru", "en"):
            html = self.client.get(f"/{language}/").content.decode()
            biography = re.search(r'<div class="bio">(.*?)</div>', html, re.S).group(1)
            self.assertNotIn('**', biography)
            self.assertIn('<p class="hero-role"><span>ML Engineer</span> <span>/ Data Scientist</span></p>', html)
            self.assertLess(biography.index('production'), biography.index('University' if language == 'en' else 'университете'))
            self.assertNotIn('RuBERT', biography)
            self.assertIn('Datathon' if language == 'en' else 'Дататона', biography)
        russian = self.client.get("/ru/")
        self.assertContains(russian, '<strong>более двух лет коммерческого опыта.</strong>')
        self.assertNotContains(russian, '2-ух')
        self.assertContains(russian, '<strong>аналитическим мышлением</strong>')
        self.assertContains(russian, '<strong>довожу задачи до результата</strong>')
        self.assertContains(self.client.get("/en/"), '<strong>over two years of commercial experience.</strong>')

    def test_profile_creation_requires_add_permission_even_when_profile_is_missing(self):
        Profile.objects.all().delete()
        viewer = User.objects.create_user("viewer", is_staff=True)
        viewer.user_permissions.add(Permission.objects.get(codename="view_profile"))
        self.client.force_login(viewer)
        self.assertEqual(self.client.post("/admin/portfolio/profile/add/", {}).status_code, 403)
        self.assertFalse(Profile.objects.exists())

    def test_project_color_survives_reordering(self):
        blue = Project.objects.get(github_url="https://github.com/baranczov/ML_Project_1")
        self.assertEqual(blue.color, "blue")
        Project.objects.filter(position=0).update(position=100)
        response = self.client.get("/ru/")
        self.assertEqual(response.context["projects"][0].pk, blue.pk)
        self.assertContains(response, 'data-color="blue" data-card data-index="0"')

    def test_public_page_query_count_does_not_grow_with_content(self):
        for index in range(20):
            Project.objects.create(title_ru=f"Дополнительный {index}", title_en=f"Extra {index}")
            ExperienceTask.objects.create(experience=Experience.objects.first(), title_ru="Задача", title_en="Task")
        with self.assertNumQueries(6):
            response = self.client.get("/ru/")
        self.assertEqual(response.status_code, 200)

    def test_image_optimization_preserves_pixels_content_originals_and_reimport(self):
        with TemporaryDirectory() as directory, override_settings(MEDIA_ROOT=directory):
            source_dir = Path(directory) / "source"
            source_dir.mkdir()
            static_dir = Path(directory) / "static"
            static_dir.mkdir()
            original = Image.new("RGBA", (160, 160), (30, 60, 120, 128))
            data = BytesIO()
            original.save(data, "PNG")
            png = data.getvalue()
            (source_dir / "portrait.png").write_bytes(png)
            svg = static_dir / "logo.svg"
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"><image width="160" height="160" href="data:image/png;base64,' + b64encode(png).decode() + '"/></svg>')
            project = Project.objects.first()
            project.image.save("cover.png", ContentFile(png), save=True)
            original_path = Path(project.image.path)
            title = project.title_ru
            call_command("import_design", directory=source_dir, stdout=StringIO())
            call_command("optimize_images", apply=True, static_directory=static_dir, stdout=StringIO())
            project.refresh_from_db()
            self.assertEqual(project.title_ru, title)
            self.assertEqual(original_path.read_bytes(), png)
            self.assertEqual(Image.open(project.image.path).convert("RGBA").tobytes(), original.tobytes())
            self.assertLess(Path(project.image.path).stat().st_size, len(png))
            icon = ET.parse(svg).getroot()[0]
            encoded = icon.attrib["href"].split(",", 1)[1]
            self.assertEqual(Image.open(BytesIO(b64decode(encoded))).convert("RGBA").tobytes(), original.tobytes())
            portrait_name = Profile.objects.get().portrait.name
            call_command("import_design", directory=source_dir, stdout=StringIO())
            self.assertEqual(Profile.objects.get().portrait.name, portrait_name)
            optimized_name = project.image.name
            call_command("optimize_images", apply=True, static_directory=static_dir, stdout=StringIO())
            project.refresh_from_db()
            self.assertEqual(project.image.name, optimized_name)

    def test_sitemap_health_and_robots(self):
        self.assertEqual(self.client.get("/health/").json(), {"status": "ok"})
        self.assertContains(self.client.get("/sitemap.xml"), "/ru/</loc>")
        self.assertContains(self.client.get("/robots.txt"), "Disallow: /admin/")

    def test_asset_import_is_repeatable_and_validates_files(self):
        with TemporaryDirectory() as directory, TemporaryDirectory() as media:
            output = BytesIO()
            Image.new("RGB", (50, 60), "blue").save(output, format="PNG")
            image = Path(directory) / "portrait.png"
            image.write_bytes(output.getvalue())
            with override_settings(MEDIA_ROOT=media):
                call_command("import_design", directory=Path(directory), stdout=StringIO())
                first = Profile.objects.get().portrait.name
                call_command("import_design", directory=Path(directory), stdout=StringIO())
                self.assertEqual(Profile.objects.get().portrait.name, first)
                self.assertEqual(len(list(Path(media).rglob("*.png"))), 1)

