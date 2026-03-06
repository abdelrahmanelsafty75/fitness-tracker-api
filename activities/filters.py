import django_filters
from .models import Activity

class ActivityFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        help_text="Filter activities from this date (YYYY-MM-DD)"
    )
    end_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        help_text="Filter activities up to this date (YYYY-MM-DD)"
    )
    min_duration = django_filters.NumberFilter(
        field_name='duration',
        lookup_expr='gte',
        help_text="Filter activities with minimum duration (minutes)"
    )
    max_duration = django_filters.NumberFilter(
        field_name='duration',
        lookup_expr='lte',
        help_text="Filter activities with maximum duration (minutes)"
    )
    min_calories = django_filters.NumberFilter(
        field_name='calories_burned',
        lookup_expr='gte',
        help_text="Filter activities with minimum calories burned"
    )
    max_calories = django_filters.NumberFilter(
        field_name='calories_burned',
        lookup_expr='lte',
        help_text="Filter activities with maximum calories burned"
    )
    activity_type = django_filters.ChoiceFilter(
        choices=Activity.ACTIVITY_TYPES,
        help_text="Filter by activity type"
    )

    class Meta:
        model = Activity
        fields = [
            'activity_type',
            'start_date',
            'end_date',
            'min_duration',
            'max_duration',
            'min_calories',
            'max_calories'
        ]