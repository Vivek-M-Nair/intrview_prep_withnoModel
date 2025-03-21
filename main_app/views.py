from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import contact
from transformers import pipeline
from .forms import Job_details
from .forms import AnsForm  
from .models import Job 
import json      
from django.contrib.auth.decorators import login_required 
from .models import Interviewprep   
import random 
from .models import Personality 
from django.http import JsonResponse                            

# from django.http import HttpResponse

# def summary(request):
#     if request.user.is_authenticated:
#        return render(request,'summary.html')
#     else:
#        messages.error(request,'please login first !')
#        return redirect('log_reg')
        
def log_reg(request):
    # login validation
    context={}
    if request.method=="POST":
        if request.POST.get('form_type')=='login_type':
            username=request.POST.get('username')
            password=request.POST.get('password')
            
            user=authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                # messages.success(request,'login successfull')
                return redirect('home')
            else:
                messages.error(request,'Invalid username or password !')

        elif request.POST.get('form_type')=='register_type':
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('password')

            if not username or not email or not password:
                messages.error(request,'please fill all fields !')
            elif User.objects.filter(username=username).exists():
                messages.error(request,'username already exists !')
                context['form_type']='register_type'
                return render(request,'log_reg.html',context)
            else:
                user=User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request,'Account successfully created !')
                return redirect('log_reg')

    return render(request,'log_reg.html')

def logout_view(request):
    logout(request)
    messages.success(request,'successfully Logout ! Please Login')
    return redirect('log_reg')
# Create your views here.
#contact
def contact_us(request):
    context={}
    if request.method=="POST":
      if request.user.is_authenticated:
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        country=request.POST.get('country')
        subject=request.POST.get('subject')
        if not firstname or not lastname or not country or not subject:
            messages.error(request,'please enter all fields')
            context['field_missing']='missing'
            return render(request,'home.html',context)
        else:
            cont=contact.objects.create(first_name=firstname, last_name=lastname, country=country, subject=subject)
            cont.save()
            messages.success(request,"Message have been send ,Thank You !")
            return redirect('home')
      else:
        messages.error(request,'please logiin first')
        return redirect('log_reg')
    return render(request,'home.html')



question_generator=pipeline('text2text-generation',model="google/flan-t5-large")
answer_generator=pipeline('text2text-generation',model="google/flan-t5-large")
feedback=pipeline('text-classification',model="distilbert-base-uncased-finetuned-sst-2-english")
personality_analsor=pipeline('text-classification',model="google/flan-t5-large")

