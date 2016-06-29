import logging

from django.core.urlresolvers import reverse_lazy

from django.views.generic.edit import FormView, CreateView

from ..forms.task import (
    OneTimeTaskForm,
    RecurringTaskForm, EventDrivenTaskForm
)


logger = logging.getLogger(__name__)


class CampaignNewView(CreateView):
    """Helps schedule a new campaign or send new one instantly"""
    template_name = 'campaign-edit.html'
    form_class = OneTimeTaskForm
    success_url = reverse_lazy('campaigns-root')

    def get_form(self, form_class=None):
        return (form_class or self.form_class)(self.request, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['range30'] = range(1, 31)
        return context


class CampaignNewRecurringView(CampaignNewView):
    form_class = RecurringTaskForm
    template_name = 'campaign-recurring-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class CampaignNewEventDrivenView(CampaignNewView):
    form_class = EventDrivenTaskForm
    template_name = 'campaign-event-driven-edit.html'


class CampaignEditView(FormView):
    """Makes modifications on an active campaign"""
    template_name = 'campaign-edit.html'
    form_class = OneTimeTaskForm
    success_url = ''

    def form_valid(self, form):
        # Change campaign settings and notify everyone about its change, which involves changing DB and rescheduling job
        return super().form_valid(form)
