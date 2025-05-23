# Generated by Django 4.2 on 2025-04-17 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('required_skills', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('cv', models.FileField(upload_to='cvs/')),
                ('matched_skills', models.TextField(blank=True, null=True)),
                ('match_percentage', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('Shortlisted', 'Shortlisted'), ('Waiting List', 'Waiting List'), ('Rejected', 'Rejected')], default='Pending', max_length=50)),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recruitment.job')),
            ],
        ),
        migrations.CreateModel(
            name='WaitingListCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cv', models.FileField(upload_to='cvs/')),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recruitment.job')),
                ('job_application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recruitment.jobapplication')),
            ],
        ),
        migrations.CreateModel(
            name='ShortlistedCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cv', models.FileField(upload_to='cvs/')),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recruitment.job')),
                ('job_application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recruitment.jobapplication')),
            ],
        ),
        migrations.CreateModel(
            name='RejectedCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cv', models.FileField(upload_to='cvs/')),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recruitment.job')),
                ('job_application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recruitment.jobapplication')),
            ],
        ),
    ]
