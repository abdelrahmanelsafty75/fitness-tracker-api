from .models import Activity
from .serializers import ActivitySerializer
from rest_framework import generics, permissions

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ActivityFilter

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count
from django.db.models.functions import TruncWeek, TruncMonth

# make sure only the owner of the activity can view or edit it
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class ActivityListCreateView(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ActivityFilter
    ordering_fields = ['date', 'duration', 'calories_burned', 'created_at']
    ordering = ['-date'] 

    def get_queryset(self): # only return activities for the logged in user
        return self.queryset.filter(user=self.request.user)
    def perform_create(self, serializer): # make the logged in user the owner of the activity
        serializer.save(user=self.request.user)

class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner] # must be authenticated and the owner of the activity to view/edit/delete it

    def get_queryset(self): 
        return self.queryset.filter(user=self.request.user)
    

class ActivitySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        queryset = Activity.objects.filter(user=request.user)

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        summary = queryset.aggregate(
            total_activities=Count('id'),
            total_duration=Sum('duration'),
            total_distance=Sum('distance'),
            total_calories=Sum('calories_burned'),
            average_duration=Avg('duration')
        )

        for key in summary:
            if summary[key] is None:
                summary[key] = 0

        return Response(summary)


class ActivityTrendsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        period = request.query_params.get('period', 'weekly')
        queryset = Activity.objects.filter(user=request.user)

        if period == 'weekly':
            trends = queryset.annotate(period_date=TruncWeek('date')).values('period_date')
        elif period == 'monthly':
            trends = queryset.annotate(period_date=TruncMonth('date')).values('period_date')
        else:
            return Response({"error": "Invalid period. Use 'weekly' or 'monthly'."}, status=400)

        trends = trends.annotate(
            total_duration=Sum('duration'),
            total_distance=Sum('distance'),
            total_calories=Sum('calories_burned'),
            activity_count=Count('id')
        ).order_by('period_date')

        formatted_trends = []
        for trend in trends:
            formatted_trends.append({
                'period': trend['period_date'].strftime('%Y-%m-%d') if trend['period_date'] else None,
                'total_duration': trend['total_duration'] or 0,
                'total_distance': trend['total_distance'] or 0,
                'total_calories': trend['total_calories'] or 0,
                'activity_count': trend['activity_count']
            })

        return Response(formatted_trends)


class ActivityStatsByTypeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Activity.objects.filter(user=request.user)
        
        stats = queryset.values('activity_type').annotate(
            total_activities=Count('id'),
            total_duration=Sum('duration'),
            total_distance=Sum('distance'),
            total_calories=Sum('calories_burned'),
            average_duration=Avg('duration')
        ).order_by('-total_duration')

        for stat in stats:
            for key in ['total_activities', 'total_duration', 'total_distance', 'total_calories', 'average_duration']:
                if stat[key] is None:
                    stat[key] = 0

        return Response(stats)