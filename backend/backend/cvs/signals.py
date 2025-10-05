# Signal pour invalider le cache quand un job est modifié
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Job, Keyword
from .services.keyword_cache import keyword_cache

@receiver(post_save, sender=Job)
@receiver(post_delete, sender=Job)
def invalidate_job_cache(sender, instance, **kwargs):
    """Invalide le cache quand un job est modifié"""
    keyword_cache.invalidate(str(instance.id))

@receiver(post_save, sender=Keyword)
@receiver(post_delete, sender=Keyword)
def invalidate_keyword_cache(sender, instance, **kwargs):
    """Invalide tout le cache quand un keyword est modifié"""
    # Invalide tout car on ne sait pas quels jobs sont affectés
    keyword_cache.invalidate()

# Tâche de nettoyage périodique (optionnel avec Celery)
def cleanup_cache():
    """Nettoie le cache périodiquement"""
    keyword_cache.cleanup_expired()