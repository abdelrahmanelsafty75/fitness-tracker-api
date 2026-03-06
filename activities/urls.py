from django.urls import path
from .views import (
    ActivityListCreateView,
    ActivityDetailView,
    ActivitySummaryView,
    ActivityTrendsView,
    ActivityStatsByTypeView 
)
urlpatterns = [

    path('', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),

    path('summary/', ActivitySummaryView.as_view(), name='activity-summary'),
    path('trends/', ActivityTrendsView.as_view(), name='activity-trends'),
    path('stats-by-type/', ActivityStatsByTypeView.as_view(), name='activity-stats-by-type'),
]