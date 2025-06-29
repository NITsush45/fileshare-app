# fileshare-app
# 📁 FileShare App

A Django REST Framework-based app that enables user signup with email verification, login, secure file uploads, and download link generation with role-based access control.

---

## 🚀 Features

- User Signup with Email Verification
- JWT Authentication
- Role-Based Permissions (Client and Ops)
- Upload DOCX, PPTX, XLSX files
- Generate secure signed download links
- File download using signed URLs

---

## 📦 Requirements

django
djangorestframework
psycopg2-binary
python-magic
django-cors-headers
Postman (for testing APIs)

---

## ⚙️ Setup

```bash
git clone https://github.com/NITsush45/fileshare-app.git
cd fileshare-app
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

API Endpoints (Postman)
1. 👤 User Signup
Endpoint: POST /api/signup/
Request Body:

json
Copy
Edit
{
  "username": "Sushi45",
  "email": "sushiitantmi45@gmail.com",
  "password": "Sush@test26",
  "user_type": "Client"  // or "Ops"
}
Response: Sends email verification link.

2. ✅ Verify Email
Endpoint: GET /api/verify-email/?token=<token>
Action: Verifies the user using signed token sent via email.

3. 🔐 Login
Endpoint: POST /api/login/
Request Body:

json
Copy
Edit
{
  "username": "Sushi45",
  "password": "Sush@test26"
}
Response:

json
Copy
Edit
{
  "token": "<JWT-token>"
}
Use this token in Postman under:

yaml
Copy
Edit
Authorization > Type: Bearer Token > Token: <JWT-token>
4. 📤 Upload File
Endpoint: POST /api/upload/
Authorization: Bearer token (Ops user only)
Form-Data:

Key	Type	Value
file	File	knn.docx

Allowed extensions: .docx, .pptx, .xlsx

Response:

json
Copy
Edit
{
  "message": "File uploaded",
  "file_id": 1
}
5. 📂 List All Files
Endpoint: GET /api/list/
Authorization: Bearer token (Client user only)

Response:

json
Copy
Edit
[
  {
    "id": 1,
    "file": "http://127.0.0.1:8000/media/knn.docx",
    "uploaded_at": "2025-06-20T12:00:00Z"
  }
]
6. 🔗 Generate Download Link
Endpoint: GET /api/generate-download/<file_id>/
Authorization: Bearer token (Client user only)

Response:

json
Copy
Edit
{
  "download-link": "http://127.0.0.1:8000/api/download/<signed_token>/",
  "message": "success"
}
7. 📥 Download File
Endpoint: GET /api/download/<signed_token>/
Authorization: Bearer token (Client user only)

Response:

json
Copy
Edit
{
  "file_url": "http://127.0.0.1:8000/media/knn.docx"
}