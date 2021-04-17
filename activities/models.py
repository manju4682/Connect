from django.db import models
from django.contrib.auth.models import User
from Login.models import Company, Branch, Alumni, Student
# Create your models here.

class Activity(models.Model):
    club_name = models.CharField(max_length=15)
    Type = models.CharField(max_length=15)
    Date_of_event = models.DateTimeField()
    std_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=12)

class Vacancies(models.Model):
    job_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=40)
    link = models.URLField(max_length=100,default="www.jssstuniv.in")
    package = models.CharField(max_length=20)
    last_date_apply = models.DateField()
    location = models.CharField(max_length=15)
    no_of_vacancies = models.IntegerField(default=1)
    type_of_branch = models.CharField(max_length=10)
    no_of_applications = models.IntegerField(default=0)
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    al_id = models.ForeignKey(Alumni,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('job_id' , 'company_id')

class Applied_status(models.Model):
    job_id = models.ForeignKey(Vacancies,on_delete=models.CASCADE)
    std_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    Date_applied = models.DateField(auto_now=True)
