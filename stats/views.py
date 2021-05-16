from django.http import HttpResponse
from django.http.response import Http404
from django.views.generic.base import RedirectView, TemplateView
from chartjs.views.lines import BaseLineChartView
from datetime import date, datetime

from stats.models import ProductionData, Producer, ProductionHistory

class ProducerLiveStatsJSONView(BaseLineChartView):
    def get_labels(self):
        prod_data = ProductionData.objects.filter(producer_id=self.kwargs['producer_id'])
        labels = []
        last_date = date.today()    # Do not print day if today or hasn't changed
        for datapoint in prod_data:
            label = ''

            if(datapoint.time.date() != last_date):
                label += str(datapoint.time.date()) + ' '
                last_date = datapoint.time.date()
            label += datapoint.time.time().isoformat(timespec='seconds')
            labels.append(label)
        return labels
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Voltage", "Amperage", "Wattage", "Frequency"]

    def get_data(self):
        prod_data = ProductionData.objects.filter(producer_id=self.kwargs['producer_id'])
        data = []

        volts = []
        for datapoint in prod_data:
            volts.append(datapoint.voltage)
        data.append(volts)
        amps = []
        for datapoint in prod_data:
            amps.append(datapoint.amperage)
        data.append(amps)
        watts = []
        for datapoint in prod_data:
            watts.append(round(datapoint.voltage * datapoint.amperage, 1))
        data.append(watts)
        hertz = []
        for datapoint in prod_data:
            hertz.append(datapoint.frequency)
        data.append(hertz)

        return data
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35]]

class ProducerHistoryJSONView(BaseLineChartView):
    def get_labels(self):
        period_str = self.kwargs['time_period'].lower()
        history_data = ProductionHistory.objects.filter(producer_id=self.kwargs['producer_id'], time_period=period_str)
        labels = []

        for datapoint in history_data:
            dt: datetime = datapoint.time.datetime()
            if period_str == 'year':
                label = dt.year
            elif period_str == 'month':
                label = dt.month + '-' + dt.year
            elif period_str == 'week':
                label = dt.date().isocalendar()[1]
            elif period_str == 'day':
                label = dt.day + '-' + dt.month
            elif period_str == 'hour':
                label = dt.hour
            else:
                raise Http404('Unknown time period')

            labels.append(label)
        return labels

    def get_providers(self):
        """Return names of datasets."""
        return ["Energy (Wh)"]

    def get_data(self):
        history_data = ProductionHistory.objects.filter(producer_id=self.kwargs['producer_id'], time_period=self.kwargs['time_period'].lower())
        data = []
        for datapoint in history_data:
            data.append(datapoint.watt_hours)

        return data

class ProducerLiveStatsView(TemplateView):
    template_name = "producer_live_stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prod_id = context['producer_id']
        prod_data = ProductionData.objects.filter(producer_id=prod_id)
        for datapoint in prod_data:
            datapoint.wattage = datapoint.voltage * datapoint.amperage
        context['prod_data'] = prod_data
        context['producer'] = Producer.objects.get(id=context['producer_id'])
        context['JSONView'] = 'producer_live_stats_json'
        return context

class ProducerHistoryView(TemplateView):
    template_name = "producer_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if(not context['time_period'].lower() in ProductionHistory.Timescale):
            raise Http404('Time period does not exist') 
        history_data = ProductionHistory.objects.filter(producer_id=context['producer_id'], time_period=context['time_period'].lower())
        context['history_data'] = history_data
        context['producer'] = Producer.objects.get(id=context['producer_id'])
        context['JSONView'] = 'producer_history_json'
        return context

