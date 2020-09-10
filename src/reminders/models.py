from django.db import models
from django.utils.translation import gettext_lazy as _


class Reminder(models.Model):

    class Meta:
        verbose_name = _('Reminder')
        verbose_name_plural = _('Reminders')

    document = models.ForeignKey(
        "documents.Document", on_delete=models.PROTECT,
        verbose_name = _('Document'),
    )
    date = models.DateTimeField(_('Date'))
    note = models.TextField(_('Note'), blank=True)
