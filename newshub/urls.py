"""newshub URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views
from django.contrib.sitemaps.views import sitemap
from articles.sitemaps import ArticleSitemap
from django.conf.urls import handler404, handler500
from django.conf.urls import url
sitemaps = {
    'articles': ArticleSitemap,
}
urlpatterns = [

    path('admin_moreme_1806/', admin.site.urls),
    path('', include('articles.urls')),
    url('', include('pwa.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('account/', include('account.urls')),
    path('news_recommendation/', include('news_recommendation.urls')),
    path('ckeditor/upload/', login_required(ckeditor_views.upload),
         name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)),
         name='ckeditor_browse'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),



]
"""
urlpatterns = urlpatterns +
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""

handler404 = 'articles.views.handler404'
handler500 = 'articles.views.handler500'