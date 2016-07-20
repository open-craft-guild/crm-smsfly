from django.db import models

from django.utils.translation import ugettext_lazy as _


class Campaign(models.Model):
    task = models.ForeignKey('Task', related_name='campaigns')
    code = models.CharField(max_length=20)
    datetime_sent = models.DateTimeField()
    state = models.TextField(default=None, null=True)
    smsfly_campaign_id = models.IntegerField(default=None, null=True)  # campaign id given by smsfly
    cost = models.IntegerField(default=None, null=True)

    def __str__(self):
        return '{}, {}'.format(self.task.title or _('Noname'), self.datetime_sent)

    class Meta:
        db_route = 'internal_app'
        get_latest_by = 'datetime_sent'
