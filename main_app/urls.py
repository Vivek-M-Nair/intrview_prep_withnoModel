from django.urls import path
from . import views
urlpatterns=[
    path('home/',views.home,name='home'),
    path('log_reg/',views.log_reg,name='log_reg'),
    path('summary/',views.summary,name='summary'),
    path('logout_view/',views.logout_view,name="logout_view"),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('get_job_description/',views.get_job_description,name='get_job_description'),
    path('generate_question/',views.generate_question,name='generate_question'),
    path('generateFeed_ans/',views.generateFeed_ans,name="generateFeed_ans"),
    path('AI_answer/',views.AI_answer,name="AI_answer"),
    path('Next_question/',views.Next_question,name="Next_question")
]