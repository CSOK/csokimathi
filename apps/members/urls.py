from django.conf.urls import url, include
from apps.members import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'members', views.MemberViewSet)
router.register(r'snippets', views.SnippetViewSet)
router.register(r'comments', views.CommentViewSet)


urlpatterns = [
    url(r'^', include(router.urls))
]