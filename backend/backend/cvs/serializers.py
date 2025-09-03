from rest_framework import serializers
from .models import Job, Keyword, Candidate

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ("id", "name", "email", "phone", "resume", "job")
        read_only_fields = ['score', 'id', 'created_at']

class CandidateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ("id", "name", "email", "phone", "score", "created_at")


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'word', 'weight']

class JobSerializer(serializers.ModelSerializer):
    keywords = KeywordSerializer(many=True)

    class Meta:
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