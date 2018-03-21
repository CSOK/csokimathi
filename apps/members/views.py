from django.shortcuts import render, redirect
from apps.members.models import Profile, Comment, Account, Member, Snippet

from schedule.models.events import Event, Occurrence
from schedule.models.calendars import Calendar, CalendarRelation
from schedule.models.rules import Rule
from django.forms.models import inlineformset_factory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash, authenticate, login as auth_login
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.sites.models import Site
from apps.members.serializers import (
    UserSerializer, 
    SnippetSerializer, 
    UserProfileSerializer, 
    ImageSerializer,
    AccountSerializer,
    CommentSerializer,
    MemberSerializer,
    EventSerializer,
    CalendarSerializer,
    RuleSerializer,
    OccurrenceSerializer,
    CalendarRelationSerializer
)
from django.contrib.syndication.views import Feed
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers, permissions, viewsets, status
from apps.members.permissions import IsOwnerOrReadOnly


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    

class OccurrenceViewSet(viewsets.ModelViewSet):
    queryset = Occurrence.objects.all()
    serializer_class = OccurrenceSerializer

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

class CalendarRelationViewSet(viewsets.ModelViewSet):
    queryset = CalendarRelation.objects.all()
    serializer_class = CalendarRelationSerializer

class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    """
    List all code snippets, or create a new snippet.
    """
    permissions_class = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ImageSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer


class AccountViewSet(viewsets.ModelViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class MemberViewSet(viewsets.ModelViewSet):
    
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

'''
class PasswordViewSet(viewsets.ModelViewSet):
    """
    An endpoint for changing password.
    """
    queryset = User.objects.all()
    serializer_class = PasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''