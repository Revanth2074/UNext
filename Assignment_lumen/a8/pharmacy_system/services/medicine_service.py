from data.datastore import datastore


class MedicineService:

    def add_medicine(self, medicine):
        datastore["medicines"][medicine.id] = medicine

    def get_medicine(self, medicine_id):
        return datastore["medicines"].get(medicine_id)

    def update_stock(self, medicine_id, quantity):
        medicine = self.get_medicine(medicine_id)

        if medicine:
            medicine.quantity = quantity

    def update_price(self, medicine_id, price):
        medicine = self.get_medicine(medicine_id)

        if medicine:
            medicine.price = price

    def delete_medicine(self, medicine_id):
        datastore["medicines"].pop(medicine_id, None)

    def list_medicines(self):
        return datastore["medicines"].values()