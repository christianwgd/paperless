import re

from django.contrib.admin.templatetags.admin_list import (
    result_headers,
    result_hidden_fields,
    results
)
from django.template import Library
from django.utils.safestring import mark_safe

EXTRACT_URL = re.compile(r'href="(.*?)"')

register = Library()


@register.inclusion_tag("admin/documents/document/change_list_results.html")
def result_list(cl):
    """
    Copy/pasted from django.contrib.admin.templatetags.admin_list just so I can
    modify the value passed to `.inclusion_tag()` in the decorator here.  There
    must be a cleaner way... right?
    """
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': headers,
            'num_sorted_fields': num_sorted_fields,
            'results': map(add_doc_edit_url, results(cl))}


def add_doc_edit_url(result):
    """
    Make the document edit URL accessible to the view as a separate item
    """
    title = result[1]
    match = re.search(EXTRACT_URL, title)
    edit_doc_url = match.group(1)
    result.append(edit_doc_url)
    return result


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.simple_tag()
def get_sort_link_params(attr, indicator, **kwargs):
    if indicator == 'sort-desc':
        return attr
    else:
        return '-'+attr
