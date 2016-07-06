import logging

from django.core.urlresolvers import reverse_lazy

from django.views.generic.edit import CreateView, UpdateView

from ..forms.task import (
    OneTimeTaskForm,
    RecurringTaskForm, EventDrivenTaskForm
)


logger = logging.getLogger(__name__)


class CampaignEditViewMixin:
    """Retrieves model class from form binded"""
    def get_queryset(self):
        return self.get_form_class().Meta.model.objects.all()


class CampaignFormViewMixin:
    """Defines base success_url"""
    success_url = reverse_lazy('campaigns-root')


class RequestAwareFormMixin:
    """Passes request as a first param into form initializer"""

    def get_form(self, form_class=None):
        return (form_class or self.form_class)(self.request, **self.get_form_kwargs())


class OneTimeCampaignMixin:
    form_class = OneTimeTaskForm
    template_name = 'campaign/edit.html'


class RecurringCampaignMixin:
    form_class = RecurringTaskForm
    template_name = 'campaign/edit-recurring.html'


class EventDrivenCampaignMixin:
    form_class = EventDrivenTaskForm
    template_name = 'campaign/edit-event-driven.html'


class CampaignNewView(OneTimeCampaignMixin, RequestAwareFormMixin, CampaignFormViewMixin, CreateView):
    pass


class CampaignNewRecurringView(RecurringCampaignMixin, RequestAwareFormMixin, CampaignFormViewMixin, CreateView):
    pass


class CampaignNewEventDrivenView(EventDrivenCampaignMixin, RequestAwareFormMixin, CampaignFormViewMixin, CreateView):
    pass


class CampaignEditView(OneTimeCampaignMixin, CampaignEditViewMixin,
                       RequestAwareFormMixin, CampaignFormViewMixin,
                       UpdateView):
    pass


class CampaignEditRecurringView(RecurringCampaignMixin, CampaignEditViewMixin,
                                RequestAwareFormMixin, CampaignFormViewMixin,
                                UpdateView):
    pass


class CampaignEditEventDrivenView(EventDrivenCampaignMixin, CampaignEditViewMixin,
                                  RequestAwareFormMixin, CampaignFormViewMixin,
                                  UpdateView):
    pass
