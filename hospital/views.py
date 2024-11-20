from django.shortcuts import render,redirect,reverse
from . import forms,models
from .models import Drug, Prescription, Invoice,User,Patient,Pharmacist,TimeSlot
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .forms import PharmacistUserForm, PharmacistForm,PrescriptionForm
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse


# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')


#for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')


#for showing signup/login button for doctor
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')


#for showing signup/login button for patient
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html')

# def pharmacistclick_view(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect('afterlogin')
#     return render(request,'hospital/pharmacistclick.html')



def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})




def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'hospital/doctorsignup.html',context=mydict)


def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'hospital/patientsignup.html',context=mydict)






#-----------for checking user is doctor , patient or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'hospital/patient_wait_for_approval.html')
        
    elif is_pharmacist(request.user):  # Add this block for pharmacist
        accountapproval = models.Pharmacist.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('pharmacist-dashboard')
        else:
            return render(request, 'hospital/pharmacist_wait_for_approval.html')
    else:
        return redirect('home')








#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/admin_update_patient.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'hospital/admin_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_discharge_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'hospital/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'hospital/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        print(a.__dict__)  # Prints all fields of the appointment object
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)





@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def search_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm = forms.PatientAppointmentForm()
    patient = models.Patient.objects.get(user_id=request.user.id)  # For sidebar patient info
    message = None
    doctors = models.Doctor.objects.all()
    mydict = {'appointmentForm': appointmentForm, 'patient': patient, 'message': message,'doctors': doctors,}

    if request.method == 'POST':
        appointmentForm = forms.PatientAppointmentForm(request.POST)
        
        if appointmentForm.is_valid():
            description = request.POST.get('description')
            doctor_id = request.POST.get('doctorId')
            time_slot_id = request.POST.get('time_slot')  # Fetch the selected time slot
            
            # Get the doctor and timeslot objects
            doctor = models.Doctor.objects.get(user_id=doctor_id)
            time_slot = get_object_or_404(models.TimeSlot, id=time_slot_id, status=0)  # Ensure slot is available
            
            # Mark the time slot as booked
            time_slot.status = 1
            time_slot.save()
            
            # Create the appointment
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = doctor_id
            appointment.patientId = request.user.id
            appointment.doctorName = doctor.user.first_name
            appointment.patientName = request.user.first_name
            appointment.description = description
            appointment.status = False  # Set appointment status to pending
            appointment.time_slot = time_slot  # Link the appointment with the time slot
            appointment.save()
            
            return HttpResponseRedirect('patient-view-appointment')

    return render(request, 'hospital/patient_book_appointment.html', context=mydict)

# def patient_book_appointment_view(request):
#     appointmentForm = forms.PatientAppointmentForm()
#     patient = models.Patient.objects.get(user_id=request.user.id)  # For profile picture in the sidebar
#     message = None

#     if request.method == 'POST':
#         appointmentForm = forms.PatientAppointmentForm(request.POST)
        
#         if appointmentForm.is_valid():
#             doctor_id = request.POST.get('doctorId')
#             time_slot_id = request.POST.get('time_slot')

#             if not time_slot_id:
#                 message = "No time slot selected or no available slots for the selected doctor."
#             else:
#                 desc = request.POST.get('description')
#                 doctor = models.Doctor.objects.get(user_id=doctor_id)
#                 time_slot = models.TimeSlot.objects.get(id=time_slot_id)

#                 appointment = appointmentForm.save(commit=False)
#                 appointment.doctorId = doctor_id
#                 appointment.patientId = request.user.id  # Ensure only the logged-in user's info is stored
#                 appointment.doctorName = doctor.user.first_name
#                 appointment.patientName = request.user.first_name
#                 appointment.description = desc
#                 appointment.time_slot = time_slot
#                 appointment.status = False
#                 appointment.save()

#                 # Redirect to view appointments
#                 return HttpResponseRedirect('patient-view-appointment')

#     doctors = models.Doctor.objects.all()
#     context = {
#         'appointmentForm': appointmentForm,
#         'patient': patient,
#         'message': message,
#         'doctors': doctors,
#     }
#     return render(request, 'hospital/patient_book_appointment.html', context=context)



def patient_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})



def search_doctor_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors=models.Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})




@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})


