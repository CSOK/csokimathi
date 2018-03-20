from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from config import views as csok_views
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='CSoKimathi API')
app_name = "csokimathi"

admin.autodiscover()

urlpatterns = [
    url(r'^$', csok_views.login_redirect, name='login_redirect'),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', schema_view),
    url(r'^api-auth/', include('apps.members.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
