from django.db import models


# This model stores each skill that will show up on the Skills page.
# We fill this in from the Django admin dashboard, and the frontend
# just reads and displays whatever is saved here.
class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # a number from 0 to 100 so we can show a progress bar on the frontend
    proficiency = models.PositiveIntegerField(default=50)
    # optional icon/image for the skill, uploaded from admin
    icon = models.ImageField(upload_to='skill_icons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-proficiency', 'name']

    def __str__(self):
        return self.name


# This model represents a single blog post. Users will be able to
# Create, Read, Update and Delete these from the frontend.
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, default='Engr Collins')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# This model stores every message a visitor sends through the Contact page.
# The Django form on the frontend collects the input, and views.py saves
# it here so we have a record of it in the database.
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return self.name + ' - ' + self.subject




class UserProfile(models.Model):
    # This field handles your luxury profile image upload
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Optional fields you can add to edit your titles from the admin panel later
    professional_title = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return "CollinsTech Professional Profile"