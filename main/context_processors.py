from .models import SiteSettings, SocialLink


def site_context(request):
    return {
        'site_settings': SiteSettings.objects.first(),
        'social_links': SocialLink.objects.filter(is_active=True),
    }
