from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('post-job/', views.post_job, name='post_job'),  # Job posting page
    path('create-job/', views.create_job, name='create_job'),  # Job creation page
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),  # Specific job
    path('recruitment-dashboard/', views.recruitment_dashboard, name='recruitment_dashboard'),  # Recruitment dashboard
    path('upload-cv/', views.upload_cv, name='upload_cv'),  # CV upload
    path('jobs/', views.job_list, name='job_list'),  # Fetch jobs
]
