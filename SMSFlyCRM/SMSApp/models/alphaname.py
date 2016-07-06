from django.db import models

from django.utils.translation import ugettext_lazy as _


class Alphaname(models.Model):
    STATUS_LIST = (
        (0, 'ACTIVE'),
        (1, 'BLOCKED'),
        (2, 'MODERATE'),
        (3, 'LIMITED'),
    )

    name = models.CharField(max_length=11)
    status = models.IntegerField(choices=STATUS_LIST, null=True)
    registration_date = models.DateField()
    created_by_crm_user_id = models.IntegerField()

    def change_status_to(self, status_text, commit=True):
        self.text_status = status_text
        return self.save(commit=commit)

    def __str__(self):
        return _('{} ({}). Registered on {} by {}').format(
            self.name, self.status, self.registration_date, self.created_by_crm_user_id)

    @property
    def text_status(self):
        return self.get_status_display()

    @text_status.setter
    def text_status(self, status_text):
        self.status = self.status_id_by_text(status_text)

    def status_id_by_text(self, status_text):
        for i, t in self.STATUS_LIST:
            if t == status_text:
                return i

        raise KeyError

    class Meta:
        db_route = 'internal_app'
