from django.contrib import admin
from .models import Drug, Governmentofficial, Patient, Person, Prescriber, Prescribeslink, State

# Register your models here.
admin.site.register(Drug)
admin.site.register(Governmentofficial)
admin.site.register(Patient)
admin.site.register(Person)
admin.site.register(Prescriber)
admin.site.register(Prescribeslink)
admin.site.register(State)