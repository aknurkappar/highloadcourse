from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .forms import AudioUploadForm
from .models import Email, AudioUpload
from .serializers import EmailSerializer
from .task import send_email_task, process_audio_file
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
import random

User = get_user_model()

class EmailViewSet(ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        email = serializer.instance
        send_email_task.delay(email.recipient, email.subject, email.body)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TwoFactorAuthViewSet(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            otp = f"{random.randint(100000, 999999)}"
            user.otp = otp
            user.save()
            print(f"Send this OTP to the user: {otp}")

            return Response({"message": "Please verify OTP"})
        return Response({"message": "Invalid credentials"}, status=401)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        username = request.data.get('username')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(username=username, otp=otp)
            user.otp = None
            user.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "Login successful!",
                "access": access_token,
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Invalid OTP"}, status=401)

    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        secret_info = request.data.get('secret_info')

        if not username or not email or not password:
            return Response({"message": "All fields are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"message": "Username already taken"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"message": "Email already registered"}, status=400)

        if secret_info:
            secret_info = make_password(secret_info)
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            secret_info=secret_info
        )
        return Response({"message": "User registered successfully!", "username": user.username})


class TestViewSet(ViewSet):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    @action(detail=False, methods=['get'])
    def throttling(self, request, *args, **kwargs):
        return Response({"message": "Testing throttling"})

# large audio file uploading
def upload_audio(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save()
            process_audio_file.delay(upload.id)
            return redirect('audio_progress', upload_id=upload.id)
    else:
        form = AudioUploadForm()
    return render(request, 'audio_upload/upload.html', {'form': form})

def audio_progress(request, upload_id):
    upload = get_object_or_404(AudioUpload, id=upload_id)
    return render(request, 'audio_upload/progress.html', {'upload': upload})
