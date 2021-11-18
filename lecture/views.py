from .models import Lecture
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import LectureSerializer

class LectureViewSet(viewsets.ModelViewSet):
	queryset = Lecture.objects.all()
	serializer_class = LectureSerializer
	permission_classes = [permissions.AllowAny] # For test