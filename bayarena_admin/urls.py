from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from motivator import views as motivator_views
from lecture import views as lecture_views
from category import views as category_vies

router = routers.DefaultRouter()
router.register(r'motivators', motivator_views.MotivatorViewSet)
router.register(r'lectures', lecture_views.LectureViewSet)
router.register(r'category', category_vies.CategoryViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)