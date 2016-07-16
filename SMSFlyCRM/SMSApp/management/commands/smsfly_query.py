from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from smsfly import SMSFlyAPI


class Command(BaseCommand):
    help = 'Runs SMS-Fly API queries for checking balance and sending SMS via CLI'
    VALID_METHODS = {
        'balance': 'getbalance',
        'send-sms': 'send_sms_to_recipient',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.smsfly_api = SMSFlyAPI(account_id=settings.SMS_FLY['login'],
                                    account_pass=settings.SMS_FLY['password'])

    def add_arguments(self, parser):
        parser.add_argument('--api-method', type=str, default=next(iter(self.VALID_METHODS.keys())))
        parser.add_argument('--sms-text', type=str, required=False)
        parser.add_argument('--sms-recipient', type=str)

    def handle(self, *args, **options):
        api_method_name = self.VALID_METHODS[options['api_method']]
        now = datetime.now()
        api_kwargs = {}

        if api_method_name == 'send_sms_to_recipient':
            api_kwargs.update({
                'start_time': 'AUTO',
                'end_time': 'AUTO',
                'lifetime': 24,
                'rate': 120,
                'desc': _('Sending SMS from django command by @webknjaz'),
                'source': 'InfoCentr',
                'body': options['sms_text'],
                'recipient': options['sms_recipient'],
            })

        api_result = getattr(self.smsfly_api, api_method_name)(**api_kwargs)

        if api_method_name == 'send_sms_to_recipient':
            self.stdout.write(self.style.SUCCESS(
                'SMS has been sent at {} via SMS-Fly gateway. API result is: {}'.format(now, api_result)))
        elif api_method_name == 'getbalance':
            self.stdout.write(self.style.SUCCESS('Account balance is: {}'.format(api_result)))
