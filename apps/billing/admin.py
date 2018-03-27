from __future__ import unicode_literals
from apps.billing.models import Transaction, Membership, UserMerchantID
from django.contrib import admin

admin.site.register(Membership)
admin.site.register(Transaction)
admin.site.register(UserMerchantID)