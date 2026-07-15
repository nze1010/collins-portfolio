from django.db import migrations, models


def normalize_existing_icons(apps, schema_editor):
    SocialLink = apps.get_model('main', 'SocialLink')
    mappings = {
        'facebook': 'facebook',
        'instagram': 'instagram',
        'gmail': 'gmail',
        'email': 'gmail',
        'mail': 'gmail',
        'whatsapp': 'whatsapp',
        'github': 'github',
    }
    for social_link in SocialLink.objects.all():
        platform_key = social_link.platform.lower()
        for platform_name, icon_name in mappings.items():
            if platform_name in platform_key:
                social_link.icon_name = icon_name
                social_link.save(update_fields=['icon_name'])
                break


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0006_professional_icon_mapping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sociallink',
            name='icon_name',
            field=models.CharField(
                choices=[
                    ('external', 'Generic link'),
                    ('facebook', 'Facebook'),
                    ('instagram', 'Instagram'),
                    ('gmail', 'Gmail / Email'),
                    ('whatsapp', 'WhatsApp'),
                    ('github', 'GitHub'),
                ],
                default='external',
                max_length=30,
            ),
        ),
        migrations.RunPython(normalize_existing_icons, migrations.RunPython.noop),
    ]
