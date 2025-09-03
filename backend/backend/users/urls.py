from django.urls import path, include
from .views import RegisterView, MeAPIView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("me/", MeAPIView.as_view(), name="me"),


]