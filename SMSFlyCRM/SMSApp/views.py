import json
from datetime import date

from django.core.urlresolvers import reverse_lazy

from django.http import JsonResponse

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView

from .models import Alphaname, Project
from .forms import AlphanameForm, TaskForm


class IndexView(TemplateView):
    """Shows all menu entries of an app"""
    template_name = 'main.html'


class AlphanameIndexView(ListView):
    """Shows all alphaname list available along with registrar and registration date"""
    template_name = 'alphanames-list.html'
    model = Alphaname


class AlphanameRegisterView(FormView):
    """Sends new alphaname register request"""
    template_name = 'alphaname-new.html'
    form_class = AlphanameForm
    success_url = reverse_lazy('alphanames-root')

    def form_valid(self, form):
        form.status = 2
        form.registration_date = date.today()
        form.created_by_crm_user_id = self.request.session['crm_user_id']
        form.save()
        # Add job for sending request to register a new alphanumeric name
        return super().form_valid(form)


class CampaignIndexView(ListView):
    """Lists all active campaigns currently in progress (scheduled)"""
    template_name = 'campaigns-list.html'
    queryset = []  # TODO: replace fake queryset with an existing model


class CampaignNewView(FormView):
    """Helps schedule a new campaign or send new one instantly"""
    template_name = 'campaign-edit.html'
    form_class = TaskForm
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['range30'] = range(1, 31)
        context['weekdays'] = (
            (1, 'пн'),
            (2, 'вт'),
            (3, 'ср'),
            (4, 'чт'),
            (5, 'пт'),
            (6, 'сб'),
            (7, 'нд'),
        )
        return context

    def form_valid(self, form):
        # Save new campaign and notify everyone about it, add job into queue if needed
        return super().form_valid(form)


class CampaignEditView(FormView):
    """Makes modifications on an active campaign"""
    template_name = 'campaign-edit.html'
    form_class = TaskForm
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


@require_POST
@csrf_exempt
def webhook_crm_event(request, crm_event, crm_user_id):
    crm_user_id = int(crm_user_id)
    json_res = {}
    try:
        json_req = json.loads(request.body.decode())
        'sms_view_projects.project_id'
        'sms_view_follower_status.follower_status_id'
        'sms_view_project_contacts.contact_id'
        'sms_view_candidates.candidate_id'
    except json.decoder.JSONDecodeError:
        json_res = {
            'result': 'Client Error',
            'status': 400,
            'message': 'The trigger processing has failed',
        }
    else:
        json_res = {
            'result': 'OK',
            'status': 200,
            'message': 'The trigger processing has been queued',
            'data': Project.objects.for_user(crm_user_id).filter(project_id=json_req['project_id']).all()[0].
            project_name,
        }
    finally:
        return JsonResponse(json_res)


@require_POST
@csrf_exempt
def webhook_smsfly_status(request):
    return 'SMSFly webhook here'
