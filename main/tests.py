from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import (
    BlogPost,
    ContactMessage,
    Experience,
    Organization,
    Project,
    SiteSettings,
    Skill,
    SocialLink,
    WorkSample,
)


class BlogAccessTests(TestCase):
    def setUp(self):
        self.post = BlogPost.objects.create(
            title='Test post',
            content='Test content',
        )
        self.staff_user = get_user_model().objects.create_user(
            username='staff',
            password='test-password',
            is_staff=True,
        )

    def test_blog_reading_is_public(self):
        self.assertEqual(self.client.get(reverse('blog_list')).status_code, 200)
        self.assertEqual(
            self.client.get(reverse('blog_detail', args=[self.post.pk])).status_code,
            200,
        )

    def test_blog_management_redirects_anonymous_users(self):
        protected_urls = [
            reverse('blog_create'),
            reverse('blog_update', args=[self.post.pk]),
            reverse('blog_delete', args=[self.post.pk]),
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f"{reverse('admin:login')}?next={url}",
                )

    def test_staff_users_can_open_blog_management_pages(self):
        self.client.force_login(self.staff_user)

        self.assertEqual(self.client.get(reverse('blog_create')).status_code, 200)
        self.assertEqual(
            self.client.get(reverse('blog_update', args=[self.post.pk])).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse('blog_delete', args=[self.post.pk])).status_code,
            200,
        )

    def test_blog_search_filters_results(self):
        BlogPost.objects.create(title='Solar engineering', content='Renewable energy guide')

        response = self.client.get(reverse('blog_list'), {'q': 'Solar'})

        self.assertContains(response, 'Solar engineering')
        self.assertNotContains(response, self.post.title)

    def test_reading_time_has_a_one_minute_minimum(self):
        self.assertEqual(self.post.reading_time, 1)


