import logging

from django.views.generic import ListView

from ..models import Message


logger = logging.getLogger(__name__)


class CampaignMessagesView(ListView):
    """Keeps a history of messages"""
    model = Message
    paginate_by = 100  # Show 100 messages per page
    template_name = 'sent-messages.html'
