import decimal
from typing import cast
from django.db.models.functions import Round
from django.db.models.aggregates import Avg, Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Drug, Prescribeslink, Prescriber, Person, PrescriberCredential, Credential

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
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
    context = {
        'drugs' : data,
        'pre' : prescribe,
        'cred' : credentials
    }

    return render(request, 'NOIC_app/prescriberPortal.html', context)

def showGovAgencyPageView(request) : 
    data = Drug.objects.all()
    agg = Prescribeslink.objects.aggregate(Count('id'))
    
    sum = Prescribeslink.objects.values("drug").distinct("drug")

    context = {
        'drugs' : data, 
        'aggre': agg,
        'dis': sum
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
    # avg = Prescribeslink.objects.filter(npi=id).values('drug').annotate(average = Count("drug")/ Count('npi', distinct= True))
    conn = psy.connect(host="noic-server.postgres.database.azure.com", port= 5432, database='noic', user='noic', password='INTEX2021*')
    cur = conn.cursor()
    
    
    avg = cur.execute("""select drug_id, Round(cast(count(drug_id)as decimal)/cast(count(distinct npi)as decimal), 2) as avg_drug
from prescribeslink
group by drug_id;""")
    x = cur.fetchall()
    print(x)
    print("hi")

    context = {
        'drugs': data1,
        'count': datacount,
        'hello': data3,
        'average': x,
        
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
    top = Prescribeslink.objects.filter(drug__in=id).values('npi').annotate(qty=Count('drug')).order_by('qty').reverse()[0:10]
    name = Prescriber.objects.filter(npi__in=top.values("npi"))
    print(name.query)
    print(top)
    
    context = {
        'data' : top,
        'names' : name,

    }

    return render(request, 'NOIC_app/topten.html', context)

#CRUD app

def addData(request):
    
    if request.method == "POST" :
        new_prescriber = Prescriber()
        new_person = Person()

        new_prescriber.npi = request.POST["p_npi"]
        new_person.new_first = request.POST["new_first_name"]
        new_person.new_last =  request.POST["new_last_name"]
        new_person.gender =  request.POST["gender"]
        new_prescriber.op_pres = request.POST["opioid_pres"]
        new_prescriber.credentials =  request.POST["credentials"]
        new_prescriber.location =  request.POST["location"]
        new_prescriber.specialty =  request.POST["specialty"]

        new_prescriber.save()
            
    return showPrescriberPageView(request)   

def deletePrescriber(request, npi) :
    data = Prescriber.objects.get(id = npi)

    data.delete()

    return showPrescriberPageView(request)
