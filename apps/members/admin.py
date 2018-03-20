from __future__ import unicode_literals
from .models import Profile, Comment, Account, Member, Snippet
from django.contrib import admin
from django.db import models as django_models
from pagedown.widgets import AdminPagedownWidget


class ProfileAdmin(admin.ModelAdmin):
	
	class Meta:
		model = Profile


class SnippetAdmin(admin.ModelAdmin):
    # Note: this makes pagedown the default editor for ALL text fields
    list_display = ('title', 'code', 'linenos', 'language', 'style', 'highlighted', 'comment_count')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('comment_count',)


class CommentAdmin(admin.ModelAdmin):
    # Note: this makes pagedown the default editor for ALL text fields
    list_display = ('user_name', 'user_email', 'ip_address', 'post_date')


class AccountAdmin(admin.ModelAdmin):
    formfield_overrides = {
        django_models.TextField: {'widget': AdminPagedownWidget},
    }
    prepopulated_fields = {'slug': ('account_name',)}
    list_display = ('account_name', 'location', 'address', 'account_leader', 'created_date', 'allow_members')


class MemberAdmin(admin.ModelAdmin):
    formfield_overrides = {
        django_models.TextField: {'widget': AdminPagedownWidget},
    }
    list_display = (
            'user',
            'first_name',
            'last_name',
            'date_of_birth',
            'regno',
            'academic_year',
            'course',
            'gender',
            'date_of_registration',
            'date_of_expiry'
        )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Snippet, SnippetAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Member, MemberAdmin)