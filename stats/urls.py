from django.urls import path
from django.views.generic.base import RedirectView

from .views import ProducerLiveStatsView, ProducerLiveStatsJSONView
from .views import ProducerHistoryView, ProducerHistoryJSONView

urlpatterns = [
    path('<int:producer_id>/', ProducerLiveStatsView.as_view(), name='producer_live_stats'),
    path('<int:producer_id>/json', ProducerLiveStatsJSONView.as_view(), name='producer_live_stats_json'),
    path('<int:producer_id>/<str:time_period>', ProducerHistoryView.as_view(), name='producer_history'),
    path('<int:producer_id>/<str:time_period>/json', ProducerHistoryJSONView.as_view(), name='producer_history_json'),
]

