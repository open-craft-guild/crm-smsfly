import logging

from django.views.generic import ListView

from ..models import Follower, Message


logger = logging.getLogger(__name__)


class CampaignMessagesView(ListView):
    """Keeps a history of messages"""
    context_object_name = 'messages'
    model = Message
    paginate_by = 100  # Show 100 messages per page
    template_name = 'sent-messages.html'

    def get_queryset(self):
        qs = super().get_queryset()
        # hack to send user-specific query to external db
        # pre-fetch followers, so they'll be retrieved from cache next time:
        Follower.objects.for_user(self.request.session['crm_user_id']).filter(
            follower_id__in=map(lambda m: m.crm_elector_id, qs)
        )
        qs = qs.prefetch_related('crm_elector')
        return qs
