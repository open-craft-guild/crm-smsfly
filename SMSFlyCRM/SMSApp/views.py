from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView

from .models import Alphaname


class IndexView(TemplateView):
    """Shows all menu entries of an app"""
    template_name = 'main.html'


class AlphanameIndexView(ListView):
    """Shows all alphaname list available along with registrar and registration date"""
    template_name = 'alphanames-list.html'
    model = Alphaname

    def get_queryset(self):
        return self.model.objects.for_user(crm_user_id=self.request.session['crm_user_id']).all()


class AlphanameRegisterView(FormView):
    """Sends new alphaname register request"""
    template_name = 'alphaname-new.html'
    form_class = dict  # TODO: replace fake form with an existing one
    success_url = ''

    def form_valid(self, form):
        # Add job for sending request to register a new alphanumeric name
        return super().form_valid(form)


class CampaignIndexView(ListView):
    """Lists all active campaigns currently in progress (scheduled)"""
    template_name = 'campaigns-list.html'
    queryset = []  # TODO: replace fake queryset with an existing model


class CampaignNewView(FormView):
    """Helps schedule a new campaign or send new one instantly"""
    template_name = 'campaign-edit.html'
    form_class = dict  # TODO: replace fake form with an existing one
    success_url = ''

    def form_valid(self, form):
        # Save new campaign and notify everyone about it, add job into queue if needed
        return super().form_valid(form)


class CampaignEditView(FormView):
    """Makes modifications on an active campaign"""
    template_name = 'campaign-edit.html'
    form_class = dict  # TODO: replace fake form with an existing one
    success_url = ''

    def form_valid(self, form):
        # Change campaign settings and notify everyone about its change, which involves changing DB and rescheduling job
        return super().form_valid(form)


class CampaignArchiveView(ListView):
    """Keeps a history of campaigns, which are inactive"""
    template_name = 'campaigns-list.html'
    queryset = []  # TODO: replace fake queryset with an existing model


class CampaignMessagesView(ListView):
    """Keeps a history of messages"""
    template_name = 'sent-messages.html'
    queryset = []  # TODO: replace fake queryset with an existing model


class CampaignStatsView(ListView):
    """Shows stats on campaigns"""
    template_name = 'campaigns-stats.html'
    queryset = []  # TODO: replace fake queryset with an existing model