class PublicPortfolioTests(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(
            name='Systems Engineering',
            description='Designing dependable technical systems.',
            category='engineering',
        )
        self.project = Project.objects.create(
            title='Portfolio Test Project',
            category='Django Web Applications',
            short_description='A safely managed Django project.',
            technologies='Python, Django',
            is_published=True,
        )

    def test_primary_public_pages_render(self):
        pages = [
            reverse('home'),
            reverse('skill_list'),
            reverse('project_list'),
            reverse('project_detail', kwargs={'slug': self.project.slug}),
            reverse('journey'),
            reverse('site_search'),
            reverse('blog_list'),
            reverse('contact'),
        ]

        for url in pages:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_global_search_finds_content_across_portfolio_sections(self):
        skill_response = self.client.get(reverse('site_search'), {'q': 'Systems Engineering'})
        project_response = self.client.get(reverse('site_search'), {'q': 'Portfolio Test Project'})

        self.assertContains(skill_response, 'Systems Engineering')
        self.assertContains(skill_response, 'Skills')
        self.assertContains(project_response, 'Portfolio Test Project')
        self.assertContains(project_response, self.project.get_absolute_url())

    def test_global_search_excludes_unpublished_and_inactive_content(self):
        Project.objects.create(
            title='Confidential Search Project',
            category='Research',
            short_description='This private project must not appear in search.',
            is_published=False,
        )
        Organization.objects.create(
            name='Confidential Search Organisation',
            organization_type='enterprise',
            description='This inactive organisation must not appear in search.',
            is_active=False,
        )

        response = self.client.get(reverse('site_search'), {'q': 'Confidential Search'})

        self.assertNotContains(response, 'Confidential Search Project')
        self.assertNotContains(response, 'Confidential Search Organisation')

    def test_header_has_accessible_site_search_and_global_watermark(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'id="global-search-toggle"')
        self.assertContains(response, 'id="site-search-dialog"')
        self.assertContains(response, 'class="site-watermark"')
        self.assertContains(response, 'main/brand-logo.svg')

    def test_site_wide_local_greeting_and_clock_are_available(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'class="visitor-timebar"')
        self.assertContains(response, 'data-visitor-greeting')
        self.assertContains(response, 'data-local-date')
        self.assertContains(response, 'data-local-time')
        self.assertContains(response, 'data-local-timezone')

    def test_admin_watermark_upload_replaces_default_logo(self):
        settings = SiteSettings.objects.get(pk=1)
        settings.background_watermark = 'site_branding/custom-watermark.jpg'
        settings.save()

        response = self.client.get(reverse('home'))

        self.assertContains(response, '/media/site_branding/custom-watermark.jpg')

    def test_whatsapp_contact_link_uses_international_number(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'https://wa.me/2348037479362')
        self.assertContains(response, 'Chat with CollinsTechEmpire on WhatsApp')

    def test_light_and_dark_theme_control_is_available(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'id="theme-toggle"')
        self.assertContains(response, 'Switch to light theme')
        self.assertNotContains(response, '>Light mode<')
        self.assertNotContains(response, '>Dark mode<')

    def test_homepage_does_not_render_the_legacy_supporting_text(self):
        from .models import SiteSettings

        settings = SiteSettings.objects.get(pk=1)
        settings.hero_intro = 'Current hero introduction.'
        settings.supporting_text = 'Legacy supporting sentence that should stay hidden.'
        settings.save()

        response = self.client.get(reverse('home'))

        self.assertContains(response, 'Current hero introduction.')
        self.assertNotContains(response, 'Legacy supporting sentence that should stay hidden.')

    def test_social_platforms_automatically_select_matching_icons(self):
        platforms = {
            'Facebook': 'facebook',
            'Instagram': 'instagram',
            'Gmail': 'gmail',
            'WhatsApp': 'whatsapp',
        }

        for order, (platform, icon_name) in enumerate(platforms.items(), start=10):
            social_link = SocialLink.objects.create(
                platform=platform,
                url=f'https://example.com/{icon_name}/',
                order=order,
            )
            self.assertEqual(social_link.icon_name, icon_name)

        response = self.client.get(reverse('home'))
        for icon_name in platforms.values():
            self.assertContains(response, f'#icon-{icon_name}')

    def test_unpublished_project_is_not_public(self):
        private_project = Project.objects.create(
            title='Private Project',
            category='Research',
            short_description='Not ready for publication.',
            is_published=False,
        )

        self.assertEqual(
            self.client.get(private_project.get_absolute_url()).status_code,
            404,
        )

    def test_project_generates_unique_slugs(self):
        duplicate = Project.objects.create(
            title=self.project.title,
            category='Research',
            short_description='Another project with the same title.',
        )

        self.assertEqual(self.project.slug, 'portfolio-test-project')
        self.assertEqual(duplicate.slug, 'portfolio-test-project-2')

    def test_professional_experience_appears_on_journey_page(self):
        Experience.objects.create(
            company_name='Example Engineering Company',
            role='Electrical Engineer',
            start_date='2024-01-01',
            summary='Delivered practical engineering support.',
        )

        response = self.client.get(reverse('journey'))

        self.assertContains(response, 'Example Engineering Company')
        self.assertContains(response, 'Electrical Engineer')

    def test_seeded_journey_has_three_complete_content_sections(self):
        response = self.client.get(reverse('journey'))

        self.assertContains(response, 'data-counter="17"')
        self.assertContains(response, 'data-counter="6"', count=2)
        self.assertContains(response, 'Creative Graphic Designer and Visual Content Specialist')
        self.assertContains(response, 'BLord Group')
        self.assertContains(response, 'Higher National Diploma in Electrical/Electronics Engineering')
        self.assertContains(response, 'class="credential-status is-verified"', count=2)
        self.assertContains(response, 'Professional training record')
        self.assertContains(response, 'class="journey-number"', count=23)
        self.assertContains(response, 'aria-label="Professional role 1"')
        self.assertContains(response, 'aria-label="Organisation 1"')
        self.assertNotContains(response, 'class="company-identity"')
        self.assertNotContains(response, 'class="organization-mark"')

    def test_public_blog_pages_do_not_show_staff_publishing_controls(self):
        post = BlogPost.objects.create(
            title='Public interface audit',
            content='A published article used to verify the visitor experience.',
        )
        self.client.force_login(get_user_model().objects.create_superuser(
            username='public-page-auditor',
            email='auditor@example.com',
            password='test-password',
        ))

        list_response = self.client.get(reverse('blog_list'))
        detail_response = self.client.get(reverse('blog_detail', args=[post.pk]))

        self.assertNotContains(list_response, 'Publish new article')
        self.assertNotContains(detail_response, 'Edit article')
        self.assertNotContains(detail_response, '>Delete</a>')

    def test_skill_and_project_filters_are_connected_to_their_grids(self):
        skill_response = self.client.get(reverse('skill_list'))
        project_response = self.client.get(reverse('project_list'))

        self.assertContains(skill_response, 'data-filter-target="#skill-grid"')
        self.assertContains(project_response, 'data-filter-target="#project-grid"')
        self.assertContains(skill_response, 'aria-pressed="true"')
        self.assertContains(project_response, 'aria-pressed="true"')

    def test_experience_period_uses_admin_label_or_dates(self):
        labelled = Experience(period_label='2021 — Present')
        dated = Experience(start_date=date(2022, 1, 1), end_date=date(2024, 1, 1))

        self.assertEqual(labelled.display_period, '2021 — Present')
        self.assertEqual(dated.display_period, '2022 — 2024')

    def test_inactive_organization_is_not_public(self):
        Organization.objects.create(
            name='Private Test Organisation',
            organization_type='enterprise',
            description='This organisation is intentionally hidden.',
            is_active=False,
        )

        response = self.client.get(reverse('journey'))

        self.assertNotContains(response, 'Private Test Organisation')

    def test_active_work_samples_appear_in_the_visual_gallery(self):
        WorkSample.objects.create(
            title='Campaign Identity Design',
            category='graphic_design',
            description='A visual identity prepared for a professional campaign.',
            image='work_samples/campaign-identity.jpg',
            is_featured=True,
        )

        work_response = self.client.get(reverse('project_list'))
        home_response = self.client.get(reverse('home'))

        self.assertContains(work_response, 'Visual Work Gallery')
        self.assertContains(work_response, 'Campaign Identity Design')
        self.assertContains(work_response, '/media/work_samples/campaign-identity.jpg')
        self.assertContains(home_response, 'Campaign Identity Design')

    def test_inactive_work_samples_are_not_public(self):
        WorkSample.objects.create(
            title='Private Draft Design',
            category='branding',
            image='work_samples/private-draft.jpg',
            is_active=False,
        )

        self.assertNotContains(self.client.get(reverse('project_list')), 'Private Draft Design')

    def test_contact_form_saves_to_existing_message_model(self):
        response = self.client.post(
            reverse('contact'),
            {
                'name': 'Portfolio Visitor',
                'email': 'visitor@example.com',
                'enquiry_type': 'django',
                'subject': 'Django collaboration',
                'message': 'I would like to discuss a Django project.',
            },
        )

        self.assertRedirects(response, reverse('contact'))
        self.assertTrue(
            ContactMessage.objects.filter(email='visitor@example.com').exists()
        )

    def test_invalid_contact_form_shows_validation_errors(self):
        response = self.client.post(
            reverse('contact'),
            {'name': 'Visitor', 'email': 'invalid-email', 'message': ''},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'email', 'Enter a valid email address.')
        self.assertFormError(response.context['form'], 'message', 'This field is required.')


class AdminAccessTests(TestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
            username='administrator',
            email='admin@example.com',
            password='test-password',
        )
        self.client.force_login(self.superuser)

    def test_preserved_and_new_models_are_available_in_admin(self):
        admin_pages = [
            'admin:main_skill_changelist',
            'admin:main_blogpost_changelist',
            'admin:main_contactmessage_changelist',
            'admin:main_userprofile_changelist',
            'admin:main_project_changelist',
            'admin:main_worksample_changelist',
            'admin:main_service_changelist',
            'admin:main_certification_changelist',
            'admin:main_experience_changelist',
            'admin:main_organization_changelist',
            'admin:main_toolkititem_changelist',
            'admin:main_sociallink_changelist',
            'admin:main_sitesettings_changelist',
        ]

        for page_name in admin_pages:
            with self.subTest(page_name=page_name):
                self.assertEqual(self.client.get(reverse(page_name)).status_code, 200)

    def test_site_settings_admin_hides_supporting_text_field(self):
        from .models import SiteSettings

        settings = SiteSettings.objects.get(pk=1)
        response = self.client.get(
            reverse('admin:main_sitesettings_change', args=[settings.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'name="supporting_text"')
