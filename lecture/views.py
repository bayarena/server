from .models import Lecture
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import LectureSerializer

class LectureViewSet(viewsets.ModelViewSet):
	queryset = Lecture.objects.all()
	serializer_class = LectureSerializer
	permission_classes = [permissions.AllowAny] # For test

	def get_queryset(self):
		length = self.request.query_params.get('length')
		if length is not None:
			try:
				length_int = int(length)
				return Lecture.objects.all().order_by("-date")[0:length_int]
			except ValueError:
				pass

		staged = self.request.query_params.get('staged')
		if staged is not None:
			try:
				return Lecture.objects.filter(staging__gt=0).order_by("staging")
			except :
				pass

		return Lecture.objects.all()