from rest_framework import serializers
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'activity_type', 'duration', 'distance',
            'calories_burned', 'date', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_duration(self, value): 
        if value <= 0:
            raise serializers.ValidationError("Duration must be greater than 0 minutes.")
        return value

    def validate_distance(self, value):
        if  value < 0:
            raise serializers.ValidationError("Distance cannot be negative.")
        return value

    def validate_calories_burned(self, value):
        if value < 0:
            raise serializers.ValidationError("Calories burned cannot be negative.")
        return value
    
class ActivitySummarySerializer(serializers.Serializer):
    total_activities = serializers.IntegerField()
    total_duration = serializers.IntegerField()
    total_distance = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_calories = serializers.IntegerField()
    average_duration = serializers.FloatField()

class ActivityTrendSerializer(serializers.Serializer):
    period = serializers.CharField()
    total_duration = serializers.IntegerField()
    total_distance = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_calories = serializers.IntegerField()
    activity_count = serializers.IntegerField()