from django.db.models.aggregates import Avg, Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Drug, Prescribeslink, Prescriber, Person, PrescriberCredential, Credential

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, query
import psycopg2 as psy

# Create your views here.
def showLandingPageView(request) :
    return render(request, 'NOIC_app/landingPage.html')

def showLoginPageView(request) :
    return render(request, 'NOIC_app/login.html')

def showPrescriberPageView(request) :
    data = Drug.objects.all()
    prescribe = Prescriber.objects.all()[0:10]
    credentials = PrescriberCredential.objects.all()[0:10]
    # print(prescribe.query)
    # print(credentials.query)

    if request.method == "POST": 

        first_name1 = request.POST['fname']
        last_name1 = request.POST['lname']
        gend = request.POST['gender1']
        state1 = request.POST['state1']
        creds = request.POST['creds']
        specialty1 = request.POST['specialty1']

        conn = psy.connect(host="noic-server.postgres.database.azure.com", port= 5432, database='noic', user='noic', password='INTEX2021*')
        cur = conn.cursor()

        a= 'select * from prescriber inner join person on prescriber.prescriber_id = person.person_id inner join prescriber_credential on prescriber_credential.npi = prescriber.npi where'


        
        if first_name1 != '' :
            a += ' first_name like ' + "'" + first_name1 + "'"

        if last_name1 != '' and first_name1 != '':
            a += ' and last_name like ' + "'" + last_name1 + "'" 
        elif last_name1 != "" :
            a += ' last_name like ' + "'" + last_name1 + "'" 
        
        if gend != '' and (last_name1 != '' or first_name1 != '' ):
            a += ' and gender like ' + "'" + gend + "'" 
        elif gend != '' :
            a += ' gender like ' + "'" + gend + "'" 
        
        if state1 != '' and (gend != '' or last_name1 != '' or first_name1 != '') :
            a += ' and state like ' + "'" + state1 + "'" 
        elif state1 != '' :
            a += ' state like ' + "'" + state1 + "'" 
        
        if creds != '' and (state1 != '' or gend != '' or last_name1 != '' or first_name1 != '' ):
            a += ' and  credentials like ' + "'"  + creds + "'" 
        elif creds != '' :
            a += '  credentials like ' + "'"  + creds + "'" 
        
        if specialty1 != '' and (creds != '' or state1 != '' or gend != '' or last_name1 != '' or first_name1 != '') :
            a += ' and specialty like ' + "'" + specialty1 + "'" 
        elif specialty1 != '' :
            a += ' specialty like ' + "'" + specialty1 + "'" 

        print(a) 

        cur.execute(a)
        x = cur.fetchall()
        cur.close()
        conn.close()

    else :
        conn = psy.connect(host="noic-server.postgres.database.azure.com", port= 5432, database='noic', user='noic', password='INTEX2021*')
        cur = conn.cursor()
        x = """select * from prescriber inner join person on prescriber.prescriber_id = person.person_id inner join prescriber_credential on prescriber_credential.npi = prescriber.npi LIMIT 30"""
        cur.execute(x)
        x = cur.fetchall()

        cur.close()
        conn.close()

    context = {
        'drugs' : data,
        'pre' : prescribe,
        'cred' : credentials,
        'dynamic': x,
    }


    return render(request, 'NOIC_app/prescriberPortal.html', context)

def showGovAgencyPageView(request) : 
    data = Drug.objects.all()

    context = {
        'drugs' : data 
    }

    return render(request, 'NOIC_app/govPortal.html', context)

def showGetHelpPageView(request) :
    return HttpResponse("Get help")

def accountSetUpPageView(request) :
    return render(request, 'NOIC_app/createaccount.html' )

def postAccountView(request):

    if request.method == "POST" :

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

       
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try some other username.")
            return redirect('createaccount')
                
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('createaccount')

        myuser = User.objects.create_user(username, email, password)

        myuser.save()
        
        messages.success(request, "Your account has been successfully created")
    
        return render(request, 'NOIC_app/login.html')

