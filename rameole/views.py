from django.views.generic.base import RedirectView, TemplateView

class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['producer'] = Producer.objects.get(id=context['producer_id'])
        return context

