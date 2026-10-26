from django.db import migrations


def capitalize_mathematics(apps, schema_editor):
    Technology = apps.get_model("portfolio", "Technology")
    records = Technology.objects.using(schema_editor.connection.alias).filter(
        title_ru="Математика", items_ru__startswith="линейная алгебра"
    )
    for technology in records:
        technology.items_ru = "Л" + technology.items_ru[1:]
        technology.save(using=schema_editor.connection.alias, update_fields=["items_ru"])


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0003_technology_content")]

    operations = [
        migrations.RunPython(capitalize_mathematics, migrations.RunPython.noop),
    ]
