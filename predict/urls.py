from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /2015/user/username
    url(r'^(?i)user/(?P<user_id>[0-9a-z ]+)/$', views.user_profile, name='user_profile'),
    # ex: /2015/team/12
    url(r'^(?i)(?P<season_id>[0-9]+)/team/(?P<team_id>[0-9]+)/$', views.team_overview, name='team_overview'),
    # ex: /2015/driver/2
    url(r'^(?i)(?P<season_id>[0-9]+)/driver/(?P<driver_id>[0-9]+)/$', views.driver_overview, name='driver_overview'),
    # ex: /2015/China
    url(r'^(?i)(?P<season_id>[0-9]+)/round/(?P<country_id>[a-z ]+)/$', views.race_overview, name='race_overview'),
    # ex: /2015/result/china
    url(r'^(?i)(?P<season_id>[0-9]+)/result/(?P<country_id>[a-z ]+)/$', views.add_result, name='result'),
    # ex: /2015/
    url(r'^(?i)(?P<season_id>[0-9]+)/$', views.season_overview, name='season_overview'),
    url(r'^(?i)(?P<season_id>[0-9]+)/bbcode$', views.season_overview_bbcode, name='season_overview_bbcode'),
    url(r'^(?i)(?P<season_id>[0-9]+)/drivers$', views.driver_championship, name='driver_championship'),
    url(r'^(?i)(?P<season_id>[0-9]+)/constructors$', views.constructor_championship, name='constructor_championship'),
    url(r'^(?i)(?P<season_id>[0-9]+)/calendar$', views.calendar, name='calendar'),
    url(r'^(?i)(?P<season_id>[0-9]+)/entry$', views.entry_list, name='entry_list'),
]
