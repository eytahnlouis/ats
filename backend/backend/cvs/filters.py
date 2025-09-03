import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    """
    Filter for Job model to allow searching by title, location, and keywords.
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    keywords__word = django_filters.CharFilter(field_name='keywords__word', lookup_expr='icontains')

    class Meta:
        model = Job
        fields = ['title', 'location', 'keywords__word']