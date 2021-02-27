from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import DetailView, FormView, TemplateView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.utils import cache
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _

from paperless.db import GnuPG
from paperless.mixins import SessionOrBasicAuthMixin
from paperless.views import StandardPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet,
    ReadOnlyModelViewSet
)
from sortable_listview import SortableListView

from .filters import CorrespondentFilterSet, DocumentFilterSet, TagFilterSet, \
    DocumentFilter
from .forms import UploadForm, DocumentUpdateForm
from .models import Correspondent, Document, Log, Tag
from .serialisers import (
    CorrespondentSerializer,
    DocumentSerializer,
    LogSerializer,
    TagSerializer
)


class IndexView(TemplateView):
    template_name = "documents/index.html"


class FetchView(SessionOrBasicAuthMixin, DetailView):

    model = Document

    def render_to_response(self, context, **response_kwargs):
        """
        Override the default to return the unencrypted image/PDF as raw data.
        """

        content_types = {
            Document.TYPE_PDF: "application/pdf",
            Document.TYPE_PNG: "image/png",
            Document.TYPE_JPG: "image/jpeg",
            Document.TYPE_GIF: "image/gif",
            Document.TYPE_TIF: "image/tiff",
            Document.TYPE_CSV: "text/csv",
            Document.TYPE_MD:  "text/markdown",
            Document.TYPE_TXT: "text/plain"
        }

        if self.kwargs["kind"] == "thumb":
            response = HttpResponse(
                self._get_raw_data(self.object.thumbnail_file),
                content_type=content_types[Document.TYPE_PNG]
            )
            cache.patch_cache_control(response, max_age=31536000, private=True)
            return response

        response = HttpResponse(
            self._get_raw_data(self.object.source_file),
            content_type=content_types[self.object.file_type]
        )

        DISPOSITION = (
            'inline' if settings.INLINE_DOC or self.kwargs["kind"] == 'preview'
            else 'attachment'
        )

        response["Content-Disposition"] = '{}; filename="{}"'.format(
            DISPOSITION, self.object.file_name)

        return response

    def _get_raw_data(self, file_handle):
        if self.object.storage_type == Document.STORAGE_TYPE_UNENCRYPTED:
            return file_handle
        return GnuPG.decrypted(file_handle)


class PushView(SessionOrBasicAuthMixin, FormView):
    """
    A crude REST-ish API for creating documents.
    """

    form_class = UploadForm

    def form_valid(self, form):
        form.save()
        return HttpResponse("1", status=202)

    def form_invalid(self, form):
        return HttpResponseBadRequest(str(form.errors))


class CorrespondentViewSet(ModelViewSet):
    model = Correspondent
    queryset = Correspondent.objects.all()
    serializer_class = CorrespondentSerializer
    pagination_class = StandardPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = CorrespondentFilterSet
    ordering_fields = ("name", "slug")


class TagViewSet(ModelViewSet):
    model = Tag
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = StandardPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = TagFilterSet
    ordering_fields = ("name", "slug")


class DocumentViewSet(RetrieveModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin,
                      ListModelMixin,
                      GenericViewSet):
    model = Document
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    pagination_class = StandardPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = DocumentFilterSet
    search_fields = ("title", "correspondent__name", "content")
    ordering_fields = (
        "id", "title", "correspondent__name", "created", "modified", "added")


class LogViewSet(ReadOnlyModelViewSet):
    model = Log
    queryset = Log.objects.all().by_group()
    serializer_class = LogSerializer
    pagination_class = StandardPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ("time",)


# Frontend views
class DocumentFilterView(LoginRequiredMixin, FilterView, SortableListView):
    model = Document
    paginate_by = 8
    filterset_class = DocumentFilter
    allowed_sort_fields = {
        'title': {
            'default_direction': '',
            'verbose_name': _('Title')
        },
        'created': {
            'default_direction': '-',
            'verbose_name': _('Created')
        },
        'added': {
            'default_direction': '-',
            'verbose_name': _('Added')
        },
    }
    default_sort_field = 'added'

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        paginate_by = self.request.user.usersettings.paginate_by
        if paginate_by == 0:
            return 1
        return paginate_by


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document


class DocumentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Document
    form_class = DocumentUpdateForm
    success_message = _('Document metadata changed.')

    def get_success_url(self):
        return reverse('documents:detail', kwargs={'pk': self.object.id})
