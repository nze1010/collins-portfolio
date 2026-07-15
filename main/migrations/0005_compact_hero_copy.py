from django.db import migrations, models


COMPACT_COPY = {
    'hero_headline': 'Electrical Engineer, AI Professional & Python/Django Developer',
    'hero_intro': (
        'I build practical solutions through engineering, AI, software, '
        'renewable energy, research, and digital creativity.'
    ),
    'supporting_text': (
        'Through CollinsTechEmpire, I turn technology into useful products, '
        'systems, and technical content.'
    ),
}


ORIGINAL_COPY = {
    'hero_headline': (
        'Electrical Engineer, AI Professional, Python & Django Developer, '
        'and Renewable Energy Specialist'
    ),
    'hero_intro': (
        'I combine engineering, artificial intelligence, software development, '
        'renewable energy, research, and digital creativity to build practical '
        'solutions for businesses, communities, and society.'
    ),
    'supporting_text': (
        'Through CollinsTechEmpire, I develop intelligent digital products, '
        'engineering systems, renewable-energy solutions, technical content, '
        'and innovative technology-driven projects.'
    ),
}


def update_copy(apps, schema_editor):
    SiteSettings = apps.get_model('main', 'SiteSettings')
    SiteSettings.objects.update_or_create(pk=1, defaults=COMPACT_COPY)


def restore_copy(apps, schema_editor):
    SiteSettings = apps.get_model('main', 'SiteSettings')
    SiteSettings.objects.update_or_create(pk=1, defaults=ORIGINAL_COPY)


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0004_seed_portfolio_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='hero_headline',
            field=models.CharField(
                default='Electrical Engineer, AI Professional & Python/Django Developer',
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='hero_intro',
            field=models.TextField(default=COMPACT_COPY['hero_intro']),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='supporting_text',
            field=models.TextField(default=COMPACT_COPY['supporting_text']),
        ),
        migrations.RunPython(update_copy, restore_copy),
    ]
