from django.db import models
from django.contrib.auth.models import User



departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"


class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)


    
class Pharmacist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    registration_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    
# class Pharmacist(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     registration_number = models.CharField(max_length=20, primary_key=True)  # Unique ID
#     name = models.CharField(max_length=100)  # Name of the pharmacist
#     address = models.CharField(max_length=255)  # Address
#     email = models.EmailField()  # Email address
#     status = models.BooleanField(default=False)  # Approval status

#     def __str__(self):
#         return self.name

class Drug(models.Model):
    name = models.CharField(max_length=100)  # Name of the drug
    description = models.TextField()  # Description of the drug
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the drug
    quantity = models.PositiveIntegerField()  # Stock quantity

    def __str__(self):
        return self.name

# class Prescription(models.Model):
#     patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions')  # Patient
#     doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_prescriptions')  # Doctor
#     pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE, null=True, blank=True)  # Pharmacist
#     drug = models.ForeignKey(Drug, on_delete=models.CASCADE)  # Prescribed drug
#     dosage = models.CharField(max_length=100)  # Dosage instructions
#     date = models.DateTimeField(auto_now_add=True)  # Date of prescription

#     def __str__(self):
#         return f"{self.patient.username} - {self.drug.name}"
    

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_prescriptions')
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE, null=True, blank=True)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.drug.name}"


class Invoice(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')  # Patient
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE)  # Pharmacist
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total cost
    date = models.DateTimeField(auto_now_add=True)  # Invoice date

    def __str__(self):
        return f"Invoice {self.id} for {self.patient.username}"
    
# class TimeSlot(models.Model):
#     doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="time_slots")
#     slot_time = models.TimeField()

class TimeSlot(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timeslots')
    start_time = models.TimeField()
    end_time = models.TimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)  # 0 = Available, 1 = Booked
    
    def __str__(self):
        return f"{self.doctor.username}: {self.start_time} - {self.end_time} (Status: {self.status})"



