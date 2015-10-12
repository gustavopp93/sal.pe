from crispy_forms.helper import FormHelper
from django import forms
from apps.organizations.models.organization import Organization


class OrganizationProfileUpdateModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        super().__init__(*args, **kwargs)

    class Meta:
        model = Organization
        fields = ['name', 'contact_phone', 'contact_name',
                  'contact_last_name', 'contact_email', 'avatar']