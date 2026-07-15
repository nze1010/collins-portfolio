from datetime import date

from django.db import migrations


ORGANIZATIONS = [
    ('BLord Group', 'employer', 'A business group operating across real estate, technology, and other commercial sectors. Collins contributes branded marketing and visual communication materials.', 10),
    ('CollinsTechEmpire', 'enterprise', 'An engineering and technology enterprise founded in 2021, providing electrical installations, solar power systems, CCTV solutions, technical maintenance, artificial-intelligence training, and digital services.', 20),
    ('CollinsTechEmpire Digital Store', 'platform', 'A digital-products platform for e-books, professional guides, learning materials, software resources, and other downloadable solutions.', 30),
    ('Collins Reality TALK SHOW', 'platform', 'A media and public-discussion platform focused on technology, governance, culture, religion, history, critical thinking, and social development.', 40),
    ('Collins Reality Space', 'platform', 'A digital publishing platform for articles, research-based content, commentary, and discussions covering local and international issues.', 50),
    ('Freelance and Independent Professional Practice', 'practice', 'An independent professional practice covering graphic design, copywriting, article and research writing, video creation, virtual assistance, and technology-related services.', 60),
]


ROLES = [
    {
        'role': 'Creative Graphic Designer and Visual Content Specialist',
        'organization': 'BLord Group',
        'company_name': 'BLord Group',
        'period_label': 'Present',
        'summary': 'I create professional graphic designs, promotional materials, social-media visuals, and branded content for BLord Group and its associated businesses. I translate business ideas, property information, and campaign messages into clear, attractive, and consistent visual communication.',
    },
    {
        'role': 'Founder and Lead Engineer',
        'organization': 'CollinsTechEmpire',
        'company_name': 'CollinsTechEmpire',
        'employment_type': 'self_employed',
        'start_date': date(2021, 1, 1),
        'summary': 'I founded CollinsTechEmpire to provide practical engineering, renewable-energy, and technology solutions. I oversee electrical installations, solar systems, CCTV installations, maintenance, technical consultation, digital projects, and brand development.',
        'is_featured': True,
    },
    {
        'role': 'Electrical and Electronics Engineer',
        'organization': 'CollinsTechEmpire',
        'company_name': 'CollinsTechEmpire',
        'employment_type': 'self_employed',
        'period_label': 'Present',
        'summary': 'I design, install, inspect, troubleshoot, and maintain electrical and electronic systems for residential and commercial clients, including wiring, fault diagnosis, equipment maintenance, and system testing.',
    },
    {
        'role': 'Solar Power Systems Specialist',
        'organization': 'CollinsTechEmpire',
        'company_name': 'CollinsTechEmpire',
        'employment_type': 'self_employed',
        'period_label': 'Present',
        'summary': 'I design and install solar photovoltaic systems, inverter systems, battery storage, and supporting electrical components. I assess energy requirements, recommend suitable capacities, and provide maintenance and troubleshooting.',
    },
    {
        'role': 'CCTV and Security Systems Specialist',
        'organization': 'CollinsTechEmpire',
        'company_name': 'CollinsTechEmpire',
        'employment_type': 'self_employed',
        'period_label': 'Present',
        'summary': 'I install and maintain CCTV surveillance systems for homes, businesses, and organisations, covering camera positioning, cabling, configuration, monitoring setup, fault diagnosis, and alternative-power integration.',
    },
    {
        'role': 'Artificial Intelligence-Augmented Professional',
        'organization': 'Freelance and Independent Professional Practice',
        'company_name': 'Independent Professional Practice',
        'employment_type': 'self_employed',
        'period_label': 'Present',
        'summary': 'I apply artificial-intelligence tools to research, writing, content development, visual communication, productivity, business operations, and problem-solving, using AI responsibly to improve work quality and reduce repetitive tasks.',
    },
    {
        'role': 'Artificial Intelligence Trainer',
        'organization': 'CollinsTechEmpire',
        'company_name': 'CollinsTechEmpire',
        'employment_type': 'self_employed',
        'period_label': 'Present',
        'summary': 'I provide beginner-friendly training in generative AI, ChatGPT, prompt development, AI-assisted research, responsible AI use, productivity, and content creation for individuals and organisations.',
    },
    {
        'role': 'Graphic Designer and Brand Identity Designer',
        'organization': 'Freelance and Independent Professional Practice',
        'company_name': 'Freelance and Independent Practice',
        'employment_type': 'freelance',
        'period_label': 'Present',
        'summary': 'I create logos, flyers, social-media graphics, real-estate advertisements, political campaign materials, event designs, government billboards, and corporate branding assets for digital and print communication.',
    },
    {
        'role': 'Trained Copywriter and Article Writer',
        'organization': 'Freelance and Independent Professional Practice',
        'company_name': 'Freelance and Independent Practice',
        'employment_type': 'freelance',
        'period_label': 'Present',
        'summary': 'I write persuasive, informative, and audience-focused advertising copy, website content, promotional messages, educational articles, opinion pieces, and social-media publications.',
    },
    {
        'role': 'Digital Article Publisher and Social-Media Writer',
        'organization': 'Collins Reality Space',
        'company_name': 'Independent Publishing',
        'employment_type': 'self_employed',
        'period_label': 'Present',
        'summary': 'I publish original articles on technology, science, artificial intelligence, governance, social development, religion, history, African affairs, culture, and other issues of public interest.',
    },
    {
        'role': 'Research Writer',
        'organization': 'Freelance and Independent Professional Practice',
        'company_name': 'Freelance and Independent Research',
        'employment_type': 'freelance',
        'period_label': 'Present',
        'summary': 'I conduct research and produce structured articles, reports, educational materials, and analytical publications by comparing relevant sources and presenting complex topics clearly.',
    },
    {
        'role': 'Igbo Omenana, Culture and Traditions Writer',
        'organization': 'Freelance and Independent Professional Practice',
        'company_name': 'Independent Cultural Research and Publishing',
        'employment_type': 'self_employed',
        'period_label': 'Present',
        'summary': 'I research, document, and publish content on Igbo Omenana, indigenous knowledge, cultural values, traditional institutions, spirituality, customs, history, and community practices.',
    },
    {
        'role': 'Founder, Writer and Media Content Creator',
        'organization': 'Collins Reality TALK SHOW',
        'company_name': 'Collins Reality TALK SHOW and Collins Reality Space',
        'employment_type': 'self_employed',
        'period_label': 'Present',
        'summary': 'I create articles, videos, commentaries, and analytical content on technology, governance, culture, religion, history, and social development to support critical thinking and informed public discussion.',
    },
    {
        'role': 'Video Creator and Digital Storyteller',
        'organization': 'Freelance and Independent Professional Practice',
        'company_name': 'Freelance and Independent Practice',
        'employment_type': 'freelance',
        'period_label': 'Present',
        'summary': 'I create promotional videos, educational content, campaign videos, and social-media visuals by combining writing, graphics, editing, and storytelling.',
    },
    {
        'role': 'Virtual Assistant',
        'organization': 'Freelance and Independent Professional Practice',
        'company_name': 'Independent Professional Practice',
        'employment_type': 'freelance',
        'period_label': 'Present',
        'summary': 'I provide remote administrative support including email organisation, calendar management, online research, document preparation, data organisation, scheduling, and professional communication.',
    },
    {
        'role': 'Python and Django Developer',
        'organization': 'Freelance and Independent Professional Practice',
        'company_name': 'Independent Learning and Portfolio Development',
        'employment_type': 'self_employed',
        'period_label': 'Present',
        'summary': 'I build database-driven web applications with Python and Django, including administrative dashboards, forms, authentication, CRUD operations, and backend application workflows.',
    },
    {
        'role': 'Digital Product Creator',
        'organization': 'CollinsTechEmpire Digital Store',
        'company_name': 'CollinsTechEmpire Digital Store',
        'employment_type': 'self_employed',
        'start_date': date(2024, 1, 1),
        'summary': 'I develop and organise e-books, educational materials, software resources, professional guides, and training content designed to support learning, productivity, professional growth, and business development.',
    },
]


