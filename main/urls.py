from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('skills/', views.skill_list, name='skill_list'),
    path('journey/', views.journey, name='journey'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('search/', views.site_search, name='site_search'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/new/', views.blog_create, name='blog_create'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:pk>/edit/', views.blog_update, name='blog_update'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    path('contact/', views.contact, name='contact'),
    path('analytics/track-pageview/', views.track_pageview, name='track_pageview'),
    path('analytics/track-heartbeat/', views.track_heartbeat, name='track_heartbeat'),
]
