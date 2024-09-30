from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('doctor', views.doctor, name='doctor'),
    path('register', views.register, name='register'),
    path('admindashboard', views.admindashboard, name='admindashboard'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('discharge/', views.discharge, name='discharge'),
    path('generate_bill/', views.generate_bill, name='generate_bill'),
    path('pay_bill/', views.pay_bill, name='pay_bill'),
    path('get_bills/<str:patient_id>/', views.get_bills, name='get_bills'),
    path('get_bill_amount/<str:bill_id>/', views.get_bill_amount, name='get_bill_amount'),
    path('login/', views.login, name='login'),
    path('logout/', views.signout, name='signout'),
    path('dsignup/', views.dsignup, name='dsignup'),
    path('rsignup/', views.rsignup, name='rsignup'),
    path('help', views.help, name='help'),
    path('patient_details/', views.patient_details, name='patient_details'),
    path('get_doctors/', views.get_doctors, name='get_doctors'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('check_status', views.check_appointment_status, name='check_status'),
    path('doctors/', views.doctor_list, name='doctors'),
]
