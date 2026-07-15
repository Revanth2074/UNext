from models.patient import Patient
from services.healthcare_system import HealthcareSystem

#Initialize the systems
system = HealthcareSystem(datastore)

#Create patients
p1 = Patient(1, "John Doe", 30, "Flu")
p2 = Patient(2, "Jane Smith", 25, "Cold")