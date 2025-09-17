from django.db import models
from uuid import uuid4
import uuid
from rest_framework import serializers
from django.contrib.auth.models import User

#Model to store what we are looking for in a job
# This model is used to store the keywords and their weights for scoring
class Keyword(models.Model):
    word = models.CharField(max_length=100, unique=True)
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.word} (Poids: {self.weight})"

class Job(models.Model): # Job model to store information about job postings
    """ 
    Structure of the Job model:
    - id_unique: UUID (primary key)
    - titre: CharField (max_length=255)
    - description: TextField
    - localisation: CharField (max_length=100, blank=True)
    - keywords: ManyToManyField (related to Keyword model)
    - created_at: DateTimeField (auto_now_add=True)
    - disponible: BooleanField (default=True)

    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    keywords = models.ManyToManyField('Keyword', blank=True)  # Lié aux mots-clés de scoring
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

#Model to store information about candidates
class Candidate(models.Model): # Candidate model to store information about job applicants
    """ 
    Structure of the Candidate model:
    - id_unique: UUID (primary key)
    - nom_prenom: CharField (max_length=255)
    - email: EmailField
    - phone: CharField (max_length=20)
    - resume: FileField (upload_to='resumes/')
    - date_of_applying: DateTimeField (auto_now_add=True)
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4, 
        editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='candidates') # Foreign key to the job posting
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)    # Foreign key to the user who uploaded the resume
    score = models.FloatField(default=0.0)  # Score of the candidate based on the resume
    def __str__(self):
        return self.name
    