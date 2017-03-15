"""F1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

urlpatterns = [
    url(r'^', include('predict.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url('^register/', CreateView.as_view(
                template_name='registration/register.html',
                form_class=UserCreationForm,
                success_url='/accounts/login/?next=/'),
                                name = 'register'
    ),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


# django.contrib.auth.urls
# urlpatterns = [
#     url(r'^login/$', views.login, name='login'),
#     url(r'^logout/$', views.logout, name='logout'),
#     url(r'^password_change/$', views.password_change, name='password_change'),
#     url(r'^password_change/done/$', views.password_change_done, name='password_change_done'),
#     url(r'^password_reset/$', views.password_reset, name='password_reset'),
#     url(r'^password_reset/done/$', views.password_reset_done, name='password_reset_done'),
#     url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#         views.password_reset_confirm, name='password_reset_confirm'),
#     url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
# ]
