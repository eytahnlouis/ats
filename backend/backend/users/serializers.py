
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model() # Use the custom user model if defined, otherwise use the default User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]  
