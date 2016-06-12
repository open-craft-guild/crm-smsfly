import logging

from django.views.generic import TemplateView


logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    """Shows all menu entries of an app"""
    template_name = 'main.html'
