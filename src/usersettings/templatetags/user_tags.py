# -*- coding:utf-8 -*-
from datetime import timedelta, date

from django import template
from django.utils.html import mark_safe

from usersettings.models import UserSettings
from django.utils.formats import date_format


register = template.Library()


@register.simple_tag
def recent_date_param(user):
    """
    get user specific recent date parameter
    """

    try:
        if user.is_authenticated:
            user_settings = UserSettings.objects.get(user=user)
            if user_settings.recent is not None and user_settings.recent > 0:
                td = date.today() - timedelta(days=user_settings.recent)
                recent_param = '?timestamp_after={date}'.format(
                    date = date_format(td, "SHORT_DATE_FORMAT")
                )
                return mark_safe(recent_param)
    except UserSettings.DoesNotExist:
        pass
    return ''
