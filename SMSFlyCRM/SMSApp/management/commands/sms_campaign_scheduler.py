from datetime import datetime
from django.core.management.base import BaseCommand

from SMSFlyCRM.SMSApp.tasks import scheduleCampaignTasksFor


class Command(BaseCommand):
    help = 'Schedules campaign sending for specified interval'

    def add_arguments(self, parser):
        parser.add_argument('min_interval', type=int)

    def handle(self, *args, **options):
        min_interval = options['min_interval']
        scheduleCampaignTasksFor.delay(min_interval)
        self.stdout.write(self.style.SUCCESS(
            'Campaign scheduler has been executed at {}'.format(datetime.now())))
