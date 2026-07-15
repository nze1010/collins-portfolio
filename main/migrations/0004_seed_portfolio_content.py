from django.db import migrations


SKILLS = [
    ('Artificial Intelligence', 'Applying AI technologies to research, content development, productivity, automation, decision support, problem solving, and intelligent digital workflows.', 'ai', 'ai'),
    ('Python Programming', 'Developing Python-based applications, automation tools, backend logic, data-processing workflows, and practical software solutions.', 'software', 'python'),
    ('Django Web Development', 'Building dynamic web applications with Django models, views, templates, forms, authentication, admin dashboards, databases, CRUD operations, and deployment workflows.', 'software', 'code'),
    ('Electrical & Electronics Engineering', 'Designing, installing, testing, maintaining, and troubleshooting electrical and electronic systems for residential, commercial, and technical applications.', 'engineering', 'circuit'),
    ('Solar PV System Design & Installation', 'Designing and installing off-grid and hybrid solar systems, including energy assessment, inverter sizing, battery selection, panel configuration, installation, and maintenance.', 'energy', 'solar'),
    ('AI Automation & Workflow Optimization', 'Using artificial intelligence to streamline repetitive tasks, improve productivity, generate structured outputs, support research, and optimize business processes.', 'ai', 'network'),
    ('Prompt Engineering & AI Optimization', 'Designing effective prompts and AI workflows for research, software development, content creation, automation, image generation, video generation, and analytical tasks.', 'ai', 'ai'),
    ('Technical Writing', 'Producing clear technical documentation, engineering reports, project guides, research materials, educational content, proposals, and software documentation.', 'research', 'document'),
    ('Research & Technical Analysis', 'Conducting multidisciplinary research across engineering, artificial intelligence, science, technology, history, archaeology, culture, and African indigenous knowledge systems.', 'research', 'search'),
    ('Graphic Design & Visual Branding', 'Creating professional logos, campaign materials, social-media graphics, corporate identities, promotional content, presentations, billboards, and print-ready designs.', 'creative', 'design'),
    ('AI Video Creation & Editing', 'Creating and editing videos with artificial intelligence and modern digital tools for education, promotion, branding, storytelling, documentaries, and social-media communication.', 'creative', 'video'),
    ('Digital Content Creation', 'Developing informative written, visual, audio, and video content focused on technology, engineering, science, artificial intelligence, society, history, and culture.', 'creative', 'media'),
    ('Virtual Assistance', 'Providing digital administrative support, research, scheduling, documentation, communication management, task organization, and workflow coordination.', 'operations', 'check'),
    ('CCTV & Security Systems', 'Installing, configuring, maintaining, and troubleshooting surveillance cameras, DVR and NVR systems, monitoring equipment, and integrated security solutions.', 'engineering', 'camera'),
    ('Project Management', 'Planning, documenting, coordinating, and executing engineering, software, research, and digital projects from concept to completion.', 'operations', 'project'),
    ('Public Speaking & Technology Advocacy', 'Communicating technical ideas through presentations, seminars, online discussions, educational content, podcasts, and public-awareness campaigns.', 'research', 'message'),
]


SERVICES = [
    ('Electrical Installation and Maintenance', 'Practical electrical installation, diagnostics, maintenance, and system support delivered with safety and reliability in focus.', 'circuit'),
    ('Solar PV System Design and Installation', 'Energy assessment, system sizing, component selection, installation, testing, and support for off-grid and hybrid solar solutions.', 'solar'),
    ('CCTV and Security System Installation', 'Planning, installation, configuration, and troubleshooting for camera, DVR, NVR, and monitoring systems.', 'camera'),
    ('Python and Django Web Development', 'Database-driven web applications, backend workflows, admin dashboards, forms, CRUD systems, and deployment support.', 'code'),
    ('Artificial Intelligence Consulting', 'Practical guidance for applying AI to research, productivity, decision support, communication, and digital workflows.', 'ai'),
    ('Prompt Engineering and AI Workflows', 'Structured prompt systems and repeatable AI-assisted workflows designed around clear professional outcomes.', 'network'),
    ('Technical Writing and Research', 'Engineering documentation, reports, proposals, educational resources, research synthesis, and software documentation.', 'document'),
    ('Graphic Design and Visual Branding', 'Professional visual identities, campaign assets, presentations, promotional graphics, and digital brand materials.', 'design'),
    ('AI Video Creation and Editing', 'AI-assisted video development and editing for education, promotion, storytelling, and digital communication.', 'video'),
    ('Digital Content Creation', 'Purposeful written, visual, audio, and video content for technology, engineering, science, society, and culture.', 'media'),
    ('Virtual Assistance and Digital Support', 'Research, documentation, communication management, organization, scheduling, and workflow coordination.', 'check'),
]


