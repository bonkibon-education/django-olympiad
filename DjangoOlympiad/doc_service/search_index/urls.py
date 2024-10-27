from rest_framework.routers import DefaultRouter

from django.urls import include, path
from .views import VisitDocumentViewSet

app_name = "search_index"

router = DefaultRouter()
books = router.register(r'visits',
                        VisitDocumentViewSet,
                        basename='visitsdocument')

urlpatterns = [
    path('', include(router.urls)),
]
