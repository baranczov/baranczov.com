from django.db import migrations


def update_title(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Project.objects.using(schema_editor.connection.alias).filter(
        github_url="https://github.com/baranczov/party_bot",
    ).update(
        title_ru="Telegram Mini App для мероприятий",
        title_en="Telegram Mini App for events",
    )


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0011_experience_dates_and_past_tense")]
    operations = [migrations.RunPython(update_title, migrations.RunPython.noop)]