def seed_portfolio_content(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    Service = apps.get_model('main', 'Service')
    ToolkitItem = apps.get_model('main', 'ToolkitItem')
    Project = apps.get_model('main', 'Project')
    SocialLink = apps.get_model('main', 'SocialLink')
    SiteSettings = apps.get_model('main', 'SiteSettings')
    UserProfile = apps.get_model('main', 'UserProfile')

    for order, (name, description, category, icon_name) in enumerate(SKILLS, start=1):
        Skill.objects.get_or_create(
            name=name,
            defaults={
                'description': description,
                'category': category,
                'icon_name': icon_name,
                'is_featured': order <= 6,
                'order': order,
                'proficiency': None,
            },
        )

    for order, (title, description, icon_name) in enumerate(SERVICES, start=1):
        Service.objects.get_or_create(
            title=title,
            defaults={
                'description': description,
                'icon_name': icon_name,
                'order': order,
            },
        )

    toolkit = [
        ('Python', 'Software Development', 'python'),
        ('Django', 'Software Development', 'code'),
        ('Git', 'Development Workflow', 'branch'),
        ('GitHub', 'Development Workflow', 'github'),
        ('Visual Studio Code', 'Development Workflow', 'code'),
        ('ChatGPT', 'Artificial Intelligence', 'ai'),
    ]
    for order, (name, category, icon_name) in enumerate(toolkit, start=1):
        ToolkitItem.objects.get_or_create(
            name=name,
            defaults={'category': category, 'icon_name': icon_name, 'order': order},
        )

    Project.objects.get_or_create(
        slug='collinstechempire-portfolio',
        defaults={
            'title': 'CollinsTechEmpire Portfolio',
            'category': 'Django Web Applications',
            'short_description': 'A dynamic professional portfolio and publishing platform built with Django, an admin-managed content system, responsive themes, and production deployment on PythonAnywhere.',
            'details': 'This evolving platform brings together engineering, artificial intelligence, software development, renewable energy, research, and digital creativity. It includes admin-managed skills and profile content, a full blog workflow, project presentation, contact-message storage, responsive design, and accessible light and dark themes.',
            'technologies': 'Python, Django, SQLite, HTML, CSS, JavaScript, Git, GitHub, PythonAnywhere',
            'live_url': 'https://collins1010.pythonanywhere.com/',
            'github_url': 'https://github.com/nze1010/collins-portfolio',
            'is_featured': True,
            'order': 1,
        },
    )

    SocialLink.objects.get_or_create(
        platform='GitHub',
        defaults={
            'url': 'https://github.com/nze1010',
            'icon_name': 'github',
            'order': 1,
        },
    )
    SiteSettings.objects.get_or_create(pk=1)

    profile = UserProfile.objects.first()
    if profile:
        profile.full_name = 'Engr. Josiah Collins Chinaza'
        profile.professional_title = 'Electrical Engineer | AI Professional | Python & Django Developer | Renewable Energy Specialist'
        profile.bio = 'I am an Electrical and Electronics Engineer and multidisciplinary technology professional building practical solutions through artificial intelligence, Python and Django development, renewable energy, research, technical communication, and digital creativity.'
        profile.long_bio = 'I combine electrical engineering experience with artificial intelligence, software development, renewable energy, research, and digital media. Through CollinsTechEmpire, I work on intelligent applications, solar power systems, security technologies, engineering services, educational content, technical documentation, and digital solutions designed to create measurable value.\n\nI am committed to continuous learning and to developing technology that responds to real challenges in Africa and beyond. My interests extend into science, history, archaeology, Igbo culture and Omenana, critical thinking, public communication, and the responsible use of technology in society.'
        profile.save()


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0003_certification_project_service_sitesettings_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_portfolio_content, migrations.RunPython.noop),
    ]
