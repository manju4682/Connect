from django.urls import path

from . import views

urlpatterns=[
     path('alportal',views.AlPortal, name='AlPortal'),
     path('stportal',views.StPortal, name='StPortal'),
     path('offers',views.offers, name='Offers'),
      path('activity',views.AddActivity, name='Offers'),
      path('vacancies',views.vacancies, name='vacancies'),
     path('activities',views.activities, name='activities'),
     path('apply',views.apply, name='apply'),
     path('pdf',views.pdf_request, name='pdf_request'),
     path('info',views.std_pdf_request, name='std_pdf_request'),
     path('analysis',views.analysis, name='analysis'),
     path('personalise',views.personalise, name='personalise'),
     ]
