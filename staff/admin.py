from django.contrib import admin
from .models import Patient,Bill,Doctor,Department,HelpRequest,Appointment
# Register your models here.
from django.contrib import admin
from .models import Department, users, Doctor
from django.contrib.auth.models import Group,User


class DoctorAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            doctor_group = Group.objects.get(name="DOCTOR")
            kwargs["queryset"] = User.objects.filter(groups=doctor_group)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient)
admin.site.register(Bill)
admin.site.register(HelpRequest)
admin.site.register(Department)
admin.site.register(Appointment)
