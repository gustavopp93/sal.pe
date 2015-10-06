from django.http import HttpResponse, Http404
from apps.core.extra.constants import ORGANIZATION_ID_KEY
from apps.organizations.models import Organization, OrganizationUser


class LoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404


class OrganizationRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        try:
            organization_id = self.request.session.get(ORGANIZATION_ID_KEY, None)
            if organization_id is not None:
                organization = Organization.objects.get(id=organization_id)
                try:
                    OrganizationUser.objects.get(organization=organization, user=self.request.user)
                    return super().dispatch(request, *args, **kwargs)
                except OrganizationUser.DoesNotExist:
                    pass
        except Organization.DoesNotExist:
            pass
        raise Http404