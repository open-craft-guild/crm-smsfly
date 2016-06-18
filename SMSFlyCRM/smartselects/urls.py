from ..SMSApp.urls import url
from .views import filterchain, filterchain_all


urlpatterns = [
    url(r'^all/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/'
        r'(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/'
        r'(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-]+)/$',
        filterchain_all, name='chained_filter_all'),
    url(r'^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/'
        r'(?P<foreign_key_app_name>[\w\-]+)/(?P<foreign_key_model_name>[\w\-]+)/'
        r'(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-]+)/$',
        filterchain, name='chained_filter'),
    url(r'^filter/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<manager>[\w\-]+)/'
        r'(?P<field>[\w\-]+)/(?P<foreign_key_app_name>[\w\-]+)/'
        r'(?P<foreign_key_model_name>[\w\-]+)/'
        r'(?P<foreign_key_field_name>[\w\-]+)/(?P<value>[\w\-]+)/$',
        filterchain, name='chained_filter'),
]
