from rest_framework import serializers
from .models import Job, Keyword, Candidate, Resume
from django.db import transaction


class CandidateSerializer(serializers.ModelSerializer): # Candidate serializer to convert Candidate model instances to JSON and vice versa
    class Meta: # Candidate serializer metadata
        model = Candidate
        fields = ("id", "name", "email", "phone", "resume", "job") # Include job field for associating candidate with a job
        read_only_fields = ['score', 'id', 'created_at']

class CandidateListSerializer(serializers.ModelSerializer): # Serializer for listing candidates with limited fields
    class Meta:
        model = Candidate
        fields = ("id", "name", "email", "phone", "score", "created_at")


class KeywordSerializer(serializers.ModelSerializer): # Keyword serializer to convert Keyword model instances to JSON and vice versa
    class Meta:
        model = Keyword
        fields = ['id', 'word', 'weight']

class JobSerializer(serializers.ModelSerializer): # Job serializer to convert Job model instances to JSON and vice versa
    keywords = KeywordSerializer(many=True)

    class Meta:  # Job serializer metadata
        model = Job
        fields = ['id', 'title', 'description', 'location', 'keywords', 'created_at', 'is_active']

    def create(self, validated_data):
        keywords_data = validated_data.pop('keywords') # Extract keywords data from validated_data
        # Create the Job instance without keywords first
        job = Job.objects.create(**validated_data, is_active=True) # Default to active job
        # Now handle the keywords
        for keyword in keywords_data:
            kw, _ = Keyword.objects.get_or_create(word=keyword['word'], defaults={'weight': keyword['weight']})
            job.keywords.add(kw)
        return job

    from django.db import transaction

    def update(self, instance, validated_data):
        # Récupère les keywords
        keywords_data = validated_data.pop('keywords', None)

        # Met à jour les champs simples du job
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if keywords_data is not None:
            with transaction.atomic():
                instance.keywords.all().delete()
                kws = [
                    Keyword(job=instance, **{
                        'id': kw.get('id'),
                        'word': str(kw.get('word','')).strip(),
                        'weight': float(kw.get('weight', 1.0))
                        # ajouter autres champs si nécessaire
                    })
                    for kw in keywords_data
                ]
                Keyword.objects.bulk_create(kws)

        return instance
    
class JobListSerializer(serializers.ModelSerializer): # Serializer for listing jobs with limited fields
    class Meta:
        model = Job
        fields = ['id', 'title', 'location', 'created_at', 'is_active']
        read_only_fields = ['id', 'created_at']

class ResumeSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    file_size_mb = serializers.SerializerMethodField()
    
    class Meta:
        model = Resume
        fields = ['id', 'file', 'uploaded_at', 'candidate', 'candidate_name', 'file_size_mb']
        read_only_fields = ['id', 'uploaded_at']
         
    def get_file_size_mb(self, obj):
        return round(obj.size / (1024 * 1024), 2) if obj.size else None 
    
    def validate_file(self, value):
        # Validation du type de fichier
        allowed_types = ['application/pdf', 'application/msword', 
                         'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if not value.content_type or value.content_type not in allowed_types:
            raise serializers.ValidationError("Type de fichier non supporté. Seuls les PDF et Word sont autorisés.")
        
        # Validation de la taille du fichier (max 3MB)
        max_size = 3 * 1024 * 1024  # 3MB
        if value.size >= max_size:
            raise serializers.ValidationError("La taille du fichier dépasse la limite de 5MB.")
        
        return value