CREDENTIALS = [
    ('ALX AI Career Essentials', {'record_type': 'certificate', 'is_verified': True, 'is_active': True, 'is_featured': True, 'order': 10}),
    ('ALX Virtual Assistant Programme', {'record_type': 'certificate', 'is_verified': True, 'is_active': True, 'is_featured': True, 'order': 20}),
    ('Higher National Diploma in Electrical/Electronics Engineering', {
        'issuer': 'Abia State Polytechnic, Aba',
        'record_type': 'qualification',
        'description': 'Advanced technical education in electrical and electronics engineering, including electrical systems, electronics, installation, maintenance, troubleshooting, and engineering problem-solving.',
        'date_earned': date(2019, 1, 1),
        'is_verified': False,
        'is_active': True,
        'order': 30,
    }),
    ('National Diploma in Electrical/Electronics Engineering', {
        'issuer': 'Federal Polytechnic, Owerri',
        'record_type': 'qualification',
        'description': 'Foundational technical training in electrical circuits, electronics, installation practices, maintenance, and engineering principles.',
        'date_earned': date(2014, 1, 1),
        'is_verified': False,
        'is_active': True,
        'order': 40,
    }),
    ('Professional Copywriting Training', {
        'record_type': 'training',
        'description': 'Training in persuasive writing, audience-focused communication, promotional content, article writing, brand messaging, and digital publication.',
        'is_verified': False,
        'is_active': True,
        'order': 50,
    }),
    ('Nigerian Army Social Media Seminar', {
        'issuer': 'Nigerian Army - 33rd Edition',
        'record_type': 'seminar',
        'description': 'Professional discussions and training on responsible social-media use, information management, digital communication, public awareness, and national-security communication.',
        'is_verified': False,
        'is_active': True,
        'order': 60,
    }),
]