@login_required
def home(request):
    # context={}
    AnsFormm=AnsForm()
    Job_detailss=Job_details()
    # if request.user.is_authenticated:
    #     context['loged_in']=True
    #     return render(request,'home.html',context)
    Finals=None
    user=request.user
    # quesion generation
    if request.method=="POST":
       action = request.POST.get('action')
    #   if action in ['Generate_question']:
    #     Job_detailss=Job_details(request.POST)
    #     if Job_detailss.is_valid():
    #       domain=Job_detailss.cleaned_data['domain']
    #       job_description=Job_detailss.cleaned_data['description']
    #       request.session['domain']=domain
    #       request.session['job_description']=job_description
    #       prompt=f"Generate a technical interview question for a {domain} role.The involves:{job_description}"
    #       question_output=question_generator(prompt,max_length=50,temperature=0.7,do_sample=True,top_p=0.9,num_return_sequences=1)[0]['generated_text']
    #       Finals=Interviewprep.objects.create(user=user,domain=domain,description=job_description,question=question_output)
    #       Finals.save()
    #     return JsonResponse({"question":Finals.question if Finals is not None else ''})

       if action =="submit_for_AI":
         Finals_id=request.POST.get('practice_id')
         Finals=get_object_or_404(Interviewprep,id=Finals_id)
         AnsFormm=AnsForm(request.POST,instance=Finals)
         if AnsFormm.is_valid():
            Finals.user_ans=AnsFormm.cleaned_data['user_ans']
            Finals.save()
            feedback_output=feedback(Finals.user_ans)[0]
            label,score=feedback_output['label'],feedback_output['score']
            feedback_Ans="😀Excellent Answer,Keep going🥳."if label=="POSITIVE" and score > 0.90 else \
                         "(●'◡'●)Good Answer,but need some improvement" if label=="POSITIVE" and score >0.75 else\
                         "⚠Need Improvement,Keep practicing."
            Finals.feedback=feedback_Ans

         if not Finals.suggested_answer:
            prompt=f"provide a structured answer for the interview question:{Finals.question} based on {Finals.description}"
            suggested_ans=answer_generator(prompt,max_length=500,top_p=0.9,temperature=0.7,top_k=50,num_return_sequences=1)[0]['generated_text']
            Finals.suggested_answer=suggested_ans
         Finals.save()

       elif action =="suggested_answer":
         Finals_id=request.POST.get('practice_id')
         Finals=get_object_or_404(Interviewprep,id=Finals_id)  
         if not Finals.suggested_answer:
            prompt=f"provide a structured answer for the interview question:{Finals.question} based on {Finals.description}"
            suggested_ans=answer_generator(prompt,max_length=500,top_p=0.9,temperature=0.7,num_return_sequences=1)[0]['generated_text']
            Finals.suggested_answer=suggested_ans
         Finals.save()

       elif action=="next_qn":
         domain=request.session['domain']
         job_description=request.session['job_description']
         prompt=f"Generate a technical interview question for a {domain} role.The involves:{job_description}"
         question_output=question_generator(prompt,max_length=50,temperature=0.7,do_sample=True,top_p=0.9,num_return_sequences=1)[0]['generated_text']
         Finals=Interviewprep.objects.create(user=user,domain=domain,description=job_description,question=question_output)
         Finals.save()
         
        


    return render(request,'home.html',{'AnsForm':AnsFormm,'Job_details':Job_detailss,'loged_in':user,
                                    #    'question':Finals.question if Finals is not None else '',
                                       "practice_id":Finals.id if Finals is not None else '',
                                       "feedback":Finals.feedback if Finals is not None else '',
                                       "Suggested_ans":Finals.suggested_answer if Finals is not None else ''})


# get job_description
def get_job_description(request):
    domain=request.GET.get('domain')
    if domain:
        # try:
         job=Job.objects.get(job_title=domain)
         return JsonResponse({'job_description':job.job_description})
    #     except:
    #      return JsonResponse({'error':"no description found"},status=404 )   
    # else:
    #     return JsonResponse({'error':'no domain provided'},status=400)



#personality analysis
def summary(request):
   user=request.user
   sum=Interviewprep.objects.filter(user=user).values("created_at","question","user_ans","feedback","suggested_answer")
   summary_list=list(sum)
   for item in summary_list:
       if item['created_at']:
           item['created_at']=item['created_at'].strftime("%Y-%m-%d %H-%M-%S")
       else:
           item['created_at']=""
           
# #    summary
#    summary_data = Interviewprep.objects.filter(user=request.user).values(
#         "id", "created_at", "question", "user_ans", "suggested_answer"
#     )
#    summary_list = list(summary_data)

#     # Convert datetime fields to strings
#    for item in summary_list:
#         if item["created_at"]:
#             item["created_at"] = item["created_at"].strftime("%Y-%m-%d %H:%M:%S")
#         else:
#             item["created_at"] = ""


# personality
   interviewpractice=Interviewprep.objects.filter(user=user,user_ans__isnull=False)
   if not interviewpractice:
       messages.error(request,"sorry,No response available")
       return redirect('home')
   
   traits={
        "openness":50,
        "conscientiousness":50,
        "extraversion":50,
        "agreeableness":50,
        "neuroticism":50
   }
   for response in interviewpractice:
      answer=response.user_ans.lower()
      sentiment=personality_analsor(answer)[0]

      if any(words in answer for words in["creative","innovative","imaginative","visionary","inventive","artistic"]):
         traits['openness'] += random.randint(5,10)
      if any(words in answer for words in ["organized","structured","methodical","systematic","precise","detail-oriented","thorough"]):
         traits['conscientiousness']  += random.randint(5,10)  
      if any(word in answer for word in ["sociable","outgoing","friendly","talkative","gregarious","approachable","carismatic"]):
            traits['extraversion'] += random.randint(5,10)
      if any(word in answer for word in ["kind","caring","compassionate","warm","gentle","generous","nurturing"]):
            traits['agreeableness'] += random.randint(5,10)
      if sentiment['label']=="NEGATIVE":
            traits['neuroticism']=random.randint(5,10)
        
   for key in traits:
       traits[key]=max(0,min(traits[key],100))

   personality,created=Personality.objects.update_or_create(
       user=user,
       defaults=traits
   )

   return render(request,'summary.html',{"personality":json.dumps(traits),"summary_list":summary_list})
 
