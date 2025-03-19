from django.db import models
from django.contrib.auth.models import User
class contact(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    country=models.CharField(max_length=100)
    subject=models.TextField()

#job_deails table
class Job(models.Model):
    job_title=models.CharField(max_length=50)
    job_description=models.TextField()

#interview practiced data table
class Interviewprep(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    domain=models.CharField(max_length=50)
    description=models.TextField()
    question=models.TextField()
    user_ans=models.TextField()
    feedback=models.TextField()
    suggested_answer=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
# Create your models here.

# personality analysis table
class Personality(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    openness=models.IntegerField()
    conscientiousness=models.IntegerField()
    extraversion=models.IntegerField()
    agreeableness=models.IntegerField()
    neuroticism=models.IntegerField()


