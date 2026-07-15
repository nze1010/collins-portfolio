from django.db import migrations


SKILL_ICONS = {
    'Artificial Intelligence': 'ai-practical',
    'Python Programming': 'python',
    'Django Web Development': 'software',
    'Electrical & Electronics Engineering': 'engineering',
    'Solar PV System Design & Installation': 'renewable',
    'AI Automation & Workflow Optimization': 'automation',
    'Prompt Engineering & AI Optimization': 'prompt',
    'Technical Writing': 'writing',
    'Research & Technical Analysis': 'research',
    'Graphic Design & Visual Branding': 'creative',
    'AI Video Creation & Editing': 'video',
    'Digital Content Creation': 'media',
    'Virtual Assistance': 'assistant',
    'CCTV & Security Systems': 'security',
    'Project Management': 'management',
    'Public Speaking & Technology Advocacy': 'microphone',
}

SERVICE_ICONS = {
    'Electrical Installation and Maintenance': 'engineering',
    'Solar PV System Design and Installation': 'renewable',
    'CCTV and Security System Installation': 'security',
    'Python and Django Web Development': 'software',
    'Artificial Intelligence Consulting': 'ai-practical',
    'Prompt Engineering and AI Workflows': 'prompt',
    'Technical Writing and Research': 'writing',
    'Graphic Design and Visual Branding': 'creative',
    'AI Video Creation and Editing': 'video',
    'Digital Content Creation': 'media',
    'Virtual Assistance and Digital Support': 'assistant',
}

TOOLKIT_ICONS = {
    'Python': 'python',
    'Django': 'software',
    'Git': 'branch',
    'GitHub': 'github',
    'Visual Studio Code': 'software',
    'ChatGPT': 'ai-practical',
}


def apply_icons(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    Service = apps.get_model('main', 'Service')
    ToolkitItem = apps.get_model('main', 'ToolkitItem')

    for name, icon_name in SKILL_ICONS.items():
        Skill.objects.filter(name=name).update(icon_name=icon_name)
    for title, icon_name in SERVICE_ICONS.items():
        Service.objects.filter(title=title).update(icon_name=icon_name)
    for name, icon_name in TOOLKIT_ICONS.items():
        ToolkitItem.objects.filter(name=name).update(icon_name=icon_name)


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0005_compact_hero_copy'),
    ]

    operations = [
        migrations.RunPython(apply_icons, migrations.RunPython.noop),
    ]
