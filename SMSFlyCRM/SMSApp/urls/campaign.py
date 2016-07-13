from django.conf.urls import url

from ..views import campaigns_list, campaigns_crud


urlpatterns = (
    # Active campaigns list:
    url('^$', campaigns_list.CampaignIndexView.as_view(), name='campaigns-root'),
    # Archive of inactive/sent campaigns:
    url('^archive$', campaigns_list.CampaignArchiveView.as_view(), name='campaigns-archive'),

    # Campaign adding/scheduling form:
    url('^new/one-time$', campaigns_crud.CampaignNewView.as_view(),
        name='add-one-time-campaign'),
    url('^snew/recurring$',
        campaigns_crud.CampaignNewRecurringView.as_view(),
        name='add-recurring-campaign'),
    url('^new/event-driven$', campaigns_crud.CampaignNewEventDrivenView.as_view(),
        name='add-event-driven-campaign'),

    # One-time campaign editing form:
    url('^edit/one-time/(?P<pk>\d+)$', campaigns_crud.CampaignEditView.as_view(),
        name='edit-one-time-campaign'),
    # Recurring campaign editing form:
    url('^edit/recurring/(?P<pk>\d+)$', campaigns_crud.CampaignEditRecurringView.as_view(),
        name='edit-recurring-campaign'),
    # Event-driven campaign editing form:
    url('^edit/event-driven/(?P<pk>\d+)$', campaigns_crud.CampaignEditEventDrivenView.as_view(),
        name='edit-event-driven-campaign'),

    # One-time campaign deleting form:
    url('^one-time/archive/(?P<pk>\d+)$', campaigns_crud.CampaignArchiveView.as_view(),
        name='archive-one-time-campaign'),
    # Recurring campaign deleting form:
    url('^recurring/archive/(?P<pk>\d+)$', campaigns_crud.CampaignArchiveRecurringView.as_view(),
        name='archive-recurring-campaign'),
    # Event-driven campaign deleting form:
    url('^event-driven/archive/(?P<pk>\d+)$', campaigns_crud.CampaignArchiveEventDrivenView.as_view(),
        name='archive-event-driven-campaign'),

    # One-time campaign put-on-hold form:
    url('^one-time/pause/(?P<pk>\d+)$', campaigns_crud.CampaignPauseView.as_view(),
        name='pause-one-time-campaign'),
    # Recurring campaign put-on-hold form:
    url('^recurring/pause/(?P<pk>\d+)$', campaigns_crud.CampaignPauseRecurringView.as_view(),
        name='pause-recurring-campaign'),
    # Event-driven campaign put-on-hold form:
    url('^event-driven/pause/(?P<pk>\d+)$', campaigns_crud.CampaignPauseEventDrivenView.as_view(),
        name='pause-event-driven-campaign'),

    # One-time campaign activate form:
    url('^one-time/activate/(?P<pk>\d+)$', campaigns_crud.CampaignActivateView.as_view(),
        name='activate-one-time-campaign'),
    # Recurring campaign activate form:
    url('^recurring/activate/(?P<pk>\d+)$', campaigns_crud.CampaignActivateRecurringView.as_view(),
        name='activate-recurring-campaign'),
    # Event-driven campaign activate form:
    url('^event-driven/activate/(?P<pk>\d+)$', campaigns_crud.CampaignActivateEventDrivenView.as_view(),
        name='activate-event-driven-campaign'),
)
