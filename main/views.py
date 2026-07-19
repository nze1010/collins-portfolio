from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .forms import BlogPostForm, ContactForm
from .models import (
    BlogPost,
    Certification,
    Experience,
    Organization,
    Project,
    Service,
    Skill,
    ToolkitItem,
    UserProfile,
    WorkSample,
)


RESEARCH_INTERESTS = [
    'Artificial Intelligence',
    'Renewable Energy',
    'Engineering Innovation',
    'Science & Technology',
    'African Development',
    'History & Archaeology',
    'Igbo Omenana',
    'Culture & Indigenous Knowledge',
    'Critical Thinking',
    'Religion & Society',
    'Media & Public Communication',
]


def home(request):
    skills = Skill.objects.all()
    projects = Project.objects.filter(is_published=True)
    services = Service.objects.filter(is_active=True)
    certifications = Certification.objects.filter(is_active=True)
    experiences = Experience.objects.filter(is_active=True)
    work_samples = WorkSample.objects.filter(is_active=True)

    featured_skills = skills.filter(is_featured=True)[:6]
    if not featured_skills:
        featured_skills = skills[:6]

    featured_projects = projects.filter(is_featured=True)[:3]
    if not featured_projects:
        featured_projects = projects[:3]

    featured_work = work_samples.filter(is_featured=True)[:6]
    if not featured_work:
        featured_work = work_samples[:6]

    context = {
        'profile': UserProfile.objects.first(),
        'top_skills': featured_skills,
        'featured_projects': featured_projects,
        'featured_work': featured_work,
        'services': services[:8],
        'certifications': certifications[:6],
        'experiences': experiences[:3],
        'toolkit_items': ToolkitItem.objects.filter(is_active=True),
        'latest_posts': BlogPost.objects.all()[:3],
        'contact_form': ContactForm(),
        'research_interests': RESEARCH_INTERESTS,
        'stats': [
            {'value': skills.count(), 'label': 'Core capabilities'},
            {'value': projects.count(), 'label': 'Documented projects'},
            {'value': services.count(), 'label': 'Professional services'},
            {'value': BlogPost.objects.count(), 'label': 'Published insights'},
        ],
    }
    return render(request, 'main/home.html', context)


def journey(request):
    experiences = Experience.objects.filter(is_active=True)
    organizations = Organization.objects.filter(is_active=True)
    certifications = Certification.objects.filter(is_active=True)
    featured_certifications = certifications.filter(is_featured=True)[:4]
    if not featured_certifications:
        featured_certifications = certifications[:4]

    return render(
        request,
        'main/journey.html',
        {
            'experiences': experiences,
            'organizations': organizations,
            'certifications': certifications,
            'featured_certifications': featured_certifications,
            'featured_projects': Project.objects.filter(is_published=True, is_featured=True)[:3],
            'journey_stats': [
                {'value': experiences.count(), 'label': 'Professional roles'},
                {'value': organizations.count(), 'label': 'Organizations'},
                {'value': certifications.count(), 'label': 'Credentials'},
            ],
        },
    )


def skill_list(request):
    skills = Skill.objects.all()
    categories = [
        {'key': key, 'label': label}
        for key, label in Skill.CATEGORY_CHOICES
        if skills.filter(category=key).exists()
    ]
    return render(request, 'main/skills.html', {'skills': skills, 'categories': categories})


def project_list(request):
    projects = Project.objects.filter(is_published=True)
    categories = projects.values_list('category', flat=True).distinct()
    work_samples = WorkSample.objects.filter(is_active=True)
    work_categories = [
        {'key': key, 'label': label}
        for key, label in WorkSample.CATEGORY_CHOICES
        if work_samples.filter(category=key).exists()
    ]
    return render(
        request,
        'main/project_list.html',
        {
            'projects': projects,
            'categories': categories,
            'work_samples': work_samples,
            'work_categories': work_categories,
        },
    )


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    related_projects = Project.objects.filter(
        is_published=True,
        category=project.category,
    ).exclude(pk=project.pk)[:3]
    return render(
        request,
        'main/project_detail.html',
        {'project': project, 'related_projects': related_projects},
    )


