class PatientService:
    def __init__(self, datastore):
        self.datastore = datastore
    
    def add_patient(self, patient):
        self.datastore["patients"][patient._id] = patient

    def get_patient(self, patient_id):
        return self.datastore["patients"].get(patient_id).display_info()
    
def update_patient(self, patient_id, ailment):
    if patient_id in self.datastore["patients"]:
        self.datastore["patients"][patient_id].ailment = ailment

def delete_patient(self, patient_id):
    if patient_id in self.datastore:
        self.datastore=["patients"]
    del self.datastore["patients"][patient_id]