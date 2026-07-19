import math

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('ai', 'Artificial Intelligence'),
        ('software', 'Software Development'),
        ('engineering', 'Engineering'),
        ('energy', 'Renewable Energy'),
        ('research', 'Research & Communication'),
        ('creative', 'Digital Creativity'),
        ('operations', 'Professional Operations'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, blank=True)
    proficiency = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Optional. Leave blank rather than using an estimated percentage.',
    )
    icon = models.ImageField(upload_to='skill_icons/', blank=True, null=True)
    icon_name = models.CharField(max_length=30, default='code', blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, default='Engr. Josiah Collins Chinaza')
    category = models.CharField(max_length=80, default='Technology')
    excerpt = models.TextField(blank=True, help_text='Optional short summary for article cards.')
    cover_image = models.ImageField(upload_to='blog_covers/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def reading_time(self):
        return max(1, math.ceil(len(self.content.split()) / 200))

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    ENQUIRY_CHOICES = [
        ('engineering', 'Engineering consultation'),
        ('solar', 'Solar and electrical services'),
        ('django', 'Django development'),
        ('ai', 'AI collaboration'),
        ('research', 'Research and writing'),
        ('creative', 'Design and digital content'),
        ('general', 'General enquiry'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    enquiry_type = models.CharField(max_length=30, choices=ENQUIRY_CHOICES, blank=True)
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.name} - {self.subject}'


class UserProfile(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    full_name = models.CharField(max_length=200, default='Engr. Josiah Collins Chinaza')
    professional_title = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    long_bio = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.full_name or 'CollinsTech Professional Profile'


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=100)
    short_description = models.TextField()
    details = models.TextField(blank=True)
    technologies = models.CharField(
        max_length=500,
        blank=True,
        help_text='Comma-separated technologies and tools.',
    )
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'project'
            slug = base_slug
            counter = 2
            while Project.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def technology_list(self):
        return [item.strip() for item in self.technologies.split(',') if item.strip()]

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class WorkSample(models.Model):
    CATEGORY_CHOICES = [
        ('graphic_design', 'Graphic Design'),
        ('video', 'Video & Motion'),
        ('branding', 'Branding'),
        ('web', 'Web & UI Design'),
        ('engineering', 'Engineering Work'),
        ('photography', 'Photography'),
        ('other', 'Other Creative Work'),
    ]

    title = models.CharField(max_length=180)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='work_samples/',
        help_text='Upload the finished design or a clear screenshot/thumbnail of the work.',
    )
    client_or_company = models.CharField(max_length=160, blank=True)
    project_date = models.DateField(blank=True, null=True)
    video_url = models.URLField(
        blank=True,
        help_text='Optional link to YouTube, Vimeo, Google Drive, or another video page.',
    )
    external_url = models.URLField(blank=True, help_text='Optional project or campaign link.')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-project_date', '-created_at']

    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_name = models.CharField(max_length=30, default='code')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Certification(models.Model):
    RECORD_TYPE_CHOICES = [
        ('certificate', 'Certificate'),
        ('qualification', 'Educational qualification'),
        ('training', 'Professional training'),
        ('seminar', 'Seminar'),
    ]

    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=150, blank=True)
    record_type = models.CharField(
        max_length=20,
        choices=RECORD_TYPE_CHOICES,
        default='certificate',
    )
    description = models.TextField(blank=True)
    date_earned = models.DateField(blank=True, null=True)
    credential_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    credential_id = models.CharField(max_length=120, blank=True)
    is_verified = models.BooleanField(
        default=False,
        help_text='Select only when supporting evidence or a verification link is available.',
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-date_earned']
        verbose_name = 'credential'
        verbose_name_plural = 'credentials'

    def __str__(self):
        return self.title


class Organization(models.Model):
    TYPE_CHOICES = [
        ('employer', 'Employer'),
        ('enterprise', 'Enterprise'),
        ('platform', 'Media or digital platform'),
        ('practice', 'Independent practice'),
    ]

    name = models.CharField(max_length=180, unique=True)
    organization_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    logo = models.ImageField(upload_to='organization_logos/', blank=True, null=True)
    website_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Experience(models.Model):
    EMPLOYMENT_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
        ('volunteer', 'Volunteer'),
        ('self_employed', 'Self-employed'),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        related_name='professional_roles',
        blank=True,
        null=True,
    )
    company_name = models.CharField(
        max_length=180,
        help_text='Organisation name shown when no Organisation record is selected.',
    )
    role = models.CharField(max_length=180)
    employment_type = models.CharField(max_length=30, choices=EMPLOYMENT_CHOICES, blank=True)
    location = models.CharField(max_length=150, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    period_label = models.CharField(
        max_length=80,
        blank=True,
        help_text='Use when the exact starting date is unknown, for example "Present".',
    )
    is_current = models.BooleanField(default=False)
    summary = models.TextField(blank=True)
    highlights = models.TextField(
        blank=True,
        help_text='Optional. Enter one achievement per line.',
    )
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_current', 'order', '-start_date']
        verbose_name = 'professional role'
        verbose_name_plural = 'professional roles'

    @property
    def highlight_list(self):
        return [line.strip() for line in self.highlights.splitlines() if line.strip()]

    @property
    def display_organization(self):
        return self.organization.name if self.organization else self.company_name

    @property
    def display_logo(self):
        if self.company_logo:
            return self.company_logo
        if self.organization and self.organization.logo:
            return self.organization.logo
        return None

    @property
    def display_period(self):
        if self.period_label:
            return self.period_label
        if not self.start_date:
            return 'Present' if self.is_current else ''

        start = str(self.start_date.year)
        if self.is_current:
            return f'{start} — Present'
        if self.end_date:
            return f'{start} — {self.end_date.year}'
        return start

    def __str__(self):
        return f'{self.role} at {self.company_name}'


class ToolkitItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)
    icon_name = models.CharField(max_length=30, default='code')
    url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    ICON_CHOICES = [
        ('external', 'Generic link'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('gmail', 'Gmail / Email'),
        ('whatsapp', 'WhatsApp'),
        ('github', 'GitHub'),
    ]

    platform = models.CharField(max_length=80)
    url = models.URLField()
    icon_name = models.CharField(max_length=30, choices=ICON_CHOICES, default='external')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'platform']

    def save(self, *args, **kwargs):
        platform_key = self.platform.lower()
        automatic_icons = {
            'facebook': 'facebook',
            'instagram': 'instagram',
            'gmail': 'gmail',
            'email': 'gmail',
            'mail': 'gmail',
            'whatsapp': 'whatsapp',
            'github': 'github',
        }
        if not self.icon_name or self.icon_name == 'external':
            for platform_name, icon_name in automatic_icons.items():
                if platform_name in platform_key:
                    self.icon_name = icon_name
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.platform


