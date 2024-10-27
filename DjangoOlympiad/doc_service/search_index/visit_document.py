from api.models import Visit
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from django.conf import settings

# Увеличим количество шардов для повышения производительности
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
INDEX.settings(
    number_of_shards=3,  # Увеличено количество шардов
    number_of_replicas=1
)

# Настроим анализатор для минимально необходимых фильтров
html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop"],  # Минимальные фильтры
    char_filter=["html_strip"]
)

@INDEX.doc_type
class VisitDocument(Document):
    """Elasticsearch документ для модели Visit."""

    id = fields.IntegerField(attr='id')
    data = fields.TextField(attr='data', analyzer=html_strip)
    date = fields.DateField(attr='date')
    room = fields.TextField(attr='room')
    hospital_id = fields.IntegerField()
    patient_id = fields.IntegerField()
    doctor_id = fields.IntegerField()

    class Django(object):
        model = Visit
