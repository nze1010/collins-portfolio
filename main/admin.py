from django.contrib import admin
from .models import Skill, BlogPost, ContactMessage, UserProfile  # Added UserProfile here


# Registering Skill here is what lets us add/edit/delete skills
# from the admin dashboard - that's the "upload your skills from
# your admin dashboard" part of the assignment.
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency', 'created_at')
    search_fields = ('name',)
    list_editable = ('proficiency',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')


# we register ContactMessage too so we can read incoming messages
# from the admin dashboard, even though they get created from the frontend
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'submitted_at')


# Registering UserProfile so you can upload your luxury avatar
# and manage your corporate branding details from the dashboard
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'professional_title')