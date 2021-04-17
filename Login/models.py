from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=10)
    website = models.URLField(max_length=100)
    type = models.CharField(max_length=15)
    desc = models.TextField()
    no_of_alumni = models.IntegerField(default=0)

class Branch(models.Model):
    name = models.CharField(max_length=20)
    branch_hod = models.CharField(max_length=20)
    contact_no = models.CharField(max_length=14)
    mail_id = models.EmailField(max_length=30,default='@gamil.com')

class Alumni(models.Model):
    id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=15)
    gender = models.CharField(max_length=1,default="M")
    year_of_grad = models.IntegerField(default=2018)
    branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    mail_id = models.EmailField(max_length=30,default='@gmail.com')
    work_expirience = models.IntegerField(default=2)

class Student(models.Model):
    id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=15)
    gender = models.CharField(max_length=1)
    year_of_grad = models.IntegerField( default=2018)
    branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE)
    mail_id = models.EmailField(max_length=30,default='@gmail.com')
