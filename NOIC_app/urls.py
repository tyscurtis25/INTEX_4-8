from django.urls import path
from .views import drugViewPage, searchDrugPageView, showGovAgencyPageView, showLandingPageView, showLoginPageView, showPrescriberPageView
from .views import showGetHelpPageView, accountSetUpPageView, postAccountView, signInPageView, updateData,topTenPageView, choosePortalPageView, addData
from .views import updatePrescriberPageView

urlpatterns = [
    path("", showLandingPageView, name="landingpage"),
    path("login/", showLoginPageView, name="loginpage"),
    path("prescriber/", showPrescriberPageView, name="prescriber"),
    path("gethelp/", showGetHelpPageView, name="getHelp"),
    path("createaccount/", accountSetUpPageView, name="createaccount"),
    path("createaccount/signup/", postAccountView, name="signup"),
    path("login/signedup/", signInPageView, name="signin"),
    path("gov/", showGovAgencyPageView, name="gov"),
    path("gov/updatedata/", updateData, name="dataup"),
    path("drugview/<int:npi>/", drugViewPage, name="drug"),
    path('drugsearch/', searchDrugPageView, name='drugsearch'),
    path('drugsearch/topten/<str:dName>/', topTenPageView, name='top'),
    path('choosePortal/', choosePortalPageView, name='chooseP'),
    path("prescriber/added/", addData, name="dataAdd"),
    path("prescriber/update/", updatePrescriberPageView, name='update' ),
]
