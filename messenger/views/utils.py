from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.utils import timezone
import datetime


def build_paginator(request, data):
    page = request.GET.get('page', None)
    paginator = Paginator(data, 10)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        last_page = paginator.page_range[-1]
        data = paginator.page(last_page)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    return data


def get_days_to_wait(date):
    date_now = timezone.now()
    date_now = datetime.date(date_now.year, date_now.month, date_now.day)
    date = date
    date = datetime.date(date.year, date.month, date.day)
    days_wait = (date_now - date).days
    return days_wait