# View to list all drugs and allow pharmacists to add or delete
# def manage_drugs_view(request):
#     if request.method == "POST":
#         # Add a new drug
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         quantity = request.POST.get('quantity')
#         Drug.objects.create(name=name, description=description, price=price, quantity=quantity)
#         return redirect('manage_drugs')
#     drugs = Drug.objects.all()
#     return render(request, 'manage_drugs.html', {'drugs': drugs})

# View to access prescriptions
def view_prescriptions(request, id,patient_id):
    # Fetch prescriptions for the specific patient
    
    prescriptions = Prescription.objects.filter(patient_id=id)
    # Fetch patient details for context
    patient = get_object_or_404(Patient, id=id)
    # Render the HTML template with prescriptions and patient info
    return render(request, 'hospital/view_prescriptions.html', {
        'prescriptions': prescriptions,
        'patient': patient
    })
# # def view_prescriptions(request):
#     prescriptions = Prescription.objects.all()
#     return render(request, 'hospital/view_prescriptions.html', {'prescriptions': prescriptions})

# View to generate invoice
def generate_invoice(request):
    if request.method == "POST":
        patient_id = request.POST.get('patient_id')
        total_amount = request.POST.get('total_amount')
        pharmacist = request.user.pharmacist
        Invoice.objects.create(patient_id=patient_id, pharmacist=pharmacist, total_amount=total_amount)
        return redirect('hospital/generate_invoice')
    # return render(request, 'generate_invoice.html')
    # Fetch all patients and invoices
    patients = User.objects.filter(groups__name='Patients')  # Assuming patients belong to a "Patients" group
    invoices = Invoice.objects.all()
    return render(request, 'hospital/generate_invoice.html', {'patients': patients, 'invoices': invoices})


# def pharmacist_dashboard(request):
#     return render(request, 'hospital/pharmacist_dashboard.html')  # No extra data needed here

# Manage Drugs View

def is_pharmacist(user):
    return user.groups.filter(name='PHARMACIST').exists()

@login_required(login_url='pharmacistlogin')
@user_passes_test(is_pharmacist)
def manage_drugs(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        models.Drug.objects.create(name=name, description=description, price=price, quantity=quantity)
        return redirect('manage_drugs')  # Stay on the same page after adding a drug

    drugs = models.Drug.objects.all()
    return render(request, 'hospital/manage_drugs.html', {'drugs': drugs})



# def manage_drugs(request):
#     if request.method == "POST":
#         # Add a new drug
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         quantity = request.POST.get('quantity')
#         Drug.objects.create(name=name, description=description, price=price, quantity=quantity)
#         return redirect('pharmacist_dashboard')
#         # return redirect('hospital/manage-drugs')  # Redirect to the same page after adding a drug

#     # Fetch all drugs
#     drugs = Drug.objects.all()
#     return render(request, 'hospital/manage_drugs.html', {'drugs': drugs})


# Delete Drug View

@login_required(login_url='pharmacistlogin')
@user_passes_test(is_pharmacist)
def delete_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    drug.delete()
    return redirect('manage_drugs')

def pharmacistclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'hospital/pharmacistclick.html')


# def pharmacist_signup_view(request):
#     userForm = forms.PharmacistUserForm()
#     if request.method == 'POST':
#         userForm = forms.PharmacistUserForm(request.POST)
#         if userForm.is_valid():
#             user = userForm.save()
#             user.set_password(user.password)
#             user.save()
#             my_pharmacist_group = Group.objects.get_or_create(name='PHARMACIST')
#             my_pharmacist_group[0].user_set.add(user)
#             return HttpResponseRedirect('pharmacistlogin')
#     return render(request, 'hospital/pharmacistsignup.html', {'userForm': userForm})

def pharmacist_signup_view(request):
    user_form = PharmacistUserForm()
    pharmacist_form = PharmacistForm()

    if request.method == 'POST':
        user_form = PharmacistUserForm(request.POST)
        pharmacist_form = PharmacistForm(request.POST)
        if user_form.is_valid() and pharmacist_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            pharmacist = pharmacist_form.save(commit=False)
            pharmacist.user = user
            pharmacist.email = user.email  # Sync email with the user table
            pharmacist.save()

            pharmacist_group = Group.objects.get_or_create(name='PHARMACIST')[0]
            pharmacist_group.user_set.add(user)

            return redirect('pharmacistlogin')
        else:
            user_form_errors = user_form.errors.as_json()  # Get errors for User form
            pharmacist_form_errors = pharmacist_form.errors.as_json()  # Get errors for Pharmacist form
            print("User Form Errors:", user_form_errors)
            print("Pharmacist Form Errors:", pharmacist_form_errors)
            messages.error(request, "There were errors in the form submission. Please correct them.")


    return render(request, 'hospital/pharmacistsignup.html', {
        'user_form': user_form,
        'pharmacist_form': pharmacist_form
    })

