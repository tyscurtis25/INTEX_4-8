from django.db import models


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Drug(models.Model):
    drug_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    is_opioid = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'drug'


class Governmentofficial(models.Model):
    official = models.OneToOneField('Person', models.DO_NOTHING, primary_key=True)
    position = models.CharField(max_length=30)
    organization = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'governmentofficial'


class Patient(models.Model):
    patient = models.OneToOneField('Person', models.DO_NOTHING, primary_key=True)
    ssn = models.CharField(max_length=11, blank=True, null=True)
    insurance_provider = models.CharField(max_length=50, blank=True, null=True)
    insurance_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient'


class Person(models.Model):
    person_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'person'


class Prescriber(models.Model):
    prescriber = models.OneToOneField(Person, models.DO_NOTHING, primary_key=True)
    npi = models.IntegerField()
    credentials = models.CharField(max_length=20, blank=True, null=True)
    specialty = models.CharField(max_length=62)
    is_opioid_prescriber = models.BooleanField()
    state = models.ForeignKey('State', models.DO_NOTHING, db_column='state')

    class Meta:
        managed = False
        db_table = 'prescriber'


class Prescribeslink(models.Model):
    id = models.IntegerField(primary_key=True)
    prescriber = models.ForeignKey(Prescriber, models.DO_NOTHING)
    drug = models.ForeignKey(Drug, models.DO_NOTHING)
    patient = models.ForeignKey(Patient, models.DO_NOTHING)
    date_prescribed = models.DateField()

    class Meta:
        managed = False
        db_table = 'prescribeslink'


class State(models.Model):
    state = models.CharField(primary_key=True, max_length=2)
    state_name = models.CharField(max_length=30)
    population = models.IntegerField()
    deaths = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'state'