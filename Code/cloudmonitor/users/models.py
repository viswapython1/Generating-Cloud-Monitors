from django.db import models
from django.contrib.auth.models import User
import os

INDCHOICES = (
    ('FINANCE', 'FINANCE'),
    ('HEALTHCARE', 'HEALTHCARE'),
    ('INSURANCE', 'INSURANCE'),
    ('LEGAL', 'LEGAL'),
    ('MANUFACTURING', 'MANUFACTURING'),
    ('PUBLISHING', 'PUBLISHING'),
    ('REAL ESTATE', 'REAL ESTATE'),
    ('SOFTWARE', 'SOFTWARE'),
)

class Account(models.Model):
    name = models.CharField("Name of Account", "name", max_length=64)
    email = models.EmailField(blank = True, null = True)
    phone = models.CharField(max_length=20, blank = True, null = True)
    industry = models.CharField("Industry Type", max_length=255, choices=INDCHOICES, blank=True, null=True)
    website = models.URLField("Website", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    createdBy = models.ForeignKey(User, related_name='account_created_by', on_delete=models.CASCADE)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ContactSource(models.Model):
    status = models.CharField("Contact Source", max_length=20)

    def __str__(self):
        return self.status

class ContactStatus(models.Model):
    status = models.CharField("Contact Status", max_length=20)

    def __str__(self):
        return self.status

class Contact(models.Model):
    first_name = models.CharField("First name", max_length=255, blank = True, null = True)
    last_name = models.CharField("Last name", max_length=255, blank = True, null = True)
    account = models.ForeignKey(Account, related_name='lead_account_contacts', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank = True, null = True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    createdBy = models.ForeignKey(User, related_name='contact_created_by', on_delete=models.CASCADE)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

class ActivityStatus(models.Model):
    status = models.CharField("Activity Status", max_length=20)

    def __str__(self):
        return self.status

class Activity(models.Model):
    description = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.description

class CloudUsersModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    address = models.TextField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=100,default='waiting')

    def __str__(self):
        return self.email

    class Meta:
        db_table = "registrations"

class UserAppCreatModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    appname = models.CharField(max_length=200,unique=True)
    accesskey = models.CharField(max_length=200,default='waiting')
    secretkey = models.CharField(max_length=200,default='waiting')
    def __str__(self):
        return self.appname
    class Meta:
        db_table = "userapps"

class UserFileModel(models.Model):
    id = models.AutoField(primary_key=True)
    name         = models.CharField(max_length=200)
    email       = models.CharField(max_length=200)
    appname           = models.CharField(max_length=200)
    accesskey               = models.CharField(max_length=200)
    secretkey               = models.CharField(max_length=200)
    filename                = models.CharField(max_length=200)
    userfile             = models.FileField(upload_to='media/')

    def __str__(self):
        return os.path.basename(self.userfile.name)
    class Meta:
        db_table = "userfiles"

    def delete(self, *args, **kwargs):
        self.userfile.delete()
        super().delete(*args, **kwargs)