def site_search(request):
    query = request.GET.get('q', '').strip()
    result_groups = []

    def add_group(label, icon, results):
        results = list(results)
        if results:
            result_groups.append({'label': label, 'icon': icon, 'results': results})

    def result(title, description, url, meta=''):
        return {
            'title': title,
            'description': description,
            'url': url,
            'meta': meta,
        }

    if query:
        page_entries = [
            ('Home', 'Portfolio introduction and featured work.', reverse('home'), 'portfolio introduction'),
            ('About Me', 'Professional background, focus, and multidisciplinary interests.', f"{reverse('home')}#about", 'about biography profile'),
            ('Skills', 'Engineering, software, AI, research, and creative capabilities.', reverse('skill_list'), 'skills capabilities expertise'),
            ('Work', 'Projects, case studies, graphic design, and visual work.', reverse('project_list'), 'work projects gallery designs videos'),
            ('Professional Journey', 'Roles, organisations, qualifications, and credentials.', reverse('journey'), 'journey experience roles organizations organisations credentials certificates'),
            ('Insights', 'Technical articles, analysis, and research perspectives.', reverse('blog_list'), 'blog insights articles writing'),
            ('Contact', 'Start a professional enquiry or project conversation.', reverse('contact'), 'contact enquiry collaboration hire'),
        ]
        query_lower = query.lower()
        page_results = [
            result(title, description, url, 'Page')
            for title, description, url, keywords in page_entries
            if query_lower in f'{title} {description} {keywords}'.lower()
        ]
        add_group('Pages', 'search', page_results)

        skills = Skill.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__icontains=query)
        )[:10]
        add_group('Skills', 'engineering', (
            result(item.name, item.description, reverse('skill_list'), item.get_category_display())
            for item in skills
        ))

        projects = Project.objects.filter(is_published=True).filter(
            Q(title__icontains=query)
            | Q(category__icontains=query)
            | Q(short_description__icontains=query)
            | Q(details__icontains=query)
            | Q(technologies__icontains=query)
        )[:10]
        add_group('Projects', 'software', (
            result(item.title, item.short_description, item.get_absolute_url(), item.category)
            for item in projects
        ))

        work_samples = WorkSample.objects.filter(is_active=True).filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(client_or_company__icontains=query)
        )[:10]
        add_group('Visual Work', 'design', (
            result(item.title, item.description, f"{reverse('project_list')}#gallery", item.get_category_display())
            for item in work_samples
        ))

        services = Service.objects.filter(is_active=True).filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )[:10]
        add_group('Services', 'engineering', (
            result(item.title, item.description, f"{reverse('home')}#services", 'Professional service')
            for item in services
        ))

        posts = BlogPost.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(excerpt__icontains=query)
            | Q(category__icontains=query)
        )[:10]
        add_group('Insights', 'document', (
            result(item.title, item.excerpt or item.content, reverse('blog_detail', args=[item.pk]), item.category)
            for item in posts
        ))

        roles = Experience.objects.filter(is_active=True).filter(
            Q(role__icontains=query)
            | Q(company_name__icontains=query)
            | Q(organization__name__icontains=query)
            | Q(summary__icontains=query)
            | Q(highlights__icontains=query)
        )[:10]
        add_group('Professional Roles', 'briefcase', (
            result(item.role, item.summary, f"{reverse('journey')}#roles", item.display_organization)
            for item in roles
        ))

        organizations = Organization.objects.filter(is_active=True).filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )[:10]
        add_group('Organisations', 'building', (
            result(item.name, item.description, f"{reverse('journey')}#organizations", item.get_organization_type_display())
            for item in organizations
        ))

        credentials = Certification.objects.filter(is_active=True).filter(
            Q(title__icontains=query)
            | Q(issuer__icontains=query)
            | Q(description__icontains=query)
        )[:10]
        add_group('Credentials', 'award', (
            result(item.title, item.description, f"{reverse('journey')}#credentials", item.issuer or item.get_record_type_display())
            for item in credentials
        ))

        toolkit = ToolkitItem.objects.filter(is_active=True).filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        )[:10]
        add_group('Technology Toolkit', 'code', (
            result(item.name, item.category, f"{reverse('home')}#toolkit", item.category)
            for item in toolkit
        ))

        interests = [
            result(item, 'Research and professional interest', f"{reverse('home')}#research", 'Interest')
            for item in RESEARCH_INTERESTS
            if query_lower in item.lower()
        ]
        add_group('Research & Interests', 'research', interests)

    return render(
        request,
        'main/search.html',
        {
            'query': query,
            'result_groups': result_groups,
            'total_results': sum(len(group['results']) for group in result_groups),
        },
    )


