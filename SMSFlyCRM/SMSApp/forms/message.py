from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models.message import Message


class MessagesSearchForm(forms.ModelForm):
    phone_number = forms.CharField(required=False, label=_("Elector's phone #"), max_length=12)
    crm_elector__lastname = forms.CharField(required=False, label=_("Elector's surname"))
    crm_elector__firstname = forms.CharField(required=False, label=_("Elector's first name"))
    crm_elector__middlename = forms.CharField(required=False, label=_("Elector's patronymic"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Message
        fields = (
            'phone_number',
            'crm_elector__lastname',  # surname
            'crm_elector__firstname',
            'crm_elector__middlename',  # patronymic
        )
