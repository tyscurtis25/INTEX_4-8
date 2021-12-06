from django.db.models.aggregates import Avg, Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Drug, Prescribeslink, Prescriber, Person

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count

# Create your views here.
def showLandingPageView(request) :
    return render(request, 'NOIC_app/landingPage.html')

def showLoginPageView(request) :
    return render(request, 'NOIC_app/login.html')

def showPrescriberPageView(request) :
    data = Drug.objects.all()
    prescribe = Prescriber.objects.all()[0:5]

    context = {
        'drugs' : data,
        'pre' : prescribe
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
            
                drugname =  request.POST["drug-dropdown"]

                id = Drug.objects.all()
                newrecord.prescriber_id = request.POST["npi"]
                newrecord.drug_id = id

        newrecord.save()
            
    return HttpResponse("hello")


def choosePortalPageView(request) :
    return render(request, 'NOIC_app/choosePortal.html')


    

#tylers going to pass the NPI

def drugViewPage(request, npi):
    id = npi
    
    data1 = Prescribeslink.objects.filter(prescriber_id = id).distinct('drug').distinct("drug")
    
    data2 = Prescriber.objects.filter(npi=id)
    data3 = Person.objects.filter(person_id__in =  data2.values("prescriber_id"))
    
    datacount = Prescribeslink.objects.filter(prescriber_id = id).values("drug").annotate(count_drug = Count('drug'))
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

def addData(request):
    
    if request.method == "POST" :
        num = request.POST["numdrugs"]
        
        newrecord = Prescribeslink()
        for entry in range(1, num) :
            
                drugname =  request.POST["drug-dropdown"]

                id = Drug.objects.all()
                newrecord.prescriber_id = request.POST["npi"]
                newrecord.drug_id = id

        newrecord.save()
            
    return HttpResponse("hello")   

