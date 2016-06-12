import logging

from django.views.generic import ListView


logger = logging.getLogger(__name__)


class CampaignStatsView(ListView):
    """Shows stats on campaigns"""
    template_name = 'campaigns-stats.html'
    queryset = []  # TODO: replace fake queryset with an existing model
