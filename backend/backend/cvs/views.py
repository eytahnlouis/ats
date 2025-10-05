from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .models import Candidate, Job, Resume
from .serializers import CandidateSerializer, CandidateListSerializer
from .services.scoring import score_resume
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import JobSerializer
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobFilter
from rest_framework.permissions import AllowAny


class JobCreateAPIView(APIView):
    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save()
            return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to upload a CV
def upload_and_score(request):
    serializer = CandidateSerializer(data=request.data)
    if serializer.is_valid():
        candidate = serializer.save(user=request.user)
        
        # Calcul du score si un CV est présent
        score = 0.0
        try:
            job_id = request.data.get("job")
            # Récupérer le CV le plus récent du candidat
            latest_resume = candidate.resumes.order_by('-uploaded_at').first()
            
            if latest_resume and latest_resume.file and job_id:
                score = score_resume(latest_resume.file.path, str(job_id))
        except Exception as e:
            # Logger l'erreur pour le debugging
            raise ValueError(f"Erreur lors du calcul de score pour candidat {candidate.id}: {e}")
            score = 0.0
        
        candidate.score = score
        candidate.save(update_fields=['score'])
        
        return Response({
            "candidate": CandidateSerializer(candidate).data,
            "score": score
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_candidates(request):
    user = request.user
    candidates = Candidate.objects.filter(user=user)
    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_top_candidates(request):
    limit = int(request.query_params.get('limit', 10))  # Par défaut top 10
    candidates = Candidate.objects.all().order_by('-score')[:limit]
    serializer = CandidateSerializer(candidates, many=True)
    return Response({
        "limit": limit,
        "results": serializer.data
    }, status=status.HTTP_200_OK)

# """
# API view for creating a new Job instance.

# This view requires the user to be authenticated. It handles POST requests by validating
# the incoming data with the JobSerializer. If the data is valid, a new Job is created and
# the serialized job data is returned with a 201 Created status. If the data is invalid,
# the serializer errors are returned with a 400 Bad Request status.
# """
class JobCreateAPIView(APIView):
    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save()
            return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class JobListAPIView(ListAPIView):
    """API view to list all job postings.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer



class JobListAPIView(generics.ListAPIView):
    """
    API view to list all job postings with filtering capabilities.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]  # Allow any user to view job postings
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobFilter

class CandidatesByJobAPIView(ListAPIView):
    serializer_class = CandidateListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs["job_id"]
        return Candidate.objects.filter(job_id=job_id).order_by("-score", "-created_at")

#UP-S : name of the algortithm used to score the resume
class JobDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permet de récupérer, modifier ou supprimer une offre d'emploi spécifique.
    GET    /api/cvs/jobs/<id>/     → détail du job
    PUT    /api/cvs/jobs/<id>/     → update complet
    PATCH  /api/cvs/jobs/<id>/     → update partiel
    DELETE /api/cvs/jobs/<id>/     → suppression
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]  # ou [AllowAny] si tu veux public
    lookup_field = 'id'
