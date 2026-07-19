import datetime
from django.utils import timezone
from django.db.models import Count, Avg
from django.db.models.functions import TruncDay
from .models import Visitor, PageView, ReadDuration

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

    # 4. Chart 2: Device breakdown (Mobile vs Desktop vs Tablet)
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

    # Update context dictionary with our custom fields
    context.update({
        'active_users': active_page_views,
        'total_visitors': total_visitors,
        'total_page_views': total_page_views,
        'avg_duration_min': round(avg_duration / 60, 1) if avg_duration else 0,
        'avg_scroll_percent': round(avg_scroll) if avg_scroll else 0,
        'chart_daily_labels': chart_daily_labels,
        'chart_daily_data': chart_daily_data,
        'chart_device_labels': chart_device_labels,
        'chart_device_data': chart_device_data,
        'chart_category_labels': chart_category_labels,
        'chart_category_data': chart_category_data,
        'popular_posts': formatted_popular_posts,
    })

    return context
