# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _


class UserSettings(models.Model):

    class Meta:
        verbose_name = _('user settings')
        verbose_name_plural = _('user settings')

    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paginate_by = models.PositiveSmallIntegerField(
        default=10, verbose_name=_('Number of items per page'),
        help_text=_('0 means no pagination'),
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        user_settings = UserSettings.objects.get(user=instance)
    except UserSettings.DoesNotExist:
        UserSettings.objects.create(
            user = instance,
        )
