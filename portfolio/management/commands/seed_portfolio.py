from django.core.management.base import BaseCommand
from django.db import transaction
from portfolio.models import Contact, Experience, ExperienceTask, Profile, Project, Technology
from portfolio.content import CONTACTS, TECHNOLOGIES
from portfolio.experience_content import EXPERIENCES
from portfolio.project_content import PROJECTS

class Command(BaseCommand):
    help = "Добавить утверждённый контент портфолио, не изменяя существующие записи."

    @transaction.atomic
    def handle(self, *args, **options):
        Profile.objects.get_or_create(pk=1)
        for position, content in enumerate(EXPERIENCES):
            defaults = {key: value for key, value in content.items() if key not in ("company", "tasks")}
            experience, created = Experience.objects.get_or_create(
                company=content["company"], defaults={**defaults, "position": position},
            )
            if created:
                for task_position, task in enumerate(content["tasks"]):
                    ExperienceTask.objects.create(experience=experience, position=task_position, **task)
        for position, project in enumerate(PROJECTS):
            defaults = {key: value for key, value in project.items() if key != "github_url"}
            Project.objects.get_or_create(github_url=project["github_url"], defaults={**defaults, "position": position, "color": ("lavender", "blue", "gray")[position % 3]})
        for position, technology in enumerate(TECHNOLOGIES):
            defaults = {key: value for key, value in technology.items() if key != "title_ru"}
            Technology.objects.get_or_create(title_ru=technology["title_ru"], defaults={**defaults, "position": position})
        for position, contact in enumerate(CONTACTS):
            Contact.objects.get_or_create(label=contact["label"], defaults={"url": contact["url"], "position": position})
        self.stdout.write(self.style.SUCCESS("Базовый контент готов. Неизвестные тексты, изображения и ссылки оставлены пустыми."))

