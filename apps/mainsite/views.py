from __future__ import unicode_literals
from django.shortcuts import render, redirect


def mainsite(request):
    return render(request, 'mainsite/mainsite.html')