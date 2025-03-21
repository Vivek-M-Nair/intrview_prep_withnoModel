from django import forms
from .models import Job
from .models import Interviewprep

#Job Feild and description form
class Job_details(forms.ModelForm):
    domain=forms.ChoiceField(choices=[('','Select a Field')]+[(job.job_title,job.job_title) for job in Job.objects.all()],
           widget=forms.Select(attrs={'class':'Job_title'})
    )
    class Meta:
        model=Interviewprep
        fields=['domain','description']
        widgets={
            'description':forms.Textarea(attrs={'class':'job_description','placeholder':"Your Selected Feild's description here "})
        }
    
#form for Answer
class AnsForm(forms.ModelForm):
    class Meta:
        model=Interviewprep
        fields=['user_ans']
    user_ans=forms.CharField(required=True,widget=forms.Textarea(attrs={'placeholder':'Enter your answer','name':'user_ans'}))