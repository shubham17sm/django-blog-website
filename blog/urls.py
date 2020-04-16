from django.urls import path, include 
from django.conf.urls.static import static
from django.conf import settings

from . import views 


urlpatterns = [
    path('', views.index, name='index-view'),
    path('blog/', views.blog, name='blog-view'),
    path('post/<slug:slug>/', views.post, name='post-view'),
    path('search/', views.search, name='search-result'),
    path('tinymce/', include('tinymce.urls')),
    path('create/', views.post_create, name='post-create'),
    path('update/<slug:slug>/', views.post_update, name='post-update'),
    path('delete/<slug:slug>/', views.post_delete, name='post-delete'),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)