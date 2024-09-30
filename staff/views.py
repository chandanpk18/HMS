from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Patient, Bill, HelpRequest
from datetime import datetime
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from .models import users

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})


def is_admin(user):
    return user.is_superuser
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_register(user):
    return user.groups.filter(name='Register').exists()

def login(request):
    if request.method == "GET":
        form = AuthenticationForm()
        context = { "form": form }
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username,password)
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                loginUser(request, user)
                return redirect('dashboard')
        else:
            context = {
                "form": form
            }
            return render(request, 'login.html', context=context)


@login_required(login_url='login')
@user_passes_test(is_register)
def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        department = request.POST.get('department')
        gender = request.POST.get('gender')
        patient = Patient(name=name, phone=phone, address=address, department=department, gender=gender)
        patient.save()
        # Create default admission bill
        Bill.objects.create(patient=patient, amount=500, description="Admission Fee", status='new')
        return redirect('register')

    departments = Department.objects.all()
    patients = Patient.objects.all()
    return render(request, 'register.html', {'departments': departments, 'patients': patients})




def signout(request):
    logout(request)
    #using django.contribs logouts the user
    return redirect('login')


@login_required(login_url='login')
@user_passes_test(is_admin)
def dsignup(request):
    if request.method == "GET":

        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'signup.html', context=context)
    else:
        form = UserCreationForm(request.POST)

        context = {
            "form": form
        }
        if form.is_valid():
            user = form.save()
            print(user.id,user.username)
            user_data = users(username=user.username,password=user.password)
            user_data.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            if user is not None:
                return redirect('admindashboard')
        else:
            return render(request, 'signup.html', context=context)

@login_required(login_url='login')
@user_passes_test(is_admin)
def rsignup(request):
    if request.method == "GET":

        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'rsignup.html', context=context)
    else:
        form = UserCreationForm(request.POST)

        context = {
            "form": form
        }
        if form.is_valid():
            user = form.save()
            print(user.id,user.username)
            user_data = users(username=user.username,password=user.password)
            user_data.save()
            my_doctor_group = Group.objects.get_or_create(name='Register')
            my_doctor_group[0].user_set.add(user)
            if user is not None:
                return redirect('admindashboard')
        else:
            return render(request, 'rsignup.html', context=context)


@login_required(login_url='login')
@user_passes_test(is_register)
def discharge(request):
    if request.method == "POST":
        pid = request.POST.get('patient')
        patient = Patient.objects.get(pid=pid)
        total_amount = 0
        remaining_amount = 0
        bills = Bill.objects.filter(patient=patient)

        for bill in bills:
            total_amount += bill.amount
            if bill.status == 'new':
                remaining_amount += bill.amount

        # Generate PDF
        template_path = 'generate_bill.html'
        context = {'patient': patient, 'bills': bills, 'total_amount': total_amount, 'remaining_amount': remaining_amount}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="bill_{patient.pid}.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        # Discharge the patient
        patient.status = 'discharged'
        patient.save()
        return response

    patients = Patient.objects.filter(status='admitted')
    return render(request, 'discharge.html', {'patients': patients})


@login_required(login_url='login')
@user_passes_test(is_doctor)
def generate_bill(request):
    if request.method == "POST":
        patient_id = request.POST.get('patient_id')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        patient = get_object_or_404(Patient, pid=patient_id)
        Bill.objects.create(patient=patient, amount=amount, description=description, status='new')
        return redirect('doctor')

    patients = Patient.objects.filter(status='admitted')
    return render(request, 'bill.html', {'patients': patients})

def get_bills(request, patient_id):
    bills = Bill.objects.filter(patient__pid=patient_id, status='new').values('id', 'amount')
    return JsonResponse({'bills': list(bills)})

