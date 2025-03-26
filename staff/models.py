from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Department(models.Model):
    name = models.CharField(max_length=50,  unique=True)
    description = models.TextField()
    bed = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    password = models.TextField(max_length=20)

    def __str__(self):
        return self.username


class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.user.username



def generate_pid():
    today = datetime.now().strftime('%Y%m%d')
    last_patient = Patient.objects.filter(pid__startswith=today).order_by('pid').last()
    if last_patient:
        last_pid = last_patient.pid
        last_sequence_number = int(str(last_pid)[-3:])
        new_sequence_number = last_sequence_number + 1
    else:
        new_sequence_number = 1
    return f"{today}{new_sequence_number:03}"

genders = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('others', 'Others')
]

class Patient(models.Model):
    pid = models.CharField(max_length=11, unique=True, editable=False)
    name = models.CharField(max_length=30)
    phone = models.BigIntegerField()
    gender = models.CharField(max_length=10, choices=genders)
    address = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    admission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, default='admitted')

    def save(self, *args, **kwargs):
        if not self.pid:
            self.pid = generate_pid()
        super(Patient, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.pid})"


class Bill(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('paid', 'Paid'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"{self.patient.name} - {self.description} ({self.status})"



#this is for customer support table
class HelpRequest(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Resolved', 'Resolved'),
    ]
    username = models.CharField(max_length=100)
    email = models.EmailField()
    help_text = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='New')

    def __str__(self):
        return self.username

from django.utils import timezone
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    appointment_date = models.DateField(default=timezone.now() + timedelta(days=1))


    def __str__(self):
        return f"{self.name} - {self.appointment_date}"