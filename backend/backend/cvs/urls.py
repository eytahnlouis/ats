from django.urls import path
from .views import (
    UploadAndScoreAPIView as upload_and_score,
    list_user_candidates,
    list_top_candidates,
    JobCreateAPIView,
    JobListAPIView,
    CandidatesByJobAPIView,
    JobDetailAPIView,
)
urlpatterns = [
    path('upload/', upload_and_score.as_view(), name='upload_and_score'), # Endpoint to upload and score a CV
    path('my-candidates/', list_user_candidates, name='list_user_candidates'), # Endpoint to list all candidates for the authenticated user
    path('top/', list_top_candidates, name='list_top_candidates'), # Endpoint to list top candidates
    path('jobs/create/', JobCreateAPIView.as_view(), name='create-job'), # Endpoint to create a job posting
    path('jobs/', JobListAPIView.as_view(), name='job-list'),
    path('jobs/<uuid:id>/candidates/', CandidatesByJobAPIView.as_view(), name='job-candidates-list'), # Endpoint to list candidates for a specific job
    path('jobs/<uuid:id>/', JobDetailAPIView.as_view(), name='job-detail'), # Endpoint to retrieve, update, or delete a specific job

]
