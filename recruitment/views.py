from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import JobApplication, Job
import pdfplumber
import docx
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')


# Home Page
def home(request):
    return render(request, 'home_page.html')

def post_job(request):
    return render(request, 'job_post.html')



# Job Posting Page
def create_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        skills = request.POST.get('skills')

        if not (title and description and skills):
            messages.error(request, "All fields are required!")
            return redirect('create_job')

        Job.objects.create(title=title, description=description, required_skills=skills)
        messages.success(request, "Job posted successfully!")
        return redirect('home')  # Redirect to home after posting a job

    return render(request, 'create_job.html')


# Job Detail Page
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job.html', {'job': job})



# Extract Text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text



# Extract Text from Word Document
def extract_text_from_word(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


# Fetch Required Skills for a Job
def get_latest_job_skills(job_id):
    job = Job.objects.filter(id=job_id).first()
    if job and job.required_skills:
        return set(job.required_skills.lower().split(", "))
    return set()


# Upload CV and Process Candidate
@csrf_exempt
def upload_cv(request):
    if request.method == 'POST':
        job_id = request.POST.get('job')
        name = request.POST.get('name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        cv_file = request.FILES.get('cv')

        if not (job_id and name and email and gender and cv_file):
            messages.error(request, "All fields are required!")
            return redirect('recruitment_dashboard')

        # Save CV
        fs = FileSystemStorage(location='media/cvs/')
        filename = fs.save(cv_file.name, cv_file)
        file_path = fs.url(filename)  # Correct file path format


        # Extract Text from CV
        if filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            extracted_text = extract_text_from_word(file_path)
        else:
            messages.error(request, "Invalid file format. Only PDF/DOCX allowed.")
            return redirect('recruitment_dashboard')

        # Tokenization & Cleaning
        tokens = word_tokenize(extracted_text.lower())
        tokens = [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]

        # Fetch Required Skills
        required_skills = get_latest_job_skills(job_id)
        if not required_skills:
            messages.error(request, "No skills found for this job. Please post a job first.")
            return redirect('recruitment_dashboard')

        # Calculate Match Percentage
        matched_skills = required_skills.intersection(set(tokens))
        match_percentage = (len(matched_skills) / len(required_skills)) * 100 if required_skills else 0

        # Categorize Candidate
        if match_percentage >= 65:
            status = "Shortlisted"
        elif 55 <= match_percentage < 65:
            status = "Waiting List"
        else:
            status = "Rejected"
        
        # Save Application
        JobApplication.objects.create(
            name=name,
            email=email,
            gender=gender,
            job = get_object_or_404(Job, id=job_id),
 
            cv=file_path,
            matched_skills=", ".join(matched_skills),
            match_percentage=match_percentage,
            status=status
        )
           

        messages.success(request, f"Application submitted successfully! Status: {status}")
        return redirect('home')

    return render(request, 'job_recruitment.html')


# Fetch Jobs & Shortlisted Candidates Count
def job_list(request):
    jobs = Job.objects.all()
    job_data = []

    for job in jobs:
        shortlisted_count = JobApplication.objects.filter(job=job, status="Shortlisted").count()
        waiting_count = JobApplication.objects.filter(job=job, status="Waiting List").count()
        rejected_count = JobApplication.objects.filter(job=job, status="Rejected").count()

        job_data.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "required_skills": job.required_skills,
            "shortlist_count": shortlisted_count,
            "waiting_count": waiting_count,
            "rejected_count": rejected_count
        })

    return render(request,'job.html',{"jobs": job_data})  # Returning as JSON for frontend

# Recruitment Dashboard
def recruitment_dashboard(request):
    jobs = Job.objects.all()  # Fix: Added ()
    return render(request, 'job_recruitment.html', {'jobs': jobs})





from django.shortcuts import render, get_object_or_404
from .models import Job, JobApplication

def job_candidates(request, job_id, status):
    job = get_object_or_404(Job, id=job_id)  # Fetch the job
    candidates = JobApplication.objects.filter(job=job, status=status)  # Filter candidates
    
    return render(request, "candidates.html", {"job": job, "candidates": candidates, "status": status})
