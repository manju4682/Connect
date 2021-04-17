from django.urls import path

from . import views

urlpatterns=[
     path('',views.home, name='Login'),
     path('login',views.Login, name='log'),
      path('register',views.Register, name='log'),
      path('alregister',views.AlRegister, name='log'),
      path('stregister',views.StRegister, name='log'),
      path('logout',views.logout, name='log'),
      path('profile',views.profile, name='profile'),
      path('delete',views.delete, name='delete'),
]
