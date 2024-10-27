from api.models import Visit
from django_elasticsearch_dsl.registries import registry

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Visit)
def update_document(sender, instance, **kwargs):
    """Обновляет документ Visit при добавлении/изменении Visit."""
    # Обновляем только экземпляр, который вызвал сигнал
    registry.update(instance)


@receiver(post_delete, sender=Visit)
def delete_document(sender, instance, **kwargs):
    """Удаляет документ Visit при удалении Visit."""
    # Удаляем только экземпляр, который вызвал сигнал
    registry.delete(instance)
