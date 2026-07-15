from django.contrib import admin

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
)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'is_featured', 'order')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('is_featured', 'order')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_featured', 'created_at', 'updated_at')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'content', 'author')
    list_editable = ('is_featured',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'enquiry_type', 'subject', 'submitted_at')
    list_filter = ('enquiry_type', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'enquiry_type', 'subject', 'message', 'submitted_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'professional_title')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'is_published', 'order')
    list_filter = ('category', 'is_featured', 'is_published')
    search_fields = ('title', 'short_description', 'details', 'technologies')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured', 'is_published', 'order')


@admin.register(WorkSample)
class WorkSampleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client_or_company', 'project_date', 'is_featured', 'is_active', 'order')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('title', 'description', 'client_or_company')
    list_editable = ('is_featured', 'is_active', 'order')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_name', 'is_active', 'order')
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'order')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'record_type', 'issuer', 'date_earned', 'is_verified', 'is_featured', 'is_active', 'order')
    list_filter = ('record_type', 'is_verified', 'is_featured', 'is_active', 'issuer')
    search_fields = ('title', 'issuer', 'description')
    list_editable = ('is_verified', 'is_featured', 'is_active', 'order')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization_type', 'is_featured', 'is_active', 'order')
    list_filter = ('organization_type', 'is_featured', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('is_featured', 'is_active', 'order')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'organization', 'company_name', 'employment_type', 'start_date', 'period_label', 'is_current', 'is_featured', 'is_active', 'order')
    list_filter = ('employment_type', 'is_current', 'is_featured', 'is_active')
    search_fields = ('role', 'organization__name', 'company_name', 'location', 'summary', 'highlights')
    autocomplete_fields = ('organization',)
    list_editable = ('is_current', 'is_featured', 'is_active', 'order')


@admin.register(ToolkitItem)
class ToolkitItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon_name', 'is_active', 'order')
    list_filter = ('category', 'is_active')
    list_editable = ('is_active', 'order')


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'icon_name', 'is_active', 'order')
    list_editable = ('icon_name', 'is_active', 'order')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'availability_status')
    exclude = ('supporting_text',)

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
