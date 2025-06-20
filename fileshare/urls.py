from django.urls import path
from .views import *

app_name = 'fileshare'

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('verify-email/', VerifyEmail.as_view()),
    path('login/', LoginView.as_view()),
    path('upload/', FileUploadView.as_view()),
    path('list/', ListFilesView.as_view()),
    path('generate-download/<int:file_id>/', GenerateDownloadLinkView.as_view()),
    path('download/<str:token>/', DownloadFileView.as_view(), name='download'),
]
