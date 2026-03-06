from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'duration', 'distance', 'calories_burned', 'date', 'created_at']
    list_filter = ['activity_type', 'date', 'created_at']
    search_fields = ['user__username', 'notes', 'activity_type']
    readonly_fields = ['created_at', 'updated_at']
    
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Activity Details', {
            'fields': ('user', 'activity_type', 'date')
        }),
        ('Metrics', {
            'fields': ('duration', 'distance', 'calories_burned')
        }),
        ('Additional Info', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )