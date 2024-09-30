# forms.py
from django import forms
from .models import Patient, Bill

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'phone', 'gender', 'address', 'department']


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['patient', 'amount', 'description']

from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'phone_number', 'email', 'doctor', 'appointment_date']
