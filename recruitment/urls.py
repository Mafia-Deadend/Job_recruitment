from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post-job/', views.post_job, name='post_job'),
    path('create-job/', views.create_job, name='create_job'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('recruitment-dashboard/', views.recruitment_dashboard, name='recruitment_dashboard'),
    path('upload-cv/', views.upload_cv, name='upload_cv'),
    path('jobs/', views.job_list, name='job_list'),  # Fetch jobs (Ensure Correct Mapping)
]
