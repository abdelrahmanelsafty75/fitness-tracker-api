from .models import Activity
from .serializers import ActivitySerializer
from rest_framework import generics, permissions

# make sure only the owner of the activity can view or edit it
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class ActivityListCreateView(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

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