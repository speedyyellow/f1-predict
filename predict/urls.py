from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /predict/2015/team/12
    url(r'^(?i)(?P<season_id>[0-9]+)/team/(?P<team_id>[0-9]+)/$', views.team_overview, name='team_overview'),
    # ex: /predict/2015/driver/2
    url(r'^(?i)(?P<season_id>[0-9]+)/driver/(?P<driver_id>[0-9]+)/$', views.driver_overview, name='driver_overview'),
    # ex: /predict/2015/China
    url(r'^(?i)(?P<season_id>[0-9]+)/(?P<country_id>[a-z ]+)/$', views.race_overview, name='race_overview'),
    # ex: /predict/2015/
    url(r'^(?i)(?P<season_id>[0-9]+)/$', views.season_overview, name='season_overview'),
]
