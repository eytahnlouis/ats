from django.db import models
from uuid import uuid4
import uuid
from rest_framework import serializers
from django.contrib.auth.models import User
from .services.parsing import extract_text_from_file

#Model to store what we are looking for in a job
# This model is used to store the keywords and their weights for scoring
class Keyword(models.Model):
    """
    Structure of the Keyword model:
    - id_unique: UUID (primary key)
    - mot: CharField (max_length=100, unique=True)
    - poids: FloatField (default=1.0)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.CharField(max_length=100, unique=False)
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True, default="Paris")
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
    - date_of_applying: DateTimeField (auto_now_add=True)
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4, 
        editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='candidates') # Foreign key to the job posting
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)    # Foreign key to the user who uploaded the resume
    score = models.FloatField(default=0.0)  # Score of the candidate based on the resume
    def __str__(self):
        return self.name
    
class Resume(models.Model): 
    """
    Structure of the Resume model:
    - id_unique: UUID (primary key)
    - candidate: ForeignKey (related to Candidate model)
    - file: FileField (upload_to='resumes/')
    - uploaded_at: DateTimeField (auto_now_add=True)
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField(null=True, blank=True)  # Taille du fichier en octets
    file_type = models.CharField(max_length=50, null=True, blank=True)  # Type MIME du fichier
    text_content = models.TextField(null=True, blank=True)  # Contenu textuel extrait du CV
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file and not self.text_content:
            try:
                self.text_content = extract_text_from_file(self.file.path)
                super().save(update_fields=['text_content'])
            except Exception as e:
                # Logger l'erreur sans faire échouer la sauvegarde
                pass
    
    def __str__(self):
        return f"Resume of {self.candidate.name} uploaded at {self.uploaded_at}"