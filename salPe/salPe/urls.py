"""salPe URL Configuration

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
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from apps.organizations.views import (OrganizationSignupFormView, OrganizationConfirmRedirectView,
                                      OrganizationProfileFormView, OrganizationLoginFormView)

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

]
