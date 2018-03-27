from django.dispatch import Signal

membership_dates_update = Signal(providing_args=['new_start_date'])