def seed_journey(apps, schema_editor):
    Organization = apps.get_model('main', 'Organization')
    Experience = apps.get_model('main', 'Experience')
    Certification = apps.get_model('main', 'Certification')

    organizations = {}
    for name, organization_type, description, order in ORGANIZATIONS:
        organization, _ = Organization.objects.update_or_create(
            name=name,
            defaults={
                'organization_type': organization_type,
                'description': description,
                'is_featured': name == 'CollinsTechEmpire',
                'is_active': True,
                'order': order,
            },
        )
        organizations[name] = organization

    for order, item in enumerate(ROLES, start=1):
        defaults = item.copy()
        role = defaults.pop('role')
        organization_name = defaults.pop('organization')
        company_name = defaults.pop('company_name')
        defaults['organization'] = organizations[organization_name]
        defaults.setdefault('employment_type', '')
        defaults.setdefault('start_date', None)
        defaults.setdefault('end_date', None)
        defaults.setdefault('period_label', '')
        defaults.setdefault('is_current', True)
        defaults.setdefault('is_featured', False)
        defaults['is_active'] = True
        defaults['order'] = order * 10
        Experience.objects.update_or_create(
            role=role,
            company_name=company_name,
            defaults=defaults,
        )

    for title, defaults in CREDENTIALS:
        Certification.objects.update_or_create(title=title, defaults=defaults)


def unseed_journey(apps, schema_editor):
    Organization = apps.get_model('main', 'Organization')
    Experience = apps.get_model('main', 'Experience')
    Certification = apps.get_model('main', 'Certification')

    Experience.objects.filter(role__in=[item['role'] for item in ROLES]).delete()
    Certification.objects.filter(title__in=[item[0] for item in CREDENTIALS[2:]]).delete()
    Certification.objects.filter(title__in=[item[0] for item in CREDENTIALS[:2]]).update(
        is_verified=False,
        record_type='certificate',
    )
    Organization.objects.filter(name__in=[item[0] for item in ORGANIZATIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0011_organization_certification_is_verified_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_journey, unseed_journey),
    ]
