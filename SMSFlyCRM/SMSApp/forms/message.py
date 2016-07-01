from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models.message import Message


class MessagesSearchForm(forms.ModelForm):
    crm_elector__surname = forms.CharField(label=_("Elector's surname"))
    crm_elector__firstname = forms.CharField(label=_("Elector's first name"))
    crm_elector__patronymic = forms.CharField(label=_("Elector's patronymic"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def crm_elector__name_clean(self):
        pass

    class Meta:
        model = Message
        fields = (
            'phone_number',
            'crm_elector__surname',
            'crm_elector__firstname',
            'crm_elector__patronymic',
        )
        labels = {
            'crm_elector__surname': _("Elector's surname"),
            'crm_elector__firstname': _("Elector's first name"),
            'crm_elector__patronymic': _("Elector's patronymic"),
            'phone_number': _("Elector's phone #"),
        }
