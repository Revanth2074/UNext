from data.datastore import DATASTORE
from models.customer import Customer
from models.vehicle import Bike, Car, SUV
from models.rental import Rental

def seed_data():
    """
    Clears current datastore and populates it with the initial sample dataset.
    Resets counter states to ensure consistent ID generation.
    """
    # 1. Clear datastore
    DATASTORE["customers"].clear()
    DATASTORE["vehicles"].clear()
    DATASTORE["rentals"].clear()

    # 2. Reset counters
    Bike.auto_id_counter = 101
    Car.auto_id_counter = 201
    SUV.auto_id_counter = 301
    Rental.auto_id_counter = 5001

    # 3. Add vehicles
    v1 = Bike("Honda Activa", True, 400.0)
    v2 = Car("Maruti Swift", True, 1800.0)
    v3 = SUV("Toyota Innova", True, 3500.0)

    DATASTORE["vehicles"][v1.vehicle_id] = v1
    DATASTORE["vehicles"][v2.vehicle_id] = v2
    DATASTORE["vehicles"][v3.vehicle_id] = v3

    # 4. Add customers
    # We use mock values for phone number
    c1 = Customer(
        person_id="CU01",
        name="Arjun",
        age=24,
        phone="9876543210",
        license_no="TN10-2021-0042",
        wallet=5000.0
    )
    c2 = Customer(
        person_id="CU02",
        name="Meera",
        age=31,
        phone="9876543211",
        license_no="TN22-2018-0913",
        wallet=15000.0
    )
    c3 = Customer(
        person_id="CU03",
        name="Rahul",
        age=17,
        phone="9876543212",
        license_no="none",
        wallet=2000.0
    )

    DATASTORE["customers"][c1.person_id] = c1
    DATASTORE["customers"][c2.person_id] = c2
    DATASTORE["customers"][c3.person_id] = c3
