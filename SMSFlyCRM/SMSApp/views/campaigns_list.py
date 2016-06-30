import logging

from django.core.urlresolvers import reverse_lazy

from django.views.generic import ListView

from django.utils.translation import ugettext_lazy as _

from ..models.task import Task


logger = logging.getLogger(__name__)


class CampaignBaseView(ListView):
    """Base for tabbed list views"""

    context_object_name = 'tasks'
    model = Task

    active_menu_item = None

    def get_tab_menu(self, active_item=None):
        menu = (
            {
                'url': reverse_lazy('campaigns-root'),
                'title': _('Актуальные'),
            },
            {
                'url': reverse_lazy('campaigns-archive'),
                'title': _('Архив'),
            },
        )

        try:
            menu[active_item or self.active_menu_item]['class'] = 'active'
        except KeyError:
            pass

        return menu

    def get_queryset(self):
        qs = super().get_queryset()
        if self.exclude_state:
            qs = qs.exclude(state=self.exclude_state)
        return qs

    def get_querysets_dict(self):
        try:
            return self.querysets
        except AttributeError:
            pass

        qs = self.get_queryset()

        self.querysets = {'all_{}'.format(self.context_object_name): qs}
        for (i, state) in Task.STATE_LIST:
            self.querysets['{}_{}'.format(state, self.context_object_name)] = qs.filter(state=i).all()

        return self.querysets

    def get_context_data(self):
        context = super().get_context_data()
        context['tab_menu'] = self.get_tab_menu()

        for (qs_name, qs) in self.get_querysets_dict().items():
            context[qs_name] = qs

        return context


class CampaignIndexView(CampaignBaseView):
    """Lists all active campaigns currently in progress (scheduled)"""
    template_name = 'campaign/list-active.html'
    active_menu_item = 0
    exclude_state = 2  # active/paused (not complete)


class CampaignArchiveView(CampaignBaseView):
    """Keeps a history of campaigns, which are inactive"""
    template_name = 'campaign/list-archived.html'
    active_menu_item = 1
    exclude_state = 0  # complete/paused (not active)
