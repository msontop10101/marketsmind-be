from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model, logout
from .models import BlacklistedToken
from django.core.exceptions import ObjectDoesNotExist
from .serializers import UserSerializer, LoginSerializer, SignUpSerializer, ForgotPasswordSerializer, ResetPasswordSerializer

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework import generics, status, serializers, response
from django.core.mail import send_mail
from django.conf import settings


User = get_user_model()

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except ObjectDoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if user.check_password(serializer.validated_data['password']):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)



class SignUpAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

# User = get_user_model()

class ForgotPasswordAPIView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except ObjectDoesNotExist:
            return response.Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Generate and send the password reset link via email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"http://127.0.0.1:8000/api/reset-password/{uid}/{token}/"

        email_subject = "Password Reset"
        email_message = f"Please click the link below to reset your password:\n\n{reset_link}"

        try:
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,  # Use the default sender email from settings.py
                [user.email],
                fail_silently=False,  # Set this to True if you want to suppress errors silently
            )
            return response.Response({"message": "Password reset email sent."})
        except Exception as e:
            # Log the error message to the console to see what went wrong
            print("Error sending email:", e)
            return response.Response({"error": "Failed to send the password reset email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, uidb64, token):
        # Logic to validate uidb64 and token and retrieve user (not implemented in this example)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Logic to reset password (not implemented in this example)
        return Response({"message": "Password reset successful."})

class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({"error": "Refresh token is required for logout."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the provided refresh token
            token = RefreshToken(refresh_token)
            token.verify()

            # Blacklist the refresh token for the authenticated user
            BlacklistedToken.objects.create(user=request.user, token=refresh_token)

            # Return a success message
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle exceptions (e.g., token has expired or is invalid)
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)