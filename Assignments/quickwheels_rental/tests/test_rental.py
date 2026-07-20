import unittest
from data.datastore import DATASTORE
from models.customer import Customer
from models.vehicle import Bike
from services.rental_service import rent

class TestRental(unittest.TestCase):
    def setUp(self):
        DATASTORE["customers"].clear()
        DATASTORE["vehicles"].clear()
        DATASTORE["rentals"].clear()
        
        Bike.auto_id_counter = 101

    def test_rent_success(self):
        c = Customer("CU01", "Arjun", 24, "9876543210", "TN10-2021-0042", 5000.0)
        v = Bike("Honda Activa", True, 400.0) # ID will be B-101, deposit_days 1
        
        DATASTORE["customers"][c.person_id] = c
        DATASTORE["vehicles"][v.vehicle_id] = v

        r = rent("CU01", "B-101", 2)

        self.assertIn(r.rental_id, DATASTORE["rentals"])
        self.assertEqual(r.status, "ACTIVE")
        self.assertFalse(v.available)
        
        self.assertEqual(c.balance, 3800.0)

    def test_ineligible_blocked(self):
        c = Customer("CU03", "Rahul", 17, "9876543212", "none", 2000.0)
        v = Bike("Honda Activa", True, 400.0) # ID will be B-101, deposit_days 1
        
        DATASTORE["customers"][c.person_id] = c
        DATASTORE["vehicles"][v.vehicle_id] = v

        with self.assertRaises(ValueError):
            rent("CU03", "B-101", 2)

        self.assertEqual(len(DATASTORE["rentals"]), 0)
        self.assertEqual(c.balance, 2000.0)
        self.assertTrue(v.available)

if __name__ == "__main__":
    unittest.main()
