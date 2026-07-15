from datetime import date

from django.db import migrations


CERTIFICATIONS = [
    {
        'title': 'ALX Virtual Assistant Programme',
        'defaults': {
            'issuer': 'ALX',
            'description': (
                'Certificate of achievement for completing the 8-week Virtual '
                'Assistance Skills in the Digital Age programme.'
            ),
            'date_earned': date(2024, 10, 7),
            'credential_id': 'sC7YR6nzN9',
            'credential_url': 'https://intranet.alxswe.com/certificates/sC7YR6nzN9',
            'image': 'certifications/alx-virtual-assistant-certificate.jpg',
            'is_featured': True,
            'is_active': True,
            'order': 10,
        },
    },
    {
        'title': 'ALX AI Career Essentials',
        'defaults': {
            'issuer': 'ALX',
            'description': (
                'Certificate of achievement for completing the 8-week AI-Augmented '
                'Professional Development Skills in the Digital Age programme.'
            ),
            'date_earned': date(2024, 7, 4),
            'credential_id': 'YcLmn7fNS2',
            'credential_url': 'https://intranet.alxswe.com/certificates/YcLmn7fNS2',
            'image': 'certifications/alx-ai-career-essentials-certificate.jpg',
            'is_featured': True,
            'is_active': True,
            'order': 20,
        },
    },
]


def add_certifications(apps, schema_editor):
    Certification = apps.get_model('main', 'Certification')
    for certification in CERTIFICATIONS:
        Certification.objects.update_or_create(
            title=certification['title'],
            defaults=certification['defaults'],
        )


def remove_certifications(apps, schema_editor):
    Certification = apps.get_model('main', 'Certification')
    Certification.objects.filter(
        title__in=[item['title'] for item in CERTIFICATIONS]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0008_experience_certification_credential_id_and_more'),
    ]

    operations = [
        migrations.RunPython(add_certifications, remove_certifications),
    ]
