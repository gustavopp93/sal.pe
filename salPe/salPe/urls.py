from django.conf.urls import url, include
from django.contrib import admin

from apps.events.views import EventListView, EventCreateView, EventUpdateView, EventListJSONView

from apps.organizations.views import (OrganizationSignupFormView,
                                      OrganizationConfirmRedirectView,
                                      OrganizationProfileFormView,
                                      OrganizationLoginFormView,
                                      OrganziationLogoutRedirectView)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^registro/$',
        OrganizationSignupFormView.as_view(),
        name='organization_signup'),

    url(r'^ingreso/$',
        OrganizationLoginFormView.as_view(),
        name='organization_login'),

    url(r'^confirmar/(?P<activation_key>[\w.@+-:]+)/$',
        OrganizationConfirmRedirectView.as_view(),
        name='organization_confirmation'),

    url(r'^organizacion/$',
        OrganizationProfileFormView.as_view(),
        name='organization_profile'),

    url(r'^eventos/$',
        EventListView.as_view(),
        name='events_list'),

    url(r'^eventos/crear/$',
        EventCreateView.as_view(),
        name='events_create'),

    url(r'^eventos/(?P<pk>\d+)/$',
        EventUpdateView.as_view(),
        name='event_update'),

    url(r'^salir/$',
        OrganziationLogoutRedirectView.as_view(),
        name='organization_logout'),

    url(r'^mobile/events/$',
        EventListJSONView.as_view(),
        name='mobile_events'),

]
