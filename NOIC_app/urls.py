from django.urls import path
from .views import showGovAgencyPageView, showLandingPageView, showLoginPageView, showPrescriberPageView
from .views import showGetHelpPageView, accountSetUpPageView, postAccountView, signInPageView, addData

urlpatterns = [
    path("", showLandingPageView, name="landingpage"),
    path("login/", showLoginPageView, name="loginpage"),
    path("prescriber/", showPrescriberPageView, name="prescriber"),
    path("gethelp/", showGetHelpPageView, name="getHelp"),
    path("createaccount/", accountSetUpPageView, name="createaccount"),
    path("createaccount/signup/", postAccountView, name="signup"),
    path("login/signedup/", signInPageView, name="signin"),
    path("gov/", showGovAgencyPageView, name="gov"),
    path("gov/adddata/", addData, name="dataAdd")
]