@login_required(login_url='pharmacistlogin')
@user_passes_test(is_pharmacist)
def pharmacist_dashboard_view(request):
    try:
        # Get the Pharmacist instance for the logged-in user
        pharmacist = Pharmacist.objects.get(user=request.user)

        # Filter prescriptions assigned to this pharmacist
        prescriptions = Prescription.objects.filter(pharmacist=pharmacist)
        

        # Get patients who have prescriptions assigned to this pharmacist
        patient_ids = prescriptions.values_list('patient_id', flat=True).distinct()
        print("Patient IDs with prescriptions:", patient_ids)  # Debug
        patients = Patient.objects.filter(id__in=patient_ids)
        print("Patients:", patients)  # Debug

        context = {
            'user': request.user,
            'prescriptions': prescriptions,
            'patients': patients,
            'pharmacist': pharmacist,
        }
        return render(request, 'hospital/pharmacist_dashboard.html', context)
    except Pharmacist.DoesNotExist:
        # Handle case where the logged-in user is not linked to a Pharmacist instance
        return HttpResponse("Pharmacist profile not found.", status=404)


# def pharmacist_dashboard_view(request):
#     try:
#         # Get the Pharmacist instance for the logged-in user
#         pharmacist = Pharmacist.objects.get(user=request.user)
        
#         # Filter prescriptions assigned to this pharmacist
#         # prescriptions = Prescription.objects.filter(pharmacist=pharmacist)
#         prescriptions = Prescription.objects.filter(pharmacist=request.user.pharmacist)
#         patients = Patient.objects.all() 
#         print(patients)
#         context = {
#             'user': request.user,
#             'prescriptions': prescriptions,
#             'patients': patients,
#             'pharmacist': pharmacist,
#         }
#         print(context)
#         return render(request, 'hospital/pharmacist_dashboard.html', context)
#     except Pharmacist.DoesNotExist:
#         # Handle case where the logged-in user is not linked to a Pharmacist instance
#         return HttpResponse("Pharmacist profile not found.", status=404)




# def add_prescription(request, patient_id):
#     patient = get_object_or_404(Patient, id=patient_id)
#     if request.method == 'POST':
#         form = PrescriptionForm(request.POST)
#         if form.is_valid():
#             prescription = form.save(commit=False)
#             prescription.patient = patient
#             prescription.doctor = request.user  # Assuming the logged-in user is the doctor
#             prescription.save()
#             return redirect('doctor-dashboard')
#     else:
#         form = PrescriptionForm()

#     return render(request, 'hospital/add_prescription.html', {
#         'form': form,
#         'patient': patient
#     })

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def add_prescription(request, id,patient_id):
    patient = get_object_or_404(Patient, user_id=patient_id)
    drugs = Drug.objects.all()  # Get the list of all available drugs

    if request.method == 'POST':
        drug_ids = request.POST.getlist('drug[]')
        dosages = request.POST.getlist('dosage[]')

        # Iterate over the drugs and dosages and create Prescription objects
        for drug_id, dosage in zip(drug_ids, dosages):
            drug = get_object_or_404(Drug, id=drug_id)
            Prescription.objects.create(
                patient=patient,
                doctor=request.user,
                drug=drug,
                dosage=dosage,
            )

        return redirect('doctor-dashboard')  # Redirect to the doctor dashboard after submission

    return render(request, 'hospital/add_prescription.html', {
        'patient': patient,
        'drugs': drugs,
    })


