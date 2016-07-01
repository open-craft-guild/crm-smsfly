import logging

from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from ..forms.message import MessagesSearchForm

from ..models.crm import Follower
from ..models.message import Message


logger = logging.getLogger(__name__)


class CampaignMessagesView(FormMixin, ListView):
    """Keeps a history of messages"""

    form_class = MessagesSearchForm

    context_object_name = 'messages'
    model = Message
    paginate_by = 100  # Show 100 messages per page
    template_name = 'sent-messages.html'

    def get_queryset(self):
        qs = super().get_queryset()
        fqs = Follower.objects.for_user(self.request.session['crm_user_id'])
        form = self.get_form()
        if form.is_valid():
            elector_name = form.cleaned_data['crm_elector__name']  # TODO: split into three fields
            if elector_name:
                fqs = fqs.filter(name_icontains=elector_name)

        # hack to send user-specific query to external db
        # pre-fetch followers, so they'll be retrieved from cache next time:
        fqs = fqs.filter(
            follower_id__in=map(lambda m: m.crm_elector_id, qs)
        )
        qs = qs.prefetch_related('crm_elector')
        return qs
