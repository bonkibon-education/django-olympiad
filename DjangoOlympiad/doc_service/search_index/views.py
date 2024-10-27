from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, \
    OrderingFilterBackend, SearchFilterBackend
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework.pagination import PageNumberPagination

from .serializers import VisitDocumentSerializer
from .visit_document import VisitDocument

class CustomPagination(PageNumberPagination):
    """Пагинация для управления объемом данных в каждом запросе."""
    page_size = 20  # Количество документов на одной странице
    page_size_query_param = 'page_size'
    max_page_size = 100

@extend_schema_view(
    list=extend_schema(
        summary="Получить список документов",
        description="Эндпоинт поиска позволяет получать список документов о визитах с фильтрацией, поиском и сортировкой.",
        parameters=[
            OpenApiParameter(name='room', type=str, location=OpenApiParameter.QUERY,
                             required=False, description='Фильтр по ID комнаты.'),
            OpenApiParameter(name='date', type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY,
                             required=False, description='Фильтр по дате визита.'),
            OpenApiParameter(name='hospitalId', type=int, location=OpenApiParameter.QUERY,
                             required=False, description='Фильтр по ID больницы.'),
            OpenApiParameter(name='patientId', type=int, location=OpenApiParameter.QUERY,
                             required=False, description='Фильтр по ID пациента.'),
            OpenApiParameter(name='doctorId', type=int, location=OpenApiParameter.QUERY,
                             required=False, description='Фильтр по ID доктора.'),
            OpenApiParameter(name='ordering', type=str, location=OpenApiParameter.QUERY,
                             required=False, description='Сортировка результатов (например, date,-date).'),
            OpenApiParameter(name='search', type=str, location=OpenApiParameter.QUERY,
                             required=False, description='Поле основного поиска по документам визитов.'),
        ],
    ),
    retrieve=extend_schema(
        summary="Получить конкретный документ",
        description="Эндпоинт поиска позволяет получить конкретный документ визита по ID.",
        parameters=[
            OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH,
                             required=True),
        ],
    ),
)
class VisitDocumentViewSet(BaseDocumentViewSet):
    document = VisitDocument
    serializer_class = VisitDocumentSerializer
    lookup_field = 'id'
    pagination_class = CustomPagination
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
    ]
    queryset = document.search()
    search_fields = ('data',)  # Ограничено наиболее востребованным полем
    filter_fields = {
        'id': 'id',
        'room': 'room',
        'data': 'data',
        'date': 'date',
        'hospitalId': 'hospitalId',
        'patientId': 'patientId',
        'doctorId': 'doctorId',
    }
    ordering_fields = {
        'id': 'id',
        'date': 'date',
        'hospitalId': 'hospitalId',
        'patientId': 'patientId',
        'doctorId': 'doctorId',
    }
