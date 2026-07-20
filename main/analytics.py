import datetime
from django.utils import timezone
from django.db.models import Count, Avg
from django.db.models.functions import TruncDay, ExtractHour
from django.contrib.auth.models import User, Group
from .models import (
    Visitor, PageView, ReadDuration, BlogPost, Project, Skill,
    Certification, ContactMessage, Service, WorkSample, SocialLink,
    ToolkitItem, Organization, Experience, BlogComment, BlogReaction
)

def dashboard_callback(request, context):
    now = timezone.now()
    five_minutes_ago = now - datetime.timedelta(minutes=5)
    seven_days_ago = now - datetime.timedelta(days=7)

    # 1. Real-time active users (active in the last 5 minutes)
    active_page_views = PageView.objects.filter(
        duration_log__last_heartbeat__gte=five_minutes_ago
    ).values('visitor').distinct().count()

    # 2. Key Metrics
    total_visitors = Visitor.objects.count()
    total_page_views = PageView.objects.count()
    
    avg_duration = ReadDuration.objects.aggregate(avg=Avg('duration_seconds'))['avg'] or 0
    avg_scroll = ReadDuration.objects.aggregate(avg=Avg('scroll_depth'))['avg'] or 0

    # 3. Chart 1: Daily views over the last 7 days
    daily_views = PageView.objects.filter(viewed_at__gte=seven_days_ago) \
        .annotate(day=TruncDay('viewed_at')) \
        .values('day') \
        .annotate(count=Count('id')) \
        .order_by('day')
    
    chart_daily_labels = []
    chart_daily_data = []
    
    # Fill in potential zero days for the last 7 days
    day_map = { (now - datetime.timedelta(days=i)).date(): 0 for i in range(7) }
    for view in daily_views:
        v_date = view['day'].date()
        if v_date in day_map:
            day_map[v_date] = view['count']
            
    # Sort chronological
    sorted_days = sorted(day_map.keys())
    for d in sorted_days:
        chart_daily_labels.append(d.strftime('%b %d'))
        chart_daily_data.append(day_map[d])

    # 4. Chart 2: Device type breakdown (Mobile vs Desktop vs Tablet)
    device_data = Visitor.objects.values('device_type').annotate(count=Count('id'))
    chart_device_labels = []
    chart_device_data = []
    for item in device_data:
        chart_device_labels.append(item['device_type'] or 'Unknown')
        chart_device_data.append(item['count'])

    # 5. Chart 3: Category interests (PageViews grouped by Blog Post Category)
    category_data = PageView.objects.filter(blog_post__isnull=False) \
        .values('blog_post__category') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:5]
    chart_category_labels = []
    chart_category_data = []
    for item in category_data:
        chart_category_labels.append(item['blog_post__category'] or 'General')
        chart_category_data.append(item['count'])

    # 6. Popular articles list
    popular_posts = PageView.objects.filter(blog_post__isnull=False) \
        .values('blog_post__id', 'blog_post__title') \
        .annotate(
            views_count=Count('id'),
            avg_read=Avg('duration_log__duration_seconds'),
            avg_scroll=Avg('duration_log__scroll_depth')
        ).order_by('-views_count')[:5]

    # Format the stats inside popular posts list for UI readability
    formatted_popular_posts = []
    for post in popular_posts:
        raw_read = post['avg_read'] or 0
        raw_scroll = post['avg_scroll'] or 0
        formatted_popular_posts.append({
            'id': post['blog_post__id'],
            'title': post['blog_post__title'],
            'views': post['views_count'],
            'avg_read': f"{round(raw_read / 60, 1)}m" if raw_read >= 60 else f"{round(raw_read)}s",
            'avg_scroll': f"{round(raw_scroll)}%"
        })

    # 7. NEW: Phone brand breakdown (Samsung, Infinix, Apple, Tecno, Itel...)
    brand_data = Visitor.objects.values('device_brand') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:10]
    chart_brand_labels = []
    chart_brand_data = []
    for item in brand_data:
        chart_brand_labels.append(item['device_brand'] or 'Unknown')
        chart_brand_data.append(item['count'])

    # 8. NEW: Peak hours chart (what hours of the day get most traffic)
    hour_data = PageView.objects.annotate(hour=ExtractHour('viewed_at')) \
        .values('hour') \
        .annotate(count=Count('id')) \
        .order_by('hour')
    hour_map = {h: 0 for h in range(24)}
    for item in hour_data:
        hour_map[item['hour']] = item['count']
    chart_hour_labels = [f"{h:02d}:00" for h in range(24)]
    chart_hour_data = [hour_map[h] for h in range(24)]

    # 9. NEW: Top countries
    top_countries = Visitor.objects.exclude(country='Unknown') \
        .values('country') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:8]
    chart_country_labels = [c['country'] for c in top_countries]
    chart_country_data = [c['count'] for c in top_countries]

    # 10. NEW: Top referrers (traffic sources)
    top_referrers = PageView.objects.exclude(referrer='') \
        .exclude(referrer__isnull=True) \
        .values('referrer') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:5]
    formatted_referrers = []
    for ref in top_referrers:
        raw = ref['referrer'] or ''
        # Shorten long referrer URLs to just the domain
        try:
            from urllib.parse import urlparse
            domain = urlparse(raw).netloc or raw[:40]
        except Exception:
            domain = raw[:40]
        formatted_referrers.append({'source': domain, 'count': ref['count']})

    # Update context dictionary with our custom fields
    context.update({
        'active_users': active_page_views,
        'total_visitors': total_visitors,
        'total_page_views': total_page_views,
        'avg_duration_min': round(avg_duration / 60, 1) if avg_duration else 0,
        'avg_scroll_percent': round(avg_scroll) if avg_scroll else 0,
        # Daily views chart
        'chart_daily_labels': chart_daily_labels,
        'chart_daily_data': chart_daily_data,
        # Device type chart
        'chart_device_labels': chart_device_labels,
        'chart_device_data': chart_device_data,
        # Blog category chart
        'chart_category_labels': chart_category_labels,
        'chart_category_data': chart_category_data,
        # Popular posts table
        'popular_posts': formatted_popular_posts,
        # Comments & Reactions counts
        'total_comments': BlogComment.objects.count(),
        'total_reactions': BlogReaction.objects.count(),
        # NEW: Phone brand chart
        'chart_brand_labels': chart_brand_labels,
        'chart_brand_data': chart_brand_data,
        # NEW: Peak hours chart
        'chart_hour_labels': chart_hour_labels,
        'chart_hour_data': chart_hour_data,
        # NEW: Top countries chart
        'chart_country_labels': chart_country_labels,
        'chart_country_data': chart_country_data,
        # NEW: Top referrers
        'top_referrers': formatted_referrers,
        # Model Counts for Control Panel Grid
        'count_blog_posts': BlogPost.objects.count(),
        'count_projects': Project.objects.count(),
        'count_skills': Skill.objects.count(),
        'count_credentials': Certification.objects.count(),
        'count_messages': ContactMessage.objects.count(),
        'count_services': Service.objects.count(),
        'count_work_samples': WorkSample.objects.count(),
        'count_social_links': SocialLink.objects.count(),
        'count_organizations': Organization.objects.count(),
        'count_experiences': Experience.objects.count(),
        'count_toolkit_items': ToolkitItem.objects.count(),
        'count_users': User.objects.count(),
        'count_groups': Group.objects.count(),
    })

    return context
