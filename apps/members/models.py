from __future__ import unicode_literals
import uuid
import datetime
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments import highlight
from pygments.styles import get_all_styles
from django.db.models.signals import post_save
from pygments.formatters.html import HtmlFormatter
from django.urls import reverse
from apps.members.signals import save_comment
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female')
]

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pic', blank=True, null=True)
    tags = GenericRelation(ContentType)
    description = models.TextField(max_length=500, default='', null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.IntegerField(default=0, null=True)
    city = models.CharField(max_length=50, default='', null=True)
    country = models.CharField(max_length=100, default='', blank=True, null=True)
    organization = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='Published')


class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='member_user')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    tags = GenericRelation(ContentType)
    date_of_birth = models.DateField(null=True, blank=True)
    academic_year = models.IntegerField(null=True, blank=True)
    course = models.CharField(max_length=100)
    regno = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=1, default='Gender', choices=GENDER_CHOICES)
    date_of_registration = models.DateField(auto_now_add=True)
    date_of_expiry = models.DateField(blank=True, null=True)
    

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')

@python_2_unicode_compatible
class Account(models.Model):
    account_name = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    account_leader = models.ForeignKey(Member, related_name='account_leader', on_delete=models.CASCADE)
    tags = GenericRelation(ContentType)
    slug = models.SlugField()
    created_date = models.DateField(auto_now_add=True)
    allow_members = models.BooleanField(default=True)
    member = models.ManyToManyField(Member)

    def __str__(self):
        return self.account_name

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def get_absolute_url(self):
        return reverse('index:account_detail', kwargs = {'slug': self.slug}) 


class Snippet(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    slug = models.SlugField()
    tags = GenericRelation(ContentType)
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='Python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='Friendly', max_length=100)
    allow_comments = models.BooleanField(default=True, verbose_name=_("allow comments"))
    comment_count = models.IntegerField(blank=True, default=0, verbose_name=_('comment count'))
    highlighted = models.TextField()

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)


class Comment(models.Model):
    snippet = models.ForeignKey(Snippet, related_name='comments',null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("snippet"))
    bodytext = models.TextField(verbose_name=_("message"))
    tags = GenericRelation(ContentType)
    post_date = models.DateTimeField(auto_now_add=True, verbose_name=_("post date"))
    ip_address = models.GenericIPAddressField(default='0.0.0.0', verbose_name=_("ip address"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_("user"), 
        on_delete=models.CASCADE, related_name='comment_user')
    user_name = models.CharField(max_length=50, default='anonymous', verbose_name=_("user name"))
    user_email = models.EmailField(blank=True, verbose_name=_("user email"))

    def __str__(self):
        return self.bodytext

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['post_date']


post_save.connect(save_comment, sender=Comment)
