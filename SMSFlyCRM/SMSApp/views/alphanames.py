import logging

from django.core.urlresolvers import reverse_lazy

from django.views.generic import ListView

from django.views.generic.edit import CreateView

from ..models.alphaname import Alphaname
from ..forms.alphaname import AlphanameForm

from ..tasks import submitAlphanameInstantly


logger = logging.getLogger(__name__)


class AlphanameIndexView(ListView):
    """Shows all alphaname list available along with registrar and registration date"""
    template_name = 'alphaname/list.html'
    context_object_name = 'alphanames'
    model = Alphaname


class AlphanameRegisterView(CreateView):
    """Sends new alphaname register request"""
    template_name = 'alphaname/new.html'
    form_class = AlphanameForm
    success_url = reverse_lazy('alphanames-root')

    def get_form(self, form_class=None):
        return (form_class or self.form_class)(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        # Add job for sending request to register a new alphanumeric name
        submitAlphanameInstantly.delay(form.cleaned_data['name'])
        return super().form_valid(form)
