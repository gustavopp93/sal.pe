from crispy_forms.helper import FormHelper
from django import forms
from apps.events.models import Event


class EventModelForm(forms.ModelForm):



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False

    class Meta:
        model = Event
        fields = ('event_type', 'name', 'description', 'extra_data',
                  'position', 'start_date', )