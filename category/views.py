from .models import Category
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [permissions.AllowAny] # For test