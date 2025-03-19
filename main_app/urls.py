from django.urls import path
from . import views
urlpatterns=[
    path('home/',views.home,name='home'),
    path('log_reg/',views.log_reg,name='log_reg'),
    path('summary/',views.summary,name='summary'),
    path('logout_view/',views.logout_view,name="logout_view"),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('get_job_description/',views.get_job_description,name='get_job_description')
]