# @login_required(login_url='pharmacistlogin')
# @user_passes_test(is_pharmacist)
# def pharmacist_dashboard_view(request):
#     # Add any pharmacist-specific dashboard data here
#     return render(request, 'hospital/pharmacist_dashboard.html')


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def add_time_slots(request):
    if request.method == 'POST':
        doctor = request.user  # Ensure this fetches the User instance
        start_time_str = request.POST.get('from_time')  # Use .get() to avoid KeyError
        end_time_str = request.POST.get('to_time')
        
        try:
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
        except ValueError:
            return HttpResponse("Invalid time format. Use HH:MM format.")
        print(f"Start Time: {start_time}, End Time: {end_time}")

        # Check if any time slots are already booked for this doctor
        if models.TimeSlot.objects.filter(doctor=doctor, status=1).exists():
            return HttpResponse("Cannot modify slots. There are booked appointments.")

         # Delete all previous time slots for the doctor
        models.TimeSlot.objects.filter(doctor=doctor).delete()

        # Logic to calculate 15-minute slots
        current_time = start_time
        time_slots = []  # Store the generated time slots
        while current_time < end_time:
            next_time = (datetime.combine(date.today(), current_time) + timedelta(minutes=15)).time()
            time_slots.append(f"{current_time} - {next_time}")
            TimeSlot.objects.create(
                doctor=doctor,  # Assign the User instance
                start_time=current_time,
                end_time=next_time,
                date_created=timezone.now()
            )
            current_time = next_time

        return redirect('add_time_slots')
    
     # Fetch existing time slots for the current doctor
    existing_slots = TimeSlot.objects.filter(doctor=request.user)
    return render(request, 'hospital/add_time_slots.html', {
        'existing_slots': existing_slots,  # Pass existing slots to the template
    })
# def add_time_slots(request):
#     if request.method == "POST":
#         from_time = request.POST.get("from_time")
#         to_time = request.POST.get("to_time")

#         if from_time and to_time:
#             from_time = datetime.strptime(from_time, "%H:%M")
#             to_time = datetime.strptime(to_time, "%H:%M")

#             slots = []
#             while from_time < to_time:
#                 slot_start = from_time
#                 slot_end = from_time + timedelta(minutes=15)
#                 if slot_end <= to_time:
#                     slots.append((slot_start.strftime("%I:%M %p"), slot_end.strftime("%I:%M %p")))
#                 from_time = slot_end
            
#             # Save to database
#             for start, end in slots:
#                 TimeSlot.objects.create(
#                     doctor=request.user.doctor,  # Assuming a ForeignKey to the Doctor model
#                     start_time=start,
#                     end_time=end
#                 )
            
#             messages.success(request, "Time slots successfully added.")

#         # Here, you can save the slots to the database if required
#             return redirect('doctor-dashboard')
        
#             # return render(request, "hospital/add_time_slots.html", {"slots": slots})
#         else:
#             messages.error(request, "Please provide valid time ranges.")

#     return render(request, "hospital/add_time_slots.html")


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def edit_time_slots(request):
    # Fetch existing slots from the database
    slots = TimeSlot.objects.filter(doctor=request.user)

    if request.method == "POST":
        # Update logic (e.g., delete and recreate slots based on input)
        slots.delete()  # Clear old slots
        new_slots = request.POST.getlist("slots[]")
        for slot in new_slots:
            TimeSlot.objects.create(doctor=request.user, slot_time=slot)

        return redirect('doctor-appointment')

    return render(request, "hospital/edit_time_slots.html", {"slots": slots})

def get_time_slots(request):
    doctor_id = request.GET.get('doctor_id')
    if not doctor_id:
        return JsonResponse({"time_slots": []})

    time_slots = models.TimeSlot.objects.filter(doctor_id=doctor_id, status=0).values('id', 'start_time', 'end_time','status')
    time_slots_list = [
        {
            "id": slot["id"],
            "start_time": slot["start_time"].strftime("%H:%M"),
            "end_time": slot["end_time"].strftime("%H:%M"),
            'status': slot["status"],
        }
        for slot in time_slots
    ]
    return JsonResponse({"time_slots": time_slots_list})


def get_prescription_by_patient(request):
    if request.method == "GET":

        patient_id = request.GET.get("patient_id")
        # print(patient_id)
        if not patient_id:
            return JsonResponse({"error": "Patient ID is required"}, status=400)
        
        prescriptions = Prescription.objects.filter(patient_id=patient_id)
        if prescriptions.exists():
            prescriptions_data = [
                {
                    # "id": prescription.id,
                    "drug_name": prescription.drug.name,
                    "dosage": prescription.dosage,
                    "doctor_name": prescription.doctor.first_name,
                    "date": prescription.date.strftime("%Y-%m-%d"),
                }
                for prescription in prescriptions
            ]
            # print(prescriptions_data)
            return JsonResponse({"prescriptions": prescriptions_data}, status=200)
        else:
            return JsonResponse({"error": "No prescriptions found for this patient"}, status=404)

