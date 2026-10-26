from django.db import migrations


CONTACT_LINKS = [('GitHub', 'https://github.com/baranczov'),
 ('Kaggle', 'https://www.kaggle.com/danilbarantsov'),
 ('Gmail', 'mailto:dbaranczov@gmail.com'),
 ('Telegram', 'https://t.me/baranczov'),
 ('Instagram', 'https://www.instagram.com/baranczov/'),
 ('Phone Number (CV)', ''),
 ('LinkedIn', '')]


def populate_contact_links(apps, schema_editor):
    Contact = apps.get_model("portfolio", "Contact")
    records = Contact.objects.using(schema_editor.connection.alias)
    for position, (label, url) in enumerate(CONTACT_LINKS):
        contact, created = records.get_or_create(label=label, defaults={"url": url, "position": position})
        if not created:
            contact.position = position
            if not contact.url:
                contact.url = url
            contact.save(using=schema_editor.connection.alias, update_fields=["url", "position"])


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0004_capitalize_mathematics")]

    operations = [
        migrations.RunPython(populate_contact_links, migrations.RunPython.noop),
    ]
