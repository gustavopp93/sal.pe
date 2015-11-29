from braces.views import JSONResponseMixin

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, View
from apps.core.extra.constants import ORGANIZATION_ID_KEY

from apps.core.extra.mixin import LoginRequiredMixin, OrganizationRequiredMixin

from apps.events.forms.events import EventModelForm
from apps.events.models import Event, EventType


class EventListView(LoginRequiredMixin,
                    OrganizationRequiredMixin,
                    ListView):
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        event_type = self.request.GET.get('event_type', None)
        if event_type is not None and event_type != '':
            queryset = queryset.filter(event_type_id=event_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_types'] = EventType.objects.all()
        return context


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

    def filter_queryset(self, queryset):
        event_type = self.request.GET.get('event_type', None)
        if event_type is not None and event_type.isdigit():
            queryset = queryset.filter(event_type_id=event_type)
        return queryset

    def get(self, request, *args, **kwargs):
        events = Event.objects.all()
        events = self.filter_queryset(events)
        data = []
        for event in events:
            data.append({
                'id': event.id,
                'name': event.name,
                'latitude': event.position.latitude,
                'longitude': event.position.longitude,
                'event_type_id': event.event_type_id,
                'avatar': event.avatar.url,
                'description': event.description,
                'extra_data': event.extra_data
            })
        return self.render_json_response(data)


class EventTypeListJSONView(JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        event_types = EventType.objects.filter(status=EventType.STATUS_ACTIVE)
        event_types = list(event_types.values('id', 'name'))
        return self.render_json_response(event_types)