def signInPageView(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'NOIC_app/prescriberPortal.html')
        else :
            messages.error(request, "The username or password you entered is incorrect.")
            return redirect('loginpage')

    return render(request, 'NOIC_app/login.html')
        
def signoutPageView(request) :
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('landingpage')


def updateData(request):
    
    if request.method == "POST" :
        num = request.POST["numdrugs"]
        
        newrecord = Prescribeslink()
        for entry in range(1, num) :
            
                pres_name = request.POST["name"]
                drugname =  request.POST["drug-dropdown"]

                id = Drug.objects.all()
                newrecord.prescriber_id = request.POST["npi"]
                newrecord.drug_id = id

        newrecord.save()


def choosePortalPageView(request) :
    return render(request, 'NOIC_app/choosePortal.html')


    

#tylers going to pass the NPI

def drugViewPage(request, npi):
    id = npi
    
    data1 = Prescribeslink.objects.filter(npi = id).distinct('drug').distinct("drug")
    
    data2 = Prescriber.objects.filter(npi=id)
    data3 = Person.objects.filter(person_id__in =  data2.values("npi"))
    
    datacount = Prescribeslink.objects.filter(npi = id).values("drug").annotate(count_drug = Count('drug'))
    #avg = Prescribeslink.objects.filter(prescriber_id = id).values("drug").annotate(average_drug = Count('drug')/Sum(Count('drug')))

    
   
    
    # data3 = Person.objects.filter(person_id = data4.prescriber_id)
    context = {
        'drugs': data1,
        'count': datacount,
        'hello': data3,
        
    }
    return render(request, 'NOIC_app/drugview.html', context)



def searchDrugPageView(request):
    data = Drug.objects.all()[0:100]

    context = {
        'drug' : data
    }


    return render(request, 'NOIC_app/drugsearch.html', context)

def topTenPageView(request, dName):
    print(dName)
    id = Drug.objects.filter(name=dName).values("drug_id")
    top = Prescribeslink.objects.filter(drug__in=id).values('prescriber').annotate(qty=Count('drug')).order_by('qty').reverse()[0:10]
    name = Prescriber.objects.filter(npi__in=top)
    

    context = {
        'data' : top,
        'names' : name,

    }

    return render(request, 'NOIC_app/topten.html', context)

#CRUD appj

def addData(request):
    
    if request.method == "POST" :
        conn = psy.connect(host="noic-server.postgres.database.azure.com", port= 5432, database='noic', user='noic', password='INTEX2021*')
        cur = conn.cursor()

        sql = """Insert Into person(person_id,first_name, last_name, email, phone, gender) OVERRIDING SYSTEM VALUE
                values ((select (max(person_id) +1) from person), %s, %s, %s, %s, %s );"""
        # sql = """Insert into person(first_name, last_name, email, phone, gender) 
        #         values(%s, %s, %s, %s, %s) RETURNING person_id;""" 
                
        sql2 = """Insert Into prescriber(prescriber_id, npi, is_opioid_prescriber, state, specialty) OVERRIDING SYSTEM VALUE
	            values ((select max(person_id) from person), %s, %s, %s, %s);"""

        npi = request.POST["npi"]
        first_name = request.POST["first_name"]
        last_name =  request.POST["last_name"]
        email = request.POST["email"]
        phone =  request.POST["phone"]
        gender =  request.POST["gender"]
        is_opioid_prescriber =  request.POST["is_opi"]
        state = request.POST["state"]
        specialty = request.POST["specialty"]      
        
        cur.execute(sql, (first_name, last_name, email, phone, gender))
        conn.commit()

        cur.execute(sql2, (npi, is_opioid_prescriber, state, specialty))
        conn.commit()

        cur.close()

        conn.close()
        return render(request, 'NOIC_app/successfulAdd.html')    
    

def deletePrescriber(request, npi) :
    data = Prescriber.objects.get(id = npi)

    data.delete()

    return render(request, 'NOIC_app/successfulAdd.html')


def successfulAddView(request) :
    return render(request, 'NOIC_app/successfulAdd.html')