from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Candidate, Job, Resume
from .serializers import CandidateSerializer, CandidateListSerializer, JobSerializer
from .services.scoring import score_resume
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobFilter
import logging
from django.db import transaction

logger = logging.getLogger(__name__)


class JobCreateAPIView(APIView):
    """
    API view for creating a new Job instance.
    Requires authentication. Handles POST requests to create a job.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save()
            return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobListAPIView(generics.ListAPIView):
    """
    API view to list all job postings with filtering capabilities.
    Allows any user to view job postings.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobFilter


class JobDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific job posting.
    Requires authentication.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to upload a CV
@transaction.atomic
def upload_and_score(request):
    """
    Upload a candidate's CV and calculate the matching score against a job.
    Returns the candidate data and the score.
    """
    serializer = CandidateSerializer(data=request.data)
    if serializer.is_valid():
        candidate = serializer.save(user=request.user)
        
        # Calculate score if a CV is present
        score = 0.0
        try:
            job_id = request.data.get("job")
            latest_resume = candidate.resumes.order_by('-uploaded_at').first()
            
            if latest_resume and latest_resume.file and job_id:
                score = score_resume(latest_resume.file.path, str(job_id))
        except Exception as e:
            # Log l'erreur sans interrompre le processus
            logger.error(f"Erreur lors du calcul de score pour candidat {candidate.id}: {e}")
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
    """
    List all candidates associated with the authenticated user.
    """
    user = request.user
    candidates = Candidate.objects.filter(user=user)
    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_top_candidates(request):
    """
    List top candidates ordered by score, limited by query parameter 'limit' (default 10).
    """
    limit = int(request.query_params.get('limit', 10))  # Default top 10
    candidates = Candidate.objects.all().order_by('-score')[:limit]
    serializer = CandidateSerializer(candidates, many=True)
    return Response({
        "limit": limit,
        "results": serializer.data
    }, status=status.HTTP_200_OK)


class CandidatesByJobAPIView(ListAPIView):
    """
    List candidates filtered by a specific job ID, ordered by score and creation date.
    Requires authentication.
    """
    serializer_class = CandidateListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs["job_id"]
        return Candidate.objects.filter(job_id=job_id).order_by("-score", "-created_at")
