from crispy_forms.helper import FormHelper
from django import forms
from apps.events.models import Event, EventType


class EventModelForm(forms.ModelForm):

    event_type = forms.ModelChoiceField(
        queryset=EventType.objects.filter(status=EventType.STATUS_ACTIVE),
        label='Tipo de Evento'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Nombre'
        self.fields['description'].label = 'Descipción'
        self.fields['extra_data'].label = 'Información extra'
        self.fields['position'].label = 'Ubicación'
        self.fields['start_date'].label = 'Fecha de inicio'
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False

    class Meta:
        model = Event
        fields = ('event_type', 'name', 'description', 'extra_data',
                  'position', 'start_date', )