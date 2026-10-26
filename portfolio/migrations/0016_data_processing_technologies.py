from django.db import migrations


def add_technologies(apps, schema_editor):
    Technology = apps.get_model("portfolio", "Technology")
    additions = (
        ("MLOps", "Apache Airflow", ("Spark/PySpark", "Hive", "HDFS")),
        ("Backend", "PostgreSQL", ("ClickHouse", "Kafka")),
    )
    records = Technology.objects.using(schema_editor.connection.alias)
    for title, anchor, technologies in additions:
        for record in records.filter(title_ru=title):
            changes = {}
            for field in ("items_ru", "items_en"):
                value = getattr(record, field)
                items = [item.strip() for item in value.rstrip().rstrip(".").split(",") if item.strip()]
                existing = {item.casefold() for item in items}
                missing = [item for item in technologies if item.casefold() not in existing]
                if missing:
                    position = items.index(anchor) + 1 if anchor in items else len(items)
                    items[position:position] = missing
                    changes[field] = ", ".join(items) + "."
            if changes:
                records.filter(pk=record.pk).update(**changes)


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0015_update_experience_duration")]
    operations = [migrations.RunPython(add_technologies, migrations.RunPython.noop)]
