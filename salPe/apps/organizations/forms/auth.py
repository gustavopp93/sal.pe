from crispy_forms.helper import FormHelper

from django import forms
from django.contrib.auth import get_user_model


class OrganizationSignupForm(forms.Form):
    MSG_ERR_INVALID_DOMAIN = 'El dominio de su email es inválido'
    MSG_ERR_EMAIL_ALREADY_REGISTERED = 'El email indicado ya ha sido registrado'

    name = forms.CharField(max_length=255, label='Nombre de organización')
    email = forms.EmailField(max_length=75, label='Email de contacto')
    contact_name = forms.CharField(max_length=50, label='Nombre de contacto')
    contact_last_name = forms.CharField(max_length=75, label='Apellido de contacto')
    contact_phone = forms.CharField(max_length=30, label='Telefono de contacto')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super().__init__(*args, **kwargs)


    def clean_email(self):
        email = self.cleaned_data['email']
        if 'yopmail' in email and 'mailinator' in email:
            raise forms.ValidationError(self.MSG_ERR_INVALID_DOMAIN)
        user_model = get_user_model()
        try:
            user_model.objects.get(email=email)
            raise forms.ValidationError(self.MSG_ERR_EMAIL_ALREADY_REGISTERED)
        except user_model.DoesNotExist:
            pass
        return email


class OrganizationLoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super().__init__(*args, **kwargs)

    email = forms.EmailField(max_length=75)
    password = forms.CharField(widget=forms.PasswordInput, max_length=75)
