from django.db import models

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Credential(models.Model):
    credentials = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'credential'
    
    def __str__(self):
        return (self.name)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Drug(models.Model):
    drug_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    is_opioid = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'drug'

    def __str__(self):
        return (self.name)


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

    def __str__(self):
        return (self.patient)


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

    def __str__(self):
        return (self.first_name + ' ' + self.last_name)


class Prescriber(models.Model):
    prescriber = models.OneToOneField(Person, models.DO_NOTHING, primary_key=True)
    npi = models.IntegerField(unique=True)
    specialty = models.CharField(max_length=62)
    is_opioid_prescriber = models.BooleanField()
    state = models.ForeignKey('State', models.DO_NOTHING, db_column='state')

    class Meta:
        managed = False
        db_table = 'prescriber'

    def __str__(self):
        return (self.prescriber)

class PrescriberCredential(models.Model):
    npi = models.OneToOneField(Prescriber, models.DO_NOTHING, db_column='npi', primary_key=True)
    credentials = models.ForeignKey(Credential, models.DO_NOTHING, db_column='credentials')

    class Meta:
        managed = False
        db_table = 'prescriber_credential'
        unique_together = (('npi', 'credentials'),)


class Prescribeslink(models.Model):
    id = models.IntegerField(primary_key=True)
    npi = models.ForeignKey(Prescriber, models.DO_NOTHING, db_column='npi')
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

    def __str__(self):
        return (self.state_name)