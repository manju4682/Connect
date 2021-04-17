from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from Login.models import Branch,Company,Alumni,Student
from .models import Vacancies,Activity,Applied_status
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
import datetime
from datetime import date
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import itertools

from django.views.decorators.csrf import csrf_protect

@csrf_protect
def AlPortal(request):
    l = Company.objects.values('name','id')
    return render(request,'alumini_form.html',{'companies':l})

def offers(request):
    if request.method=='POST':
        role = request.POST.get('role','')
        link = request.POST.get('link','')
        pack = request.POST.get('pack','')
        location = request.POST.get('location','')
        vac = request.POST.get('vac','')
        branch_allowed = request.POST.get('branch','')
        company = request.POST.get('company','')
        date = request.POST.get('date','')
        vacancy = Vacancies(role = role,link = link,package = pack,last_date_apply = date,location=location,no_of_vacancies=vac, type_of_branch=branch_allowed)
        vacancy.company_id = Company.objects.filter(id=company).first()
        try:
            vacancy.al_id = Alumni.objects.filter(id=request.user.id).first()
            vacancy.save()
            print("Job added")
            messages.info(request,"Job added successfully!")
            return HttpResponseRedirect("/alportal")
        except:
            messages.info(request,"You have to be logged in as an Alumni to add a job vacancy!")
            return HttpResponseRedirect("/alportal")


def StPortal(request):
    return render(request,'student_form.html');

def AddActivity(request):
    if request.method=='POST':
        club_name = request.POST.get('club_name','')
        name = request.POST.get('type','')
        time = request.POST.get('time','')
        contact = request.POST.get('contact_details','')

        act = Activity(club_name = club_name,Type = name, Date_of_event=time, contact_no=contact)
        try:
            act.std_id = Student.objects.filter(id=request.user.id).first()
            act.save()
            print("Activity added")
            messages.info(request,"Activity added successfully!")
            return HttpResponseRedirect("/stportal")
        except:
            messages.info(request,"You have to be logged in as a Student to add an activity!")
            return HttpResponseRedirect("/stportal")

def vacancies(request):
    if request.user.id == None:
        return HttpResponseRedirect("/login")
    else:
        li = Vacancies.objects.values('job_id','role','link','package','last_date_apply','location','no_of_vacancies','type_of_branch','no_of_applications','company_id')
        usr_id = Student.objects.filter(id=request.user.id).first()
        admin = User.objects.filter(id=request.user.id).values('is_staff').first()
        if admin['is_staff']:
            is_admin = 1
        else:
            is_admin = 0
        print(is_admin)
        if usr_id is None:
            value = 0
        else:
            value = 1
        print(value)
        status = Applied_status.objects.filter(std_id=usr_id).values('job_id')
        jobs = []
        current = []
        companies = []
        for no in status:
            jobs.append(no['job_id'])
        for l in li:
            if l['job_id'] in jobs or l['last_date_apply'] < date.today():
                continue
            else:
                companies.append(Company.objects.filter(id=l['company_id']).values('name').first())
                current.append(l)
        roles_list = []
        locations_list = []
        for vac in li:
            if vac['role'] in roles_list:
                pass
            else:
                roles_list.append(vac['role'])
            if vac['location'] in locations_list:
                pass
            else:
                locations_list.append(vac['location'])

        print(roles_list)
        print(locations_list)

        return render(request,'vacancy_table.html',{'vacancies':zip(current,companies),'value':value,'is_admin':is_admin,'roles':roles_list,'locations':locations_list,'personalised':1});

def activities(request):
    if request.user.id == None:
        return HttpResponseRedirect("/login")
    else:
        li = Activity.objects.values('club_name','Type','Date_of_event','contact_no')
        print(li)
        return render(request,'activities_table.html',{'Activities':li});

def apply(request):
    if request.method=='POST':
        jobid = request.POST.get('id','')
        job =  Vacancies.objects.filter(job_id=jobid).first()
        stat = Applied_status(Date_applied=datetime.date.today())
        stat.job_id = job
        stat.std_id = Student.objects.filter(id=request.user.id).first()
        stat.save()
        print("status saved!")
        return HttpResponseRedirect("/vacancies")
    else:
        return HttpResponseRedirect("/")

