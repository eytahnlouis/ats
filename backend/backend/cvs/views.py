from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Candidate, Job, Resume
from .serializers import CandidateSerializer, CandidateListSerializer, JobSerializer, ResumeSerializer
from .services.scoring import score_resume
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobFilter
import logging
from django.db import transaction
from django_ratelimit.decorators import ratelimit
logger = logging.getLogger(__name__) # Configure logger for this module


class JobCreateAPIView(APIView):
    """
    API view for creating a new Job instance.
    Requires authentication. Handles POST requests to create a job.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ Handle POST request to create a new job """
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


class UploadAndScoreAPIView(APIView):
    """
    API view to handle uploading a candidate's CV and scoring it against a job.
    Supports both authenticated and anonymous users.
    """
    permission_classes = [AllowAny]
    
    def dispatch(self, request, *args, **kwargs):
        # Applique le ratelimit sur toute la view DRF
        # block=True => renvoie 429 si limite dépassée
        decorated = ratelimit(key='ip', rate='3/m', method='POST', block=True)(super().dispatch)
        return decorated(request, *args, **kwargs)
    
    def post(self, request):
        print(request.data)
        """
        Upload a candidate's CV and calculate the matching score against a job.
        Returns the candidate data and the score.
        Supports both authenticated and anonymous users.
        """
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            # Associer l'utilisateur seulement s'il est authentifié
            if request.user and request.user.is_authenticated:
                candidate = serializer.save(user=request.user)
                logger.info(f"Candidat {candidate.id} créé par utilisateur authentifié {candidate.user.id}")
            else:
                candidate = serializer.save(user=None)
                logger.info(f"Candidat {candidate.id} créé en mode anonyme: {candidate.phone}, {candidate.email}")
        
            #Calculate score if a CV is present
            score = 0.0
            try:
                job_id = request.data.get("job")
                # Récupère le CV le plus récent du candidat
                latest_resume = Resume.objects.filter(candidate=candidate).order_by('-uploaded_at').first()

                if latest_resume and latest_resume.file and job_id:
                    score = score_resume(latest_resume.file.path, str(job_id))
                elif not latest_resume:
                    logger.warning(f"Aucun CV trouvé pour candidat {candidate.id}")
            except Exception as e:
                # Log l'erreur sans interrompre le processus
                logger.error(f"Erreur lors du calcul de score pour candidat {candidate.id}: {e}", exc_info=True)
                score = 0.0
            
            candidate.score = score
            candidate.save(update_fields=['score'])
            
            return Response({
                "candidate": CandidateSerializer(candidate).data,
                "score": score
            }, status=status.HTTP_201_CREATED)
        print("❌ Serializer errors:", serializer.errors)
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

class UploadResumeAPIView(APIView):
    """
    API view to handle uploading a resume for a candidate.
    Allowed for all users,
    """
    permission_classes = [AllowAny]

    def dispatch(self, request, *args, **kwargs):
        """         Applique le ratelimit sur toute la view DRF
        block=True => renvoie 429 si limite dépassée
        """
        if request.user.is_authenticated:
            rate = '10/m'
            key = 'user'
        else:
            rate = '3/m'
            key = 'ip'
        decorated = ratelimit(key=key, rate=rate, method='POST', block=True)(super().dispatch)        
        return decorated(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, candidate_id):
        """
        Upload a resume file for the specified candidate.
        """        
        # Vérifier d'abord si le fichier est présent
        if 'file' not in request.FILES:
            print("❌ No file in request")
            return Response({"file": ["No file provided."]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if request.user.is_authenticated:
                # Pour les utilisateurs authentifiés, vérifier que le candidat leur appartient
                print(f"👤 Utilisateur authentifié: {request.user.id}")
                candidate = Candidate.objects.select_for_update().get(
                    id=candidate_id,
                    user=request.user)
            else:
                # Pour les utilisateurs anonymes, juste vérifier que le candidat existe
                candidate = Candidate.objects.select_for_update().get(id=candidate_id)
        except Candidate.DoesNotExist:
            return Response({"candidate": ["Invalid pk \"{}\" - object does not exist.".format(candidate_id)]}, status=status.HTTP_400_BAD_REQUEST)

        resume_file = request.FILES['file']
        
        # Valider le fichier avec le serializer
        file_serializer = ResumeSerializer(data={'file': resume_file})
        if not file_serializer.is_valid():
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            Resume.objects.filter(candidate=candidate).delete()  # Supprime tous les CV existants
            resume = Resume.objects.create(candidate=candidate, file=resume_file)

        try:
            logger.info(f"Resume uploaded for candidate {candidate.id} by user {request.user.id if request.user.is_authenticated else 'anonymous'}")
            # Calculate and save score if a job is associated with the candidate
            if candidate.job_id:
                candidate.score = score_resume(resume.file.path, str(candidate.job_id))
            else:
                candidate.score = 0.0
            candidate.save(update_fields=['score'])

        except Exception as e:
            logger.error(f"Error logging resume upload for candidate {candidate.id}: {e}", exc_info=True)

        return Response({"detail": "Resume uploaded successfully.", "resume_id": resume.id, "score": candidate.score}, status=status.HTTP_201_CREATED)