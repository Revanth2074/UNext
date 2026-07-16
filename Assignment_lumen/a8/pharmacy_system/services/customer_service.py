from data.datastore import datastore


class CustomerService:

    def add_customer(self, customer):
        datastore["customers"][customer.id] = customer

    def get_customer(self, customer_id):
        return datastore["customers"].get(customer_id)

    def update_prescription(self, customer_id, prescription):
        customer = self.get_customer(customer_id)

        if customer:
            customer.prescription = prescription

    def delete_customer(self, customer_id):
        datastore["customers"].pop(customer_id, None)

    def list_customers(self):
        return datastore["customers"].values()