def get_bill_amount(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return JsonResponse({'amount': bill.amount})

@login_required(login_url='login')
@user_passes_test(is_register)
def pay_bill(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        bill_id = request.POST.get('bill_id')

        try:
            bill = Bill.objects.get(id=bill_id, patient__pid=patient_id)
            bill.status = 'paid'
            bill.save()
            return redirect('register')
        except Bill.DoesNotExist:
            return render(request, 'register.html', {'error': 'Invalid Patient ID or Bill ID'})

    return render(request, 'register.html')

# Views
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import  Patient, Department, Doctor


def index(request):
    departments = Department.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'index.html', {'departments': departments,'doctors':doctors})




from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Patient

def patient_details(request):
    if request.method == 'GET':
        pid = request.GET.get('patient_id')
        if pid:
            patient = get_object_or_404(Patient, pid=pid)
            data = {
                'name': patient.name,
                'admission_date': patient.admission_date,
                'gender': patient.gender,
                'department': patient.department,
                'status': patient.status
            }
            return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.http import JsonResponse

def get_doctors(request):
    department_id = request.GET.get('department_id')
    doctors = doctor.objects.filter(department_id=department_id)
    doctor_list = list(doctors.values('id', 'user__username'))  # Adjust this based on your Doctor model
    return JsonResponse(doctor_list, safe=False)

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Department, Doctor


@login_required(login_url='login')
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admindashboard')
    elif is_doctor(request.user):
        return redirect('doctor')
    else:
        return redirect('register')

def contact(request):
    return render(request, 'contact.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doctor, Appointment
from .forms import AppointmentForm
from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .models import Department, Doctor, Appointment
from django.contrib import messages

def book_appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        doctor_id = request.POST.get('doctor')

        # Validate doctor ID
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            doctor = None

        if doctor:
            appointment = Appointment.objects.create(
                name=name,
                phone_number=phone_number,
                email=email,
                doctor=doctor,
                status='pending'  # Initial status is pending
            )
            messages.success(request, 'Appointment booked successfully!')
            return redirect('index')  # Replace 'index' with your actual redirect URL after booking

    # Filter users who belong to the "doctor" group
    doctor_group = Group.objects.get(name='DOCTOR')
    doctors = users.objects.filter(user__groups=doctor_group)
    return render(request, 'index.html', {'doctors': doctors})
from django.shortcuts import render
from .models import Appointment

def check_appointment_status(request):
    appointments = []
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')

        # Assuming phone number is unique for appointments
        appointments = Appointment.objects.filter(name=name, phone_number=phone_number)

    return render(request, 'index.html', {'appointments': appointments})


from django.shortcuts import render, redirect
from .models import Appointment
from django.contrib import messages

@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        status = request.POST.get('status')

        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.status = status
            appointment.save()
            messages.success(request, 'Appointment status updated successfully!')
        except Appointment.DoesNotExist:
            messages.error(request, 'Appointment not found.')

    unread_appointments = Appointment.objects.filter(status='pending')
    todays_appointments = Appointment.objects.filter(status='confirmed')

    return render(request, 'doctor.html', {
        'unread_appointments': unread_appointments,
        'todays_appointments': todays_appointments,
    })




from django.shortcuts import render
from .models import Department, Patient

@login_required(login_url='login')
@user_passes_test(is_admin)
def admindashboard(request):
    # Fetch data from the database
    num_departments = Department.objects.count()
    active_patients = Patient.objects.filter(status='admitted').count()
    total_admissions_today = Patient.objects.filter(admission_date=datetime.today().date()).count()

    # Data for charts
    departments = Department.objects.all()
    department_names = [dept.name for dept in departments]

    # Active patients by department
    active_patients_data = []
    for dept in departments:
        count = Patient.objects.filter(department=dept.name, status='admitted').count()
        active_patients_data.append(count)

    # Admissions by department
    admissions_data = []
    for dept in departments:
        count = Patient.objects.filter(department=dept.name).count()
        admissions_data.append(count)

    # Beds remaining by department
    bed_remaining_data = []
    for dept in departments:
        total_beds = dept.bed
        occupied_beds = Patient.objects.filter(department=dept.name, status='admitted').count()
        bed_remaining_data.append(total_beds - occupied_beds)

    context = {
        'num_departments': num_departments,
        'active_patients': active_patients,
        'total_admissions_today': total_admissions_today,
        'department_names': department_names,
        'active_patients_data': active_patients_data,
        'admissions_data': admissions_data,
        'bed_remaining_data': bed_remaining_data,
    }
    return render(request, 'admin.html', context)


def help(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        help_text = request.POST.get('help')
        if username and email:
            # Saving the help request to the database
            help = HelpRequest.objects.create(username=username, email=email, help_text=help_text)
            help.save()
            #it saves the user query into the help table of the database
            alert_message = "Your query is submitted successfully."
            # Return the HttpResponse object
        return render(request, 'help.html', {'alert_message': alert_message})

    return render(request,'help.html')