from .models import Motivator
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import MotivatorSerializer

class MotivatorViewSet(viewsets.ModelViewSet):
	queryset = Motivator.objects.all()
	serializer_class = MotivatorSerializer
	permission_classes = [permissions.AllowAny] # For test