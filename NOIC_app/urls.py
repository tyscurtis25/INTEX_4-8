from django.urls import path
from .views import drugViewPage, searchDrugPageView, showGovAgencyPageView, showLandingPageView, showLoginPageView, showPrescriberPageView, successfulAddView, updatePrescriberInfo
from .views import showGetHelpPageView, accountSetUpPageView, postAccountView, signInPageView, updateData,topTenPageView, choosePortalPageView, addData
from .views import updatePrescriberPageView, updatePrescriberInfo, successfulUpView

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
    path("updateview/please", updatePrescriberInfo, name = 'updatepage'),
    path("prescriber/update/", updatePrescriberPageView, name="updarecord"),
    path("successfulAdd/", successfulAddView, name="success"),
    path("updatePre/", updatePrescriberPageView, name="updatePre"),
    path("successfulUp/", successfulUpView, name="successUp"),
]