def blog_list(request):
    posts = BlogPost.objects.all()
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(excerpt__icontains=query)
            | Q(category__icontains=query)
        )
    if category:
        posts = posts.filter(category=category)

    featured_post = BlogPost.objects.filter(is_featured=True).first()
    categories = BlogPost.objects.values_list('category', flat=True).distinct().order_by('category')
    return render(
        request,
        'main/blog_list.html',
        {
            'posts': posts,
            'featured_post': featured_post,
            'categories': categories,
            'query': query,
            'selected_category': category,
        },
    )


def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    related_posts = BlogPost.objects.filter(category=post.category).exclude(pk=post.pk)[:3]
    return render(
        request,
        'main/blog_detail.html',
        {'post': post, 'related_posts': related_posts},
    )


@staff_member_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save()
            messages.success(request, 'Your blog post was published successfully.')
            return redirect('blog_detail', pk=new_post.pk)
    else:
        form = BlogPostForm()

    return render(
        request,
        'main/blog_form.html',
        {'form': form, 'page_title': 'Write a New Post'},
    )


@staff_member_required
def blog_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your blog post was updated successfully.')
            return redirect('blog_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)

    return render(
        request,
        'main/blog_form.html',
        {'form': form, 'page_title': 'Edit Post'},
    )


@staff_member_required
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'The blog post was deleted.')
        return redirect('blog_list')

    return render(request, 'main/blog_confirm_delete.html', {'post': post})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Thanks for reaching out. Your message has been received and I will respond soon.',
            )
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})


@csrf_exempt
def track_pageview(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)
    try:
        data = json.loads(request.body)
        visitor_uuid = data.get('visitor_uuid')
        path = data.get('path', '/')
        referrer = data.get('referrer', '')
        blog_post_id = data.get('blog_post_id')
        
        # User details from headers
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip_address = ip_address.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')
            
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Device information from front-end data
        device_type = data.get('device_type', 'Unknown')
        browser = data.get('browser', 'Unknown')
        
        # Location information from front-end lookup
        country = data.get('country', 'Unknown')
        region = data.get('region', 'Unknown')
        city = data.get('city', 'Unknown')
        
        from .models import Visitor, PageView, BlogPost
        
        # Get or create Visitor
        visitor, created = Visitor.objects.get_or_create(
            session_key=visitor_uuid,
            defaults={
                'ip_address': ip_address,
                'user_agent': user_agent,
                'device_type': device_type,
                'browser': browser,
                'country': country,
                'region': region,
                'city': city,
            }
        )
        
        # Update details if changed or if they were unknown
        updated = False
        if visitor.ip_address != ip_address and ip_address:
            visitor.ip_address = ip_address
            updated = True
        if visitor.user_agent != user_agent and user_agent:
            visitor.user_agent = user_agent
            updated = True
        if country != 'Unknown' and visitor.country == 'Unknown':
            visitor.country = country
            visitor.region = region
            visitor.city = city
            updated = True
        if updated:
            visitor.save()
            
        # Check if it's a blog post view
        blog_post = None
        if blog_post_id:
            try:
                blog_post = BlogPost.objects.get(pk=blog_post_id)
            except BlogPost.DoesNotExist:
                pass
                
        # Create PageView
        page_view = PageView.objects.create(
            visitor=visitor,
            blog_post=blog_post,
            path=path,
            referrer=referrer
        )
        
        return JsonResponse({
            'status': 'success',
            'page_view_id': page_view.id,
            'visitor_id': visitor.id
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
def track_heartbeat(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)
    try:
        data = json.loads(request.body)
        page_view_id = data.get('page_view_id')
        duration_seconds = int(data.get('duration_seconds', 0))
        scroll_depth = int(data.get('scroll_depth', 0))
        
        from .models import PageView, ReadDuration
        
        page_view = PageView.objects.get(pk=page_view_id)
        
        # Get or create ReadDuration
        read_log, created = ReadDuration.objects.get_or_create(
            page_view=page_view,
            defaults={
                'duration_seconds': duration_seconds,
                'scroll_depth': scroll_depth
            }
        )
        
        if not created:
            # Update only if values are greater to keep the peak engagement stats
            if duration_seconds > read_log.duration_seconds:
                read_log.duration_seconds = duration_seconds
            if scroll_depth > read_log.scroll_depth:
                read_log.scroll_depth = scroll_depth
            read_log.save()
            
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

