from django.conf import settings
from django.conf.urls import include, static
from django.contrib import admin
from django.urls import reverse_lazy, path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from django.utils.translation import gettext_lazy as _
from rest_framework.routers import DefaultRouter

from paperless.views import FaviconView
from documents.views import (
    CorrespondentViewSet,
    DocumentViewSet,
    FetchView,
    LogViewSet,
    PushView,
    TagViewSet
)
from reminders.views import ReminderViewSet


router = DefaultRouter()
router.register(r"correspondents", CorrespondentViewSet)
router.register(r"documents", DocumentViewSet)
router.register(r"logs", LogViewSet)
router.register(r"reminders", ReminderViewSet)
router.register(r"tags", TagViewSet)

urlpatterns = [

    # API
    path(
        "api/auth/",
        include(
            ('rest_framework.urls', 'rest_framework'),
            namespace="rest_framework")
    ),
    path("api/", include((router.urls, 'drf'), namespace="drf")),
    path('documents/', include('documents.urls')),

    # File downloads
    re_path(
        r"^fetch/(?P<kind>doc|thumb|preview)/(?P<pk>\d+)$",
        FetchView.as_view(),
        name="fetch"
    ),

    # File uploads
    re_path(r"^push$", csrf_exempt(PushView.as_view()), name="push"),

    # Favicon
    re_path(r"^favicon.ico$", FaviconView.as_view(), name="favicon"),

    # The Django admin
    path("admin/", admin.site.urls),

    # Redirect / to /admin
    # re_path(r"^$", RedirectView.as_view(
    #     permanent=True, url=reverse_lazy("admin:index"))),
    re_path(r"^$", RedirectView.as_view(
        permanent=True, url=reverse_lazy("documents:list"))),

] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Text in each page's <h1> (and above login form).
admin.site.site_header = 'Paperless'
# Text at the end of each page's <title>.
admin.site.site_title = 'Paperless'
# Text at the top of the admin index page.
admin.site.index_title = _('Paperless administration')