class SiteSettings(models.Model):
    brand_name = models.CharField(max_length=100, default='CollinsTechEmpire')
    availability_status = models.CharField(
        max_length=220,
        default='Available for engineering, AI, software, research, and digital projects',
    )
    hero_headline = models.CharField(
        max_length=255,
        default='Electrical Engineer, AI Professional & Python/Django Developer',
    )
    hero_intro = models.TextField(
        default=(
            'I build practical solutions through engineering, AI, software, '
            'renewable energy, research, and digital creativity.'
        )
    )
    supporting_text = models.TextField(
        default=(
            'Through CollinsTechEmpire, I turn technology into useful products, '
            'systems, and technical content.'
        )
    )
    footer_statement = models.TextField(
        default=(
            'CollinsTechEmpire combines engineering, artificial intelligence, software '
            'development, renewable energy, research, and digital creativity to build '
            'practical solutions for a changing world.'
        )
    )
    background_watermark = models.ImageField(
        upload_to='site_branding/',
        blank=True,
        null=True,
        help_text=(
            'Optional faint image shown across the public website. Upload a logo or '
            'professional portrait; the CollinsTechEmpire logo is used when left blank.'
        ),
    )

    class Meta:
        verbose_name_plural = 'Site settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return None

    def __str__(self):
        return self.brand_name


class Visitor(models.Model):
    session_key = models.CharField(max_length=100, unique=True, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    device_type = models.CharField(max_length=20, default='Unknown')
    browser = models.CharField(max_length=50, default='Unknown')
    country = models.CharField(max_length=100, default='Unknown')
    region = models.CharField(max_length=100, default='Unknown')
    city = models.CharField(max_length=100, default='Unknown')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Visitor {self.session_key[:8]} ({self.country}, {self.device_type})"


class PageView(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='page_views')
    blog_post = models.ForeignKey(BlogPost, null=True, blank=True, on_delete=models.SET_NULL, related_name='page_views')
    path = models.CharField(max_length=255)
    referrer = models.TextField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.path} viewed by {self.visitor.session_key[:8]} at {self.viewed_at.strftime('%Y-%m-%d %H:%M')}"


class ReadDuration(models.Model):
    page_view = models.OneToOneField(PageView, on_delete=models.CASCADE, related_name='duration_log')
    duration_seconds = models.PositiveIntegerField(default=0)
    scroll_depth = models.PositiveIntegerField(default=0)
    last_heartbeat = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_heartbeat']

    def __str__(self):
        return f"{self.duration_seconds}s read depth {self.scroll_depth}% for {self.page_view}"


class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField(blank=True, null=True)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author_name} on {self.post.title}"


class BlogReaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('clap', 'Clap'),
        ('insightful', 'Insightful'),
    ]

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    session_id = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'reaction_type', 'session_id')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.reaction_type} by {self.session_id[:8]} on {self.post.title}"

