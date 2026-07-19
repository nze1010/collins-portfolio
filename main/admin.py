from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    BlogPost,
    Certification,
    ContactMessage,
    Experience,
    Organization,
    Project,
    Service,
    SiteSettings,
    Skill,
    SocialLink,
    ToolkitItem,
    UserProfile,
    WorkSample,
    Visitor,
    PageView,
    ReadDuration,
)


@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'is_featured', 'order')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('is_featured', 'order')


@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_featured', 'created_at', 'updated_at')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'content', 'author')
    list_editable = ('is_featured',)
    
    readonly_fields = ('article_views_count', 'average_reading_duration', 'average_scroll_completion')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author', 'category', 'excerpt', 'cover_image', 'is_featured')
        }),
        ('Reader Insights & Analytics', {
            'fields': ('article_views_count', 'average_reading_duration', 'average_scroll_completion'),
        }),
    )

    def article_views_count(self, obj):
        if not obj.id:
            return 0
        return obj.page_views.count()
    article_views_count.short_description = "Total Page Views"

    def average_reading_duration(self, obj):
        if not obj.id:
            return "0s"
        from django.db.models import Avg
        avg = obj.page_views.aggregate(avg=Avg('duration_log__duration_seconds'))['avg']
        if avg:
            return f"{round(avg / 60, 1)} minutes" if avg >= 60 else f"{round(avg)} seconds"
        return "0 seconds"
    average_reading_duration.short_description = "Avg Reading Time"

    def average_scroll_completion(self, obj):
        if not obj.id:
            return "0%"
        from django.db.models import Avg
        avg = obj.page_views.aggregate(avg=Avg('duration_log__scroll_depth'))['avg']
        return f"{round(avg or 0)}%"
    average_scroll_completion.short_description = "Avg Scroll Depth"


@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ('name', 'email', 'enquiry_type', 'subject', 'submitted_at')
    list_filter = ('enquiry_type', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'enquiry_type', 'subject', 'message', 'submitted_at')


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ('full_name', 'professional_title')


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'is_published', 'order')
    list_filter = ('category', 'is_featured', 'is_published')
    search_fields = ('title', 'short_description', 'details', 'technologies')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured', 'is_published', 'order')


@admin.register(WorkSample)
class WorkSampleAdmin(ModelAdmin):
    list_display = ('title', 'category', 'client_or_company', 'project_date', 'is_featured', 'is_active', 'order')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('title', 'description', 'client_or_company')
    list_editable = ('is_featured', 'is_active', 'order')


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ('title', 'icon_name', 'is_active', 'order')
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'order')


@admin.register(Certification)
class CertificationAdmin(ModelAdmin):
    list_display = ('title', 'record_type', 'issuer', 'date_earned', 'is_verified', 'is_featured', 'is_active', 'order')
    list_filter = ('record_type', 'is_verified', 'is_featured', 'is_active', 'issuer')
    search_fields = ('title', 'issuer', 'description')
    list_editable = ('is_verified', 'is_featured', 'is_active', 'order')


@admin.register(Organization)
class OrganizationAdmin(ModelAdmin):
    list_display = ('name', 'organization_type', 'is_featured', 'is_active', 'order')
    list_filter = ('organization_type', 'is_featured', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('is_featured', 'is_active', 'order')


@admin.register(Experience)
class ExperienceAdmin(ModelAdmin):
    list_display = ('role', 'organization', 'company_name', 'employment_type', 'start_date', 'period_label', 'is_current', 'is_featured', 'is_active', 'order')
    list_filter = ('employment_type', 'is_current', 'is_featured', 'is_active')
    search_fields = ('role', 'organization__name', 'company_name', 'location', 'summary', 'highlights')
    autocomplete_fields = ('organization',)
    list_editable = ('is_current', 'is_featured', 'is_active', 'order')


@admin.register(ToolkitItem)
class ToolkitItemAdmin(ModelAdmin):
    list_display = ('name', 'category', 'icon_name', 'is_active', 'order')
    list_filter = ('category', 'is_active')
    list_editable = ('is_active', 'order')


@admin.register(SocialLink)
class SocialLinkAdmin(ModelAdmin):
    list_display = ('platform', 'url', 'icon_name', 'is_active', 'order')
    list_editable = ('icon_name', 'is_active', 'order')


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    list_display = ('brand_name', 'availability_status')
    exclude = ('supporting_text',)

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# Analytics registrations
@admin.register(Visitor)
class VisitorAdmin(ModelAdmin):
    list_display = ('session_key_short', 'ip_address', 'device_type', 'browser', 'country', 'city', 'created_at')
    list_filter = ('device_type', 'browser', 'country', 'created_at')
    search_fields = ('session_key', 'ip_address', 'user_agent', 'country', 'city')
    readonly_fields = ('session_key', 'ip_address', 'user_agent', 'device_type', 'browser', 'country', 'region', 'city', 'created_at')
    
    def session_key_short(self, obj):
        return obj.session_key[:8]
    session_key_short.short_description = "Visitor UUID"


@admin.register(PageView)
class PageViewAdmin(ModelAdmin):
    list_display = ('visitor_link', 'path', 'blog_post', 'referrer_short', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('visitor__session_key', 'path', 'referrer')
    readonly_fields = ('visitor', 'blog_post', 'path', 'referrer', 'viewed_at')

    def visitor_link(self, obj):
        return obj.visitor.session_key[:8]
    visitor_link.short_description = "Visitor"

    def referrer_short(self, obj):
        if obj.referrer:
            return obj.referrer[:40] + ('...' if len(obj.referrer) > 40 else '')
        return '-'
    referrer_short.short_description = "Referrer"


@admin.register(ReadDuration)
class ReadDurationAdmin(ModelAdmin):
    list_display = ('page_view_path', 'visitor_short', 'duration_seconds_formatted', 'scroll_depth_formatted', 'last_heartbeat')
    readonly_fields = ('page_view', 'duration_seconds', 'scroll_depth', 'last_heartbeat')

    def page_view_path(self, obj):
        return obj.page_view.path
    page_view_path.short_description = "Path"

    def visitor_short(self, obj):
        return obj.page_view.visitor.session_key[:8]
    visitor_short.short_description = "Visitor"

    def duration_seconds_formatted(self, obj):
        return f"{obj.duration_seconds}s"
    duration_seconds_formatted.short_description = "Time Spent"

    def scroll_depth_formatted(self, obj):
        return f"{obj.scroll_depth}%"
    scroll_depth_formatted.short_description = "Scroll Depth"
