from data.datastore import datastore


class SaleService:

    def create_sale(self, sale):

        if sale.medicine.quantity >= sale.quantity:

            sale.medicine.quantity -= sale.quantity

            datastore["sales"][sale.id] = sale

            print("Sale Completed Successfully")

        else:
            print("Insufficient Stock")

    def get_sale(self, sale_id):
        return datastore["sales"].get(sale_id)

    def delete_sale(self, sale_id):
        datastore["sales"].pop(sale_id, None)

    def list_sales(self):
        return datastore["sales"].values()