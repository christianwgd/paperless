from django.conf import settings
from django.conf.urls import include, static
from django.contrib import admin
from django.urls import reverse_lazy, path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import views as auth_views
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

    # The Django admin
    path("admin/", admin.site.urls),

    path('login/', auth_views.LoginView.as_view(
      template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
      template_name='accounts/logged_out.html'),
       name='logout'),
    path('password_change/',
       auth_views.PasswordChangeView.as_view(
           template_name='accounts/password_change_form.html'),
       name='password_change'),
    path('password_change/done/',
       auth_views.PasswordChangeDoneView.as_view(
           template_name='accounts/password_change_done.html'),
       name='password_change_done'),

    # Redirect / to /admin
    # re_path(r"^$", RedirectView.as_view(
    #     permanent=True, url=reverse_lazy("admin:index"))),
    re_path(r"^$", RedirectView.as_view(
        permanent=True, url=reverse_lazy("documents:list"))),

    path('settings/', include('usersettings.urls')),

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

] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Text in each page's <h1> (and above login form).
admin.site.site_header = 'Paperless'
# Text at the end of each page's <title>.
admin.site.site_title = 'Paperless'
# Text at the top of the admin index page.
admin.site.index_title = _('Paperless administration')