from django.http import JsonResponse
from .models import Interviewprep
from .forms import Job_details


def generate_question(request):
    if request.method == "POST":
        
        Job_detailss = Job_details(request.POST)
        if not Job_detailss.is_valid():
               print("Form Errors:", Job_detailss.errors)  # Debugging
               return JsonResponse({'error': 'Invalid form data'}, status=400)
        # Rest of your logic...

        domain = Job_detailss.cleaned_data['domain']
        job_description = Job_detailss.cleaned_data['description']
        request.session['domain'] = domain
        request.session['job_description'] = job_description
                
                # Generate question
        prompt = f"Generate a technical interview question for a {domain} role. The job involves: {job_description}"
        question_output = question_generator(
                        prompt, 
                        max_length=50, 
                        temperature=0.7, 
                        do_sample=True, 
                        top_p=0.9, 
                        num_return_sequences=1
                    )[0]['generated_text']
       
                # Save to database
        Finals = Interviewprep.objects.create(
                    user=request.user, 
                    domain=domain, 
                    description=job_description, 
                    question=question_output
                )
        Finals.save()
                
        return JsonResponse({"question": Finals.question,"practice_id":Finals.id if Finals is not None else ''})


def generateFeed_ans(request):
    if request.method=="POST":
         Finals_id=request.POST.get('practice_id')
         Finals=get_object_or_404(Interviewprep,id=Finals_id)
         AnsFormm=AnsForm(request.POST,instance=Finals)
         if AnsFormm.is_valid():
            Finals.user_ans=AnsFormm.cleaned_data['user_ans']
            Finals.save()
            
            feedback_output=feedback(Finals.user_ans)[0]
            label,score=feedback_output['label'],feedback_output['score']
            feedback_Ans="😀Excellent Answer,Keep going🥳."if label=="POSITIVE" and score > 0.90 else \
                         "(●'◡'●)Good Answer,but need some improvement" if label=="POSITIVE" and score >0.75 else\
                         "⚠Need Improvement,Keep practicing."
            Finals.feedback=feedback_Ans

         if not Finals.suggested_answer:
            prompt=f"provide a structured answer for the interview question:{Finals.question} based on {Finals.description}"
            suggested_ans=answer_generator(prompt,max_length=500,top_p=0.9,temperature=0.7,top_k=50,num_return_sequences=1)[0]['generated_text']
            Finals.suggested_answer=suggested_ans
         Finals.save()
         return JsonResponse({"feedback":Finals.feedback,"Suggested_ans":Finals.suggested_answer} )


def AI_answer(request):
   if request.method=="POST":
     Finals_id=request.POST.get('practice_id')
     Finals=get_object_or_404(Interviewprep,id=Finals_id)  
     if not Finals.suggested_answer:
            prompt=f"provide a structured answer for the interview question:{Finals.question} based on {Finals.description}"
            suggested_ans=answer_generator(prompt,max_length=500,top_p=0.9,temperature=0.7,num_return_sequences=1)[0]['generated_text']
            Finals.suggested_answer=suggested_ans
     Finals.save()
     return JsonResponse({"Suggested_ans":Finals.suggested_answer})


def Next_question(request):   
    if request.method=="POST":
         domain=request.session['domain']
         job_description=request.session['job_description']
         prompt=f"Generate a technical interview question for a {domain} role.The involves:{job_description}"
         question_output=question_generator(prompt,max_length=50,temperature=0.7,do_sample=True,top_p=0.9,num_return_sequences=1)[0]['generated_text']
         Finals=Interviewprep.objects.create(user=request.user,domain=domain,description=job_description,question=question_output)
         Finals.save()
         return JsonResponse({"question": Finals.question,"practice_id":Finals.id if Finals is not None else ''})

         
        