from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails,Pharmacist,Drug,Prescription
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)

# Customize the admin interface for Pharmacist
class PharmacistAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'name', 'email', 'status')  # Display 'status' field
    list_filter = ('status',)  # Filter by 'status' field
    actions = ['approve_pharmacists']  # Custom admin action

    # Custom action to approve pharmacists
    def approve_pharmacists(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, "Selected pharmacists have been approved.")

    approve_pharmacists.short_description = "Approve selected pharmacists"

# Register the model
admin.site.register(Pharmacist, PharmacistAdmin)



class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')  # Fields to display
    search_fields = ('name',)  # Add a search bar

admin.site.register(Drug, DrugAdmin)


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'pharmacist', 'drug', 'dosage', 'date')

admin.site.register(Prescription, PrescriptionAdmin)
