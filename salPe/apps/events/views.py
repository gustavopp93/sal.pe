from braces.views import JSONResponseMixin

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, View
from apps.core.extra.constants import ORGANIZATION_ID_KEY

from apps.core.extra.mixin import LoginRequiredMixin, OrganizationRequiredMixin

from apps.events.forms.events import EventModelForm
from apps.events.models import Event


class EventListView(LoginRequiredMixin,
                    OrganizationRequiredMixin,
                    ListView):
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'
    paginate_by = 10


class EventCreateView(LoginRequiredMixin,
                      OrganizationRequiredMixin,
                      CreateView):
    model = Event
    template_name = 'events/create.html'
    form_class = EventModelForm

    def form_valid(self, form):
        event = form.save(commit=False)
        event.organization_id = self.request.session[ORGANIZATION_ID_KEY]
        event.save()
        return HttpResponseRedirect(reverse('events_list'))


class EventUpdateView(LoginRequiredMixin,
                      OrganizationRequiredMixin,
                      UpdateView):
    model = Event
    template_name = 'events/update.html'
    form_class = EventModelForm

    def form_valid(self, form):
        event = form.save(commit=False)
        event.organization_id = self.request.session[ORGANIZATION_ID_KEY]
        event.save()
        return HttpResponseRedirect(reverse('events_list'))


class EventListJSONView(JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        events = Event.objects.all().only('id', 'name', 'position', 'event_type')
        data = []
        for event in events:
            data.append({
                'id': event.id,
                'name': event.name,
                'latitude': event.position.latitude,
                'longitude': event.position.longitude,
                'event_type_id': event.event_type_id
            })
        return self.render_json_response(data)
