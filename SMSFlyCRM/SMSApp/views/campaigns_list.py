import logging

from django.core.urlresolvers import reverse_lazy

from django.db.models import Q

from django.views.generic import ListView

from django.utils.translation import ugettext_lazy as _

from ..models import Task


logger = logging.getLogger(__name__)


class CampaignBaseView(ListView):
    """Base for tabbed list views"""

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

    def get_context_data(self):
        context = super().get_context_data()
        context['tab_menu'] = self.get_tab_menu()
        return context


class CampaignIndexView(CampaignBaseView):
    """Lists all active campaigns currently in progress (scheduled)"""
    template_name = 'campaigns-list.html'
    active_menu_item = 0
    context_object_name = 'tasks'
    queryset = Task.objects.filter(state=0)


class CampaignArchiveView(CampaignBaseView):
    """Keeps a history of campaigns, which are inactive"""
    template_name = 'campaigns-list.html'
    active_menu_item = 1
    context_object_name = 'tasks'
    queryset = Task.objects.filter(Q(state=2) | Q(state=1))
