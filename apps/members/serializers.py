from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.members.models import (
    Snippet, 
    LANGUAGE_CHOICES, 
    STYLE_CHOICES, 
    Profile, 
    Comment, 
    Account,
    Member
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'first_name', 'last_name', 'password', 'snippets')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style')


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('url', 'id', 'user', 'image', 'description', 'date_of_birth', 'phone', 'city', 'country', 'organization')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('image')


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('url', 'id', 'account_name', 'location', 'address', 'account_leader', 'slug', 'allow_members', 'member')

    def create(self, validated_data):
        account = super(AccountSerializer, self).create(validated_data)
        account.save()
        return account


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('url', 'id', 'snippet', 'bodytext')
    
    def create(self, validated_data):
        comment = super(CommentSerializer, self).create(validated_data)
        comment.save()
        return comment


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ('url', 'id', 'user', 'first_name', 'last_name', 'date_of_birth', 'academic_year', 'course', 'regno', 'gender', 'date_of_registration')

    def create(self, validated_data):
        member = super(MemberSerializer, self).create(validated_data)
        member.save()
        return member

'''
class PasswordSerializer(serializers.HyperlinkedModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('url', 'old_password', 'new_password')
'''