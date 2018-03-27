from __future__ import unicode_literals
import datetime
import random
from django.contrib.auth.signals import user_logged_in
from apps.billing.signals import membership_dates_update
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save


class Membership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now, verbose_name='Start Date')
    end_date = models.DateTimeField(default=timezone.now, verbose_name='End Date')

    def __str__(self):
        return self.user.get_full_name()

    def update_status(self):
        if self.end_date >= timezone.now():
            self.user.is_member = True
            self.user.save()
        
        elif self.end_date < timezone.now():
            self.user.is_member = False
            self.user.save()
        
        else:
            pass

def update_membership_status(sender, instance, created, **kwargs):
    if not created:
        instance.update_status()

post_save.connect(update_membership_status, sender=Membership)

    
def update_membership_dates(sender, new_start_date, **kwargs):
    membership = sender
    current_end_date = membership.end_date

    if current_end_date >= new_start_date:
        membership.end_date = current_end_date + datetime.timedelta(days=30, hours=10)
        membership.save()

    else:
        membership.start_date = new_start_date
        membership.end_date = new_start_date + datetime.timedelta(days=30, hours=10)
        membership.save()

membership_dates_update.connect(update_membership_dates)


class TransactionManager(models.Manager):
    def create_new(self, user, transaction_id, amount, t_type, success=None, transaction_status=None, last_four=None):
        if not user:
            raise ValueError('Must be a user')
        
        if not transaction_id:
            raise ValueError('Must complete payments for you to be added')

        new_account_id = "%s%s%s" % (transaction_id[:2], random.randint(1, 100000000), transaction_id[2:])
        new_trans = self.model(
            user = user,
            transaction_id = transaction_id,
            account_id = new_account_id,
            amount = amount,
            t_type = t_type
        )

        if success is not None:
            new_trans.success = success
            new_trans.transaction_status = transaction_status

        if last_four is not None:
            new_trans.last_four = last_four

        new_trans.save(using=self._db)
        return new_trans

    def all_for_user(self, user):
        return super(TransactionManager, self).filter(user=user)

    def get_recent_for_user(self, user, num):
        return super(TransactionManager, self).filter(user=user)[:num]

    
class Transaction(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    transaction_id = models.CharField(max_length=100) # mpesa code
    account_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    success = models.BooleanField(default=True)
    transaction_status = models.CharField(max_length=220, null=True, blank=True)
    t_type = models.CharField(max_length=50)
    last_four = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    objects = TransactionManager()

    def __unicode__(self):
        return self.account_id

    class Meta:
        ordering = ['-timestamp']


class UserMerchantID(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    member_id = models.CharField(max_length=100)
    sub_id = models.CharField(max_length=100, null=True, blank=True)
    merchant_name = models.CharField(max_length=100, default='M-pesa')

    def __unicode__(self):
        return self.member_id