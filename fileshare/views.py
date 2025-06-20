from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import *
from .models import *
from .permissions import IsClientUser, IsOpsUser
from django.core.signing import Signer, BadSignature
from django.core.mail import send_mail
from .utils import allowed_file_type
from django.conf import settings
from django.urls import reverse

signer = Signer()

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            signed_url = signer.sign(user.username)
            verify_url = f"http://localhost:8000/api/verify-email/?token={signed_url}"
            send_mail('Verify Email', f'Click to verify: {verify_url}', settings.DEFAULT_FROM_EMAIL, [user.email])
            return Response({'encrypted-url': verify_url}, status=201)
        return Response(serializer.errors, status=400)

class VerifyEmail(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get('token')
        try:
            username = signer.unsign(token)
            user = User.objects.get(username=username)
            user.is_verified = True
            user.save()
            return Response({'message': 'Email verified'})
        except (BadSignature, User.DoesNotExist):
            return Response({'error': 'Invalid token'}, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=400)

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated, IsOpsUser]

    def post(self, request):
        file = request.FILES.get('file')
        if not allowed_file_type(file.name):
            return Response({'error': 'Only .pptx, .docx, .xlsx allowed'}, status=400)
        upload = UploadedFile.objects.create(owner=request.user, file=file)
        return Response({'message': 'File uploaded', 'file_id': upload.id})

class ListFilesView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request):
        files = UploadedFile.objects.all()
        serializer = FileListSerializer(files, many=True)
        return Response(serializer.data)

class GenerateDownloadLinkView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request, file_id):
        try:
            file = UploadedFile.objects.get(id=file_id)
            signed_id = signer.sign(str(file.id))
            url = request.build_absolute_uri(reverse('fileshare:download', args=[signed_id]))
            return Response({'download-link': url, 'message': 'success'})
        except UploadedFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=404)

class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request, token):
        try:
            file_id = signer.unsign(token)
            file = UploadedFile.objects.get(id=file_id)
            return Response({'file_url': file.file.url})
        except (BadSignature, UploadedFile.DoesNotExist):
            return Response({'error': 'Invalid or expired link'}, status=400)
