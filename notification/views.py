from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import NotificationPreferences
from .serializers import NotificationPreferencesSerializer

# Create your views here.


class NotificationPreferencesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationPreferencesSerializer

    def get(self, request, *args, **kwargs):
        # Get the UserPreferences object for the current user (you need to implement this logic)
        notification_preferences = NotificationPreferences.objects.get(
            user_id=request.user.id
        )  # You may need to adjust this based on your authentication logic

        # Serialize the UserPreferences object
        serializer = NotificationPreferencesSerializer(notification_preferences)

        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)
