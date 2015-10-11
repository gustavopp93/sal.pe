from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.core.urlresolvers import reverse
from django.core import signing
from django.http import Http404, HttpResponseRedirect
from django.views.generic import FormView, RedirectView, UpdateView

from apps.core.extra.constants import ORGANIZATION_ID_KEY
from apps.core.extra.email import send_email_via_mandrill
from apps.core.extra.mixin import LoginRequiredMixin, OrganizationRequiredMixin

from apps.organizations.forms.auth import OrganizationSignupForm, OrganizationLoginForm
from apps.organizations.forms.profile import OrganizationProfileUpdateModelForm
from apps.organizations.models.organization import Organization, OrganizationUser


class OrganizationSignupFormView(FormView):
    form_class = OrganizationSignupForm
    template_name = 'organizations/singup.html'

    MSG_SUCCESS = 'Se ha registrado la organización con éxito. Se le enviará un correo de un correo de confirmación.'

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        user_model = get_user_model()
        email = cleaned_data['email']
        first_name = cleaned_data['contact_name']
        last_name = cleaned_data['contact_last_name']
        user = user_model.objects.create_user(username=email, email=email,
                                              first_name=first_name, last_name=last_name)
        user.is_active = False
        user.save()
        organization = Organization(contact_email=email,
                                    name=cleaned_data['name'],
                                    contact_name=first_name,
                                    contact_phone=cleaned_data['contact_phone'],
                                    contact_last_name=last_name)
        organization.save()
        OrganizationUser.objects.create(organization=organization, user=user)
        signer = signing.TimestampSigner(salt=settings.REGISTRATION_SALT)
        activation_key = signer.sign(
            str(getattr(user, user.USERNAME_FIELD))
        )
        url = settings.SITE_URL + reverse('organization_confirmation', kwargs={'activation_key': activation_key})
        content = [
            {'name': 'name', 'content': user.get_full_name()},
            {'name': 'url', 'content': url}
        ]
        send_email_via_mandrill(email, user.get_full_name(), 'Verificación  de email',
                                'confirmation', content)
        messages.success(self.request, self.MSG_SUCCESS)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('organization_signup')


class OrganizationLoginFormView(FormView):
    form_class = OrganizationLoginForm
    template_name = 'organizations/login.html'

    MSG_ERR_NO_USER = 'El usuario no existe'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        auth_user = authenticate(username=email, password=password)
        if auth_user is not None and auth_user.is_active:
            try:
                organization_user = OrganizationUser.objects.get(user=auth_user)
                login(self.request, auth_user)
                self.request.session[ORGANIZATION_ID_KEY] = organization_user.organization_id
                return HttpResponseRedirect(reverse('organization_profile'))
            except OrganizationUser.DoesNotExist:
                pass
        messages.warning(self.request, self.MSG_ERR_NO_USER)
        return self.form_invalid(form)


class OrganizationConfirmRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        activation_key = kwargs.get('activation_key')
        signer = signing.TimestampSigner(salt=settings.REGISTRATION_SALT)
        try:
            username = signer.unsign(
                activation_key,
                max_age=settings.ACCOUNT_ACTIVATION_DAYS * 86400
            )
            if username is not None:
                user_model = get_user_model()
                try:
                    kwargs = {user_model.USERNAME_FIELD: username,
                              'is_active': False}
                    user = user_model.objects.get(**kwargs)
                    try:
                        organization_user = OrganizationUser.objects.get(user=user)

                        password = user_model.objects.make_random_password()

                        user.set_password(password)
                        user.is_active = True
                        user.save()

                        auth_user = authenticate(username=user.email, password=password)
                        login(self.request, auth_user)
                        self.request.session[ORGANIZATION_ID_KEY] = organization_user.organization_id
                        content = [
                            {'name': 'name', 'content': user.get_full_name()},
                            {'name': 'password', 'content': password}
                        ]
                        send_email_via_mandrill(user.email, user.get_full_name(), 'Contraseña generada',
                                                'password', content)
                        return reverse('organization_profile')
                    except OrganizationUser.DoesNotExist:
                        pass
                except user_model.DoesNotExist:
                    pass
        except signing.BadSignature:
            pass
        raise Http404


class OrganizationProfileFormView(LoginRequiredMixin,
                                  OrganizationRequiredMixin,
                                  UpdateView):
    form_class = OrganizationProfileUpdateModelForm
    model = Organization
    template_name = 'organizations/profile.html'

    def get_object(self, queryset=None):
        organization_id = self.request.session.get(ORGANIZATION_ID_KEY, None)
        if organization_id is not None:
            try:
                return Organization.objects.get(id=organization_id)
            except Organization.DoesNotExist:
                pass
        raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization_name'] = self.object.name
        return context

    def get_success_url(self):
        return reverse('organization_profile')
