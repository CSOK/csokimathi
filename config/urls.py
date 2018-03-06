"""csokimathi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import re_path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from config import views as csok_views
from apps.mainsite import views as mainsite_views
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='CSoKimathi API')
app_name = "csokimathi"

admin.autodiscover()

urlpatterns = [
    re_path(r'^$', csok_views.login_redirect, name='login_redirect'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^$', schema_view),
    re_path(r'^index/', include('apps.members.urls', namespace='index')),
    re_path(r'^mainsite/$', mainsite_views.mainsite, name='mainsite'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
