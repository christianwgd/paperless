from django_filters.rest_framework import FilterSet

from .models import Reminder


class ReminderFilterSet(FilterSet):

    class Meta(object):
        model = Reminder
        fields = {
            "document": ["exact"],
            "date": ["gt", "lt", "gte", "lte", "exact"],
            "note": ["istartswith", "iendswith", "icontains"]
        }
