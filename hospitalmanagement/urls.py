from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView, LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),  # Home page (Landing page)

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),

    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('patientclick', views.patientclick_view),
    # path('pharmacistclick', views.pharmacistclick_view),

    path('adminsignup', views.admin_signup_view),
    path('doctorsignup', views.doctor_signup_view, name='doctorsignup'),
    path('patientsignup', views.patient_signup_view),

    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),

    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'), name='logout'),

    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),

    path('admin-doctor', views.admin_doctor_view, name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view, name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view, name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view, name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view, name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view, name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view, name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view, name='reject-doctor'),
    path('admin-view-doctor-specialisation', views.admin_view_doctor_specialisation_view, name='admin-view-doctor-specialisation'),

    path('admin-patient', views.admin_patient_view, name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view, name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view, name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view, name='update-patient'),
    path('admin-add-patient', views.admin_add_patient_view, name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view, name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view, name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view, name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view, name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view, name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view, name='download-pdf'),
    # path('download-drug-pdf/<int:pk>', views.download_drug_pdf_view, name='download-drug-pdf'),
    path('issue-drug/<int:patient_id>/', views.issue_drug_view, name='issue-drug'),
    path('test-invoice/', views.test_invoice, name='test-invoice'),


    path('admin-appointment', views.admin_appointment_view, name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view, name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view, name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view, name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view, name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view, name='reject-appointment'),
]

#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns += [
    path('doctor-dashboard', views.doctor_dashboard_view, name='doctor-dashboard'),
    path('search', views.search_view, name='search'),

    path('doctor-patient', views.doctor_patient_view, name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view, name='doctor-view-patient'),
    path('doctor-view-discharge-patient', views.doctor_view_discharge_patient_view, name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_view, name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view, name='doctor-view-appointment'),
    path('doctor-delete-appointment', views.doctor_delete_appointment_view, name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view, name='delete-appointment'),
]

#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns += [
    path('patient-dashboard', views.patient_dashboard_view, name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view, name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view, name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view, name='patient-view-appointment'),
    path('patient-view-doctor', views.patient_view_doctor_view, name='patient-view-doctor'),
    path('searchdoctor', views.search_doctor_view, name='searchdoctor'),
    path('patient-discharge', views.patient_discharge_view, name='patient-discharge'),

]

# #---------FOR PHARMACIST RELATED URLS---------------------------------
# urlpatterns += [
#     path('pharmacistclick', views.pharmacist_dashboard, name='pharmacist-dashboard'),
#     # path('pharmacist-dashboard', views.pharmacist_dashboard, name='pharmacist-dashboard'),
#     path('manage-drugs', views.manage_drugs, name='manage_drugs'),
#     path('view-prescriptions', views.view_prescriptions, name='view-prescriptions'),
#     path('generate-invoice', views.generate_invoice, name='generate-invoice'),
#     path('delete-drug/<int:drug_id>', views.delete_drug, name='delete-drug'),
# ]


# Pharmacist-related URLs
# urlpatterns += [
#     path('pharmacistclick', views.pharmacist_dashboard, name='pharmacist_dashboard'),
#     path('manage-drugs', views.manage_drugs, name='manage_drugs'),
#     path('view-prescriptions', views.view_prescriptions, name='view_prescriptions'),
#     path('generate-invoice', views.generate_invoice, name='generate_invoice'),
#     path('delete-drug/<int:drug_id>', views.delete_drug, name='delete-drug'),
# ]

urlpatterns += [
    path('pharmacistclick', views.pharmacistclick_view, name='pharmacistclick'),
    path('pharmacistsignup', views.pharmacist_signup_view, name='pharmacistsignup'),
    path('pharmacistlogin', LoginView.as_view(template_name='hospital/pharmacistlogin.html'), name='pharmacistlogin'),
    path('pharmacist-dashboard', views.pharmacist_dashboard_view, name='pharmacist-dashboard'),
    path('manage-drugs', views.manage_drugs, name='manage_drugs'),
    # path('view-prescriptions', views.view_prescriptions, name='view_prescriptions'),
    path('generate-invoice', views.generate_invoice, name='generate_invoice'),
    path('delete-drug/<int:drug_id>', views.delete_drug, name='delete-drug'),
    path('view-prescriptions/<int:id>/<int:patient_id>/', views.view_prescriptions, name='view_prescriptions'),
    path('add-prescription/<int:id>/<int:patient_id>/', views.add_prescription, name='add_prescription'),
    path("add-time-slots/", views.add_time_slots, name="add_time_slots"),
    path("edit-time-slots/", views.edit_time_slots, name="edit_time_slots"),
    path("get-time-slots/", views.get_time_slots, name="get_time_slots"),
    path('issue-drug/<int:patient_id>/', views.issue_drug_view, name='issue-drug'),
    path('get-prescription-by-patient/', views.get_prescription_by_patient, name='get_prescription_by_patient'),
]





























# from django.contrib import admin
# from django.urls import path
# from hospital import views
# from django.contrib.auth.views import LoginView,LogoutView


# #-------------FOR ADMIN RELATED URLS
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',views.home_view,name=''),


#     path('aboutus', views.aboutus_view),
#     path('contactus', views.contactus_view),


#     path('adminclick', views.adminclick_view),
#     path('doctorclick', views.doctorclick_view),
#     path('patientclick', views.patientclick_view),

#     path('adminsignup', views.admin_signup_view),
#     path('doctorsignup', views.doctor_signup_view,name='doctorsignup'),
#     path('patientsignup', views.patient_signup_view),
    
#     path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
#     path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
#     path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),


#     path('afterlogin', views.afterlogin_view,name='afterlogin'),
#     path('logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),


#     path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

#     path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
#     path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
#     path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
#     path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
#     path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
#     path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
#     path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
#     path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
#     path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),


#     path('admin-patient', views.admin_patient_view,name='admin-patient'),
#     path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
#     path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
#     path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
#     path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
#     path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
#     path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
#     path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
#     path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
#     path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
#     path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


#     path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
#     path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
#     path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
#     path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
#     path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
#     path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
# ]


# #---------FOR DOCTOR RELATED URLS-------------------------------------
# urlpatterns +=[
#     path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
#     path('search', views.search_view,name='search'),

#     path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
#     path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
#     path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

#     path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
#     path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
#     path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
#     path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
# ]




# #---------FOR PATIENT RELATED URLS-------------------------------------
# urlpatterns +=[

#     path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
#     path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
#     path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
#     path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
#     path('patient-view-doctor', views.patient_view_doctor_view,name='patient-view-doctor'),
#     path('searchdoctor', views.search_doctor_view,name='searchdoctor'),
#     path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),

# ]



# urlpatterns = [
#     # path('', views.index, name='home'),  # Home page
#     path('pharmacistclick', views.pharmacist_dashboard, name='pharmacist_dashboard'),  # Pharmacist dashboard
#     # Other existing routes
#     path('pharmacist-dashboard', views.pharmacist_dashboard, name='pharmacist_dashboard'),
#     path('manage-drugs', views.manage_drugs, name='manage_drugs'),
#     path('view-prescriptions', views.view_prescriptions, name='view_prescriptions'),
#     path('generate-invoice', views.generate_invoice, name='generate_invoice'),
#     path('delete-drug/<int:drug_id>', views.delete_drug, name='delete_drug'),
# ]