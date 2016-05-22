from django.conf.urls import url

from . import views


urlpatterns = (
    url('', views.IndexView.as_view()),
    url('alphanames', views.AlphanameIndexView.as_view()),
    url('alphanames/new', views.AlphanameRegisterView.as_view()),
    url('sms-campaigns', views.CampaignIndexView.as_view()),
    url('sms-campaigns/new', views.CampaignNewView.as_view()),
    url('sms-campaigns/edit', views.CampaignEditView.as_view()),
    url('sms-campaigns/archive', views.CampaignArchiveView.as_view()),  # Archive of inactive/sent campaigns
)