def pdf_request(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="applications_info.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    # container for the 'Flowable' objects
    elements = []
    data = []
    all_applications = Applied_status.objects.values('job_id','std_id')
    print(all_applications)
    cnt = 1
    l = ["Sr.No","Name","Role","Company","Location"]
    data.append(l)
    for appl in all_applications:
        students = []
        students.append(cnt)
        students.append(Student.objects.filter(id=appl['std_id']).values('name').first()['name'])
        students.append(Vacancies.objects.filter(job_id=appl['job_id']).values('role').first()['role'])
        comp = Vacancies.objects.filter(job_id=appl['job_id']).values('company_id').first()
        students.append(Company.objects.filter(id=comp['company_id']).values('name').first()['name'])
        students.append(Vacancies.objects.filter(job_id=appl['job_id']).values('location').first()['location'])
        data.append(students)
        cnt = cnt+1

    t=Table(data,5*[1.6*inch], cnt*[0.6*inch])
    t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('BACKGROUND', (0, 0), (4, 0), colors.lightgrey),
    ('TEXTFONT', (0, 1), (-1, 1), 'Times-Bold'),
    ('FONTSIZE', (0, 0), (4, 0), 16),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTSIZE', (0, 1), (-1, -1), 14),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))

    elements.append(t)
    # write the document to dis
    doc.build(elements)



    return response

def std_pdf_request(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="info.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    # container for the 'Flowable' objects
    elements = []
    data = []
    all_applications = Applied_status.objects.filter(std_id=request.user.id).values('job_id','std_id')
    print(all_applications)
    cnt = 1
    l = ["Sr.No","Role","Company","Location"]
    data.append(l)
    for appl in all_applications:
        students = []
        students.append(cnt)
        students.append(Vacancies.objects.filter(job_id=appl['job_id']).values('role').first()['role'])
        comp = Vacancies.objects.filter(job_id=appl['job_id']).values('company_id').first()
        students.append(Company.objects.filter(id=comp['company_id']).values('name').first()['name'])
        students.append(Vacancies.objects.filter(job_id=appl['job_id']).values('location').first()['location'])
        data.append(students)
        cnt = cnt+1

    if cnt==1:
        messages.info(request,"You have not applied to any jobs!")
        return HttpResponseRedirect("/profile")

    else:
        t=Table(data,4*[1.6*inch], cnt*[0.6*inch])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('BACKGROUND', (0, 0), (4, 0), colors.lightgrey),
        ('TEXTFONT', (0, 1), (-1, 1), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (4, 0), 16),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 1), (-1, -1), 14),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))

        elements.append(t)
    # write the document to dis
        doc.build(elements)

        return response

def analysis(request):
    all_applications = Applied_status.objects.values('job_id','std_id')
    location = {}
    role = {}
    l = []
    li = []
    for appl in all_applications:
        rol = Vacancies.objects.filter(job_id=appl['job_id']).values('role').first()['role']
        loc = Vacancies.objects.filter(job_id=appl['job_id']).values('location').first()['location']
        location[loc] = location.get(loc,1) + 1
        role[rol] = role.get(rol,1) + 1
    for key,item in location.items():
        l.append({'city':key,'count':item})
    for key,item in role.items():
        li.append({'role':key,'count':item})

    print(location)
    print(role)
    print(l)
    print(li)
    return render(request,'analysis.html',{'location':l,'role':li})

def personalise(request):
    if request.method == 'POST':
        role = request.POST.get('role','')
        location = request.POST.get('location','')
        print(role)
        print(location)
        l1 = Vacancies.objects.filter(role=role,location=location).values('job_id','role','link','package','last_date_apply','location','no_of_vacancies','type_of_branch','no_of_applications','company_id')
        l2 = Vacancies.objects.filter(role=role).values('job_id','role','link','package','last_date_apply','location','no_of_vacancies','type_of_branch','no_of_applications','company_id')
        l3 = Vacancies.objects.filter(location=location).values('job_id','role','link','package','last_date_apply','location','no_of_vacancies','type_of_branch','no_of_applications','company_id')
        l4 = Vacancies.objects.values('job_id','role','link','package','last_date_apply','location','no_of_vacancies','type_of_branch','no_of_applications','company_id')
        usr_id = Student.objects.filter(id=request.user.id).first()
        admin = User.objects.filter(id=request.user.id).values('is_staff').first()
        if admin['is_staff']:
            is_admin = 1
        else:
            is_admin = 0
        print(is_admin)
        if usr_id is None:
            value = 0
        else:
            value = 1
        print(value)
        status = Applied_status.objects.filter(std_id=usr_id).values('job_id')
        jobs = []
        current = []
        companies = []
        for no in status:
            jobs.append(no['job_id'])

        for lis in itertools.chain(l1,l2,l3,l4):
            if lis['job_id'] in jobs or lis['last_date_apply'] < date.today():
                continue
            else:
                companies.append(Company.objects.filter(id=lis['company_id']).values('name').first())
                current.append(lis)
                jobs.append(lis['job_id'])
        print(current)
        return render(request,'vacancy_table.html',{'vacancies':zip(current,companies),'value':value,'is_admin':is_admin,'personalised':0});
