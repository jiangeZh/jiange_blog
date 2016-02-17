from django.conf.urls import include, url

from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'',include('blog.urls')),
    url(r'',include('jiange_comments.urls')),
    url(r'',include('jiange_auth.urls')),
	url(r'^markdown/',include('django_markdown.urls')),
]
