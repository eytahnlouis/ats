"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # pour login
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # pour refresh token
    path('users/', include('users.urls')), # pour les routes de l'api users
    path('api/cvs/', include('cvs.urls')), # pour les routes de l'api cvs
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # à changer pour la prod
