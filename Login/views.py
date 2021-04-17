from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Branch,Company,Alumni,Student
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
# Create your views here.

def home(request):
    return render(request,'index.html')

@csrf_protect
def Login(request):
    if request.method == 'POST':
        usrname = request.POST.get('username')
        password = request.POST.get('pass')
        print(usrname+" "+password)
        user = authenticate(username=usrname, password=password)

        if user is not None:
            print(usrname+" "+password)
            auth.login(request, user)
            print("logged in")
            return HttpResponseRedirect("/")
        else:
            print("No")
            messages.info(request,"Inavalid credentials!")
            return HttpResponseRedirect("/login")
    else:
        return render(request,'login.html')

def Register(request):

    li = Branch.objects.values('name','id')
    l = Company.objects.values('name','id')


    return render(request,'form.html',{'branches':li,'companies':l})

def AlRegister(request):
    if request.method == "POST":
        name1 = request.POST.get('name','')
        gender = request.POST.get('gender','')
        year_of_grad = request.POST.get('graduation','')
        mail = request.POST.get('email','')
        experience = request.POST.get('xperience','')
        branch = request.POST.get('branch','')
        company = request.POST.get('company','')
        pswd1 = request.POST.get('psw','')
        pswd2 = request.POST.get('re_psw','')

        if pswd1 == pswd2:
            if User.objects.filter(email=mail).exists():

                messages.info(request, "Email ID is already registered!")
                return HttpResponseRedirect("/register")
            else:
                usr = User.objects.create_user(username=mail,first_name=name1,email=mail,password=pswd1)
                usr.save()
                ppl = Alumni(name=name1,gender=gender,year_of_grad=year_of_grad,work_expirience=experience,mail_id=mail)
                ppl.id=usr
                ppl.branch_id = Branch.objects.filter(id=branch).first()
                ppl.company_id = Company.objects.filter(id=company).first()
                ppl.save()
                print("User created")
                return HttpResponseRedirect("/login")
        else:
            messages.info(request, "Passwords do not match!")
            return HttpResponseRedirect("/register")
    else:
        return render(request,'register.html')

def StRegister(request):
    if request.method == "POST":
        name1 = request.POST.get('name','')
        gender = request.POST.get('gender','')
        year_of_grad = request.POST.get('graduation','')
        mail = request.POST.get('email','')
        branch = request.POST.get('branch','')
        pswd1 = request.POST.get('psw','')
        pswd2 = request.POST.get('re_psw','')

        if pswd1 == pswd2:
            if User.objects.filter(email=mail).exists():

                messages.info(request, "Email ID is already registered!")
                return HttpResponseRedirect("/register")
            else:
                usr = User.objects.create_user(username=mail,first_name=name1,email=mail,password=pswd1)
                usr.save()
                ppl = Student(name=name1,gender=gender,year_of_grad=year_of_grad,mail_id=mail)
                ppl.id=usr
                ppl.branch_id = Branch.objects.filter(id=branch).first()
                ppl.save()
                print("User created")
                return HttpResponseRedirect("/login")
        else:
            messages.info(request, "Passwords do not match!")
            return HttpResponseRedirect("/register")
    else:
        return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def profile(request):
    if request.user.id == None:
        return HttpResponseRedirect("/login")
    else:
        std = Student.objects.filter(id = request.user.id).values().first()
        alm = Alumni.objects.filter(id = request.user.id).values().first()
        if alm is None:
            dept = Branch.objects.filter(id = std['branch_id_id']).values('name').first()
            std['branch_name'] = dept['name']

        else:
            dept = Branch.objects.filter(id = alm['branch_id_id']).values('name').first()
            comp = Company.objects.filter(id = alm['company_id_id']).values('name').first()
            alm['branch_name'] = dept['name']
            alm['company_name'] = comp['name']
        print(alm)

        return render(request,'profile.html',{'alm':alm,'std':std})

def delete(request):
    User.objects.filter(id=request.user.id).delete()
    auth.logout(request)
    return HttpResponseRedirect("/")
