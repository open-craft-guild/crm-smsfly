import logging

from django.views.generic import ListView


logger = logging.getLogger(__name__)


class CampaignMessagesView(ListView):
    """Keeps a history of messages"""
    template_name = 'sent-messages.html'
    queryset = []  # TODO: replace fake queryset with an existing model
