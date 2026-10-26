from django.db import migrations
from django.db.models import F, Value
from django.db.models.functions import Replace


def replace_dashes(apps, schema_editor):
    fields_by_model = {
        "Experience": ("company", "role_ru", "role_en", "tasks_ru", "tasks_en", "period_ru", "period_en"),
        "ExperienceTask": ("title_ru", "title_en", "description_ru", "description_en"),
    }
    for model_name, fields in fields_by_model.items():
        model = apps.get_model("portfolio", model_name)
        model.objects.using(schema_editor.connection.alias).update(**{
            field: Replace(Replace(F(field), Value("—"), Value("-")), Value("–"), Value("-"))
            for field in fields
        })


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0007_work_history_content")]
    operations = [migrations.RunPython(replace_dashes, migrations.RunPython.noop)]
