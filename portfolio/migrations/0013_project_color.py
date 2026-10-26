from django.db import migrations, models


def preserve_palette(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    projects = Project.objects.using(schema_editor.connection.alias).order_by("position", "pk")
    for index, project in enumerate(projects):
        project.color = ("lavender", "blue", "gray")[index % 3]
        project.save(update_fields=["color"], using=schema_editor.connection.alias)


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0012_telegram_mini_app_title")]
    operations = [
        migrations.AddField("project", "color", models.CharField(
            choices=[("lavender", "Лавандовый"), ("blue", "Синий"), ("gray", "Серый")],
            default="lavender", max_length=10, verbose_name="Цвет карточки",
        )),
        migrations.RunPython(preserve_palette, migrations.RunPython.noop),
    ]
