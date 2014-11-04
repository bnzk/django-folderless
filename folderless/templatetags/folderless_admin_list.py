# coding: utf-8

from django.template import Library
from django.utils.html import format_html
from django.contrib.admin.templatetags.admin_list import result_list

register = Library()


DISMISS_STRING = u'dismissRelatedLookupPopup'
REPLACE_STRING = u'dismissRelatedFolderlessLookupPopup'


@register.inclusion_tag("admin/change_list_results.html")
def folderless_result_list(cl):
    """
    Displays the headers and data list together
    """
    context = result_list(cl)
    for row_no, row in enumerate(context['results']):
        for cell_no, cell in enumerate(row):
            # TODO: this feels awkward?!
            context['results'][row_no][cell_no] = format_html(cell.replace(DISMISS_STRING, REPLACE_STRING))
    return context
