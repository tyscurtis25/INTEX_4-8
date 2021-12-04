from django.shortcuts import render

# Create your views here.
def showGovPortalPageView(request) :
    return render(request, 'NOIC_app/govPortal.html')