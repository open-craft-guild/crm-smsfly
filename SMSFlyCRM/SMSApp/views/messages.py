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
        phone_number = None

        flwr_filters = {}
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            for field_name in ('lastname', 'firstname', 'middlename'):
                fld = form.cleaned_data['crm_elector__{}'.format(field_name)]
                if fld:
                    flwr_filters['{}__icontains'.format(field_name)] = fld

        if phone_number:
            logger.debug('Applying phone number filter')
            qs = qs.filter(phone_number=phone_number)

        if flwr_filters:
            logger.debug('Pre-fetching followers with filters applied')
            fqs = fqs.filter(**flwr_filters)
            qs = qs.filter(
                crm_elector_id__in=map(lambda f: f.follower_id, fqs)
            )
        else:
            logger.debug('Pre-fetching followers for non-filtered view')
            # hack for sending user-specific query to external db
            # pre-fetch followers, so they'll be retrieved from cache next time:
            fqs = fqs.filter(
                follower_id__in=map(lambda m: m.crm_elector_id, qs)
            )

        qs = qs.prefetch_related('crm_elector')
        return qs

    def get_form(self):
        return self.form_class(self.request.GET)
