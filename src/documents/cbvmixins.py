from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.utils.translation import gettext_lazy as _


class RestrictToOwnMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()
        if hasattr(obj, 'user'):
            if obj.user == self.request.user:
                return True
        msg = _('Object not found')
        raise Http404(msg)
