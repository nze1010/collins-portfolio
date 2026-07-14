from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Skill, BlogPost, UserProfile  # <-- UPDATED: Imported UserProfile here
from .forms import ContactForm, BlogPostForm


# ---------- HOMEPAGE ----------

def home(request):
    # Show a few skills and the latest blog posts as a preview on the homepage
    top_skills = Skill.objects.all()[:6]
    latest_posts = BlogPost.objects.all()[:3]
    
    # Fetch your profile details (grabs the first record you create in Admin)
    profile = UserProfile.objects.first()
    
    context = {
        'top_skills': top_skills,
        'latest_posts': latest_posts,
        'profile': profile, # Passed to the frontend template
    }
    return render(request, 'main/home.html', context)

# ---------- SKILLS PAGE ----------

def skill_list(request):
    # everything here comes straight from what was entered in the admin dashboard
    skills = Skill.objects.all()
    context = {'skills': skills}
    return render(request, 'main/skills.html', context)


# ---------- BLOG PAGES (CRUD) ----------

# READ (list) - show every blog post
def blog_list(request):
    posts = BlogPost.objects.all()
    context = {'posts': posts}
    return render(request, 'main/blog_list.html', context)


# READ (detail) - show one single blog post
def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    context = {'post': post}
    return render(request, 'main/blog_detail.html', context)


# CREATE - add a brand new blog post
@staff_member_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            new_post = form.save()
            messages.success(request, 'Your blog post was published successfully.')
            return redirect('blog_detail', pk=new_post.pk)
    else:
        form = BlogPostForm()

    context = {'form': form, 'page_title': 'Write a New Post'}
    return render(request, 'main/blog_form.html', context)


# UPDATE - edit an existing blog post
@staff_member_required
def blog_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        # passing instance=post tells Django to update this post
        # instead of creating a new one
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your blog post was updated successfully.')
            return redirect('blog_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)

    context = {'form': form, 'page_title': 'Edit Post'}
    return render(request, 'main/blog_form.html', context)


# DELETE - remove a blog post after the user confirms
@staff_member_required
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'The blog post was deleted.')
        return redirect('blog_list')

    context = {'post': post}
    return render(request, 'main/blog_confirm_delete.html', context)


# ---------- CONTACT PAGE ----------

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # this saves the name, email, subject and message straight to the DB
            form.save()
            messages.success(request, 'Thanks for reaching out! Your message has been sent.')
            return redirect('contact')
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'main/contact.html', context)
