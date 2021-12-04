from django.urls import path
from .views import showGovPortalPageView

urlpatterns = [
    path("govPortal/", showGovPortalPageView, name="govportal"),
]