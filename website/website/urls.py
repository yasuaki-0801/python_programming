"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.flatpages import views
from django.contrib.sitemaps.views import sitemap
from .feeds import LatestPostsFeed
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve

from .sitemaps import (
    BlogPostSitemap,
    StaticViewSitemap,
)

sitemaps = {
    'cms': BlogPostSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('cms.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('latest/feed/', LatestPostsFeed()),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('summernote/', include('django_summernote.urls')), 
    path('i18n/', include('django.conf.urls.i18n')),
    #url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    prefix_default_language=False   
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
