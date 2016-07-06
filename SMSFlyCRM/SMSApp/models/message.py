from django.db import models

from django.utils.translation import ugettext_lazy as _

from ..utils import calculate_price_for


class Message(models.Model):
    STATUS_LIST = (
        (0, 'PENDING'),
        (1, 'SENT'),
        (2, 'DELIVERED'),
        (3, 'EXPIRED'),
        (4, 'UNDELIV'),
        (5, 'STOPED'),
        (6, 'ERROR'),
        (7, 'USERSTOPED'),
        (8, 'ALFANAMELIMITED'),
        (9, 'STOPFLAG'),
        (10, 'NEW'),
        (11, 'ACCEPTED'),
    )

    crm_elector = models.ForeignKey('Follower', to_field='follower_id',
                                    on_delete=models.DO_NOTHING, related_name='messages')
    phone_number = models.CharField(max_length=12)
    message_text = models.CharField(max_length=402)
    datetime_scheduled = models.DateTimeField()
    datetime_sent = models.DateTimeField(null=True)
    status = models.IntegerField(choices=STATUS_LIST)
    campaign = models.ForeignKey('Campaign')

    @property
    def msg_cost(self):
        return calculate_price_for(1, len(self.message_text))

    @property
    def status_text(self):
        return self.get_status_display()

    @status_text.setter
    def status_text(self, status_text):
        self.status = self.status_id_by_text(status_text)

    def status_id_by_text(self, status_text):
        for i, t in self.STATUS_LIST:
            if t == status_text:
                return i

        raise KeyError

    def __str__(self):
        return _('{} to {}  ({})').format(self.message_text, self.phone_number, self.status_text)

    class Meta:
        db_route = 'internal_app'
