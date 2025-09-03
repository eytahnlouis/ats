from django.urls import path
from .views import upload_and_score, list_user_candidates, list_top_candidates
from django.urls import path
from .views import JobCreateAPIView, JobListAPIView, CandidatesByJobAPIView
urlpatterns = [
    path('upload/', upload_and_score, name='upload_and_score'), # Endpoint to upload and score a CV
    path('my-candidates/', list_user_candidates, name='list_user_candidates'), # Endpoint to list all candidates for the authenticated user
    path('top/', list_top_candidates, name='list_top_candidates'), # Endpoint to list top candidates
    path('jobs/create/', JobCreateAPIView.as_view(), name='create-job'), # Endpoint to create a job posting
    path('jobs/', JobListAPIView.as_view(), name='job-list'),
    path('jobs/<uuid:pk>/candidates/', CandidatesByJobAPIView.as_view(), name='job-candidates-list'), # Endpoint to list candidates for a specific job

]
