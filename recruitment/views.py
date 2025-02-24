from django.shortcuts import render

def home(request):
    return render(request, 'home_page.html')

def post_job(request):
    return render(request, 'job_post.html')

def create_job(request):
    return render(request, 'create_job.html')

def job_detail(request, job_id):
    return render(request, 'job.html', {'job_id': job_id})

def recruitment_dashboard(request):
    return render(request, 'job_recruitment.html')


import pdfplumber
import docx
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import JobApplication, Job

nltk.download('punkt')
nltk.download('stopwords')

# Extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Extract text from Word
def extract_text_from_word(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Fetch latest job skills from database
def get_latest_job_skills():
    latest_job = Job.objects.last()
    if latest_job and latest_job.required_skills:
        return set(latest_job.required_skills.lower().split(", "))
    return set()

# Upload CV and process
@csrf_exempt
def upload_cv(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        cv_file = request.FILES.get('cv')

        if not cv_file:
            return render(request, 'job_recruitment.html', {'error': 'No file uploaded'})

        # Save CV
        fs = FileSystemStorage(location='media/cvs/')
        filename = fs.save(cv_file.name, cv_file)
        file_path = f"media/cvs/{filename}"

        # Extract text from CV
        if filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            extracted_text = extract_text_from_word(file_path)
        else:
            return render(request, 'job_recruitment.html', {'error': 'Invalid file format. Only PDF/DOCX allowed.'})

        # Tokenization and cleaning
        tokens = word_tokenize(extracted_text.lower())
        tokens = [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]

        # Fetch required skills
        required_skills = get_latest_job_skills()
        if not required_skills:
            return render(request, 'job_recruitment.html', {'error': 'No job skills found! Please post a job first.'})

        # Check skill match percentage
        matched_skills = required_skills.intersection(set(tokens))
        match_percentage = (len(matched_skills) / len(required_skills)) * 100 if required_skills else 0

        # Categorize candidate
        if match_percentage >= 65:
            status = "Shortlisted"
        elif 55 <= match_percentage < 65:
            status = "Waiting List"
        else:
            status = "Rejected"

        # Save in database
        JobApplication.objects.create(
            name=name,
            email=email,
            gender=gender,
            cv=file_path,  # Store relative path
            matched_skills=", ".join(matched_skills),
            match_percentage=match_percentage,
            status=status
        )

        return redirect('home')  # Redirect after processing

    return render(request, 'job_recruitment.html')

# Fetch job list

 # Returns jobs in JSON format
def job_list(request):
    jobs = Job.objects.all
    short_list = JobApplication.status
    return render(request, 'job_list.html', {'jobs': jobs,'short_list':short_list},)
