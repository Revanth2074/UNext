import unittest
from data.datastore import DATASTORE
from models.vehicle import Bike, Car, SUV

class TestVehicle(unittest.TestCase):
    def setUp(self):
        DATASTORE["customers"].clear()
        DATASTORE["vehicles"].clear()
        DATASTORE["rentals"].clear()

    def test_rental_cost_overriding(self):
        
        v1 = Bike(400.0)
        v2 = Car(1800.0)
        v3 = SUV(3500.0)

        
        self.assertEqual(v1.rental_cost(2), 800.0)
        self.assertEqual(v2.rental_cost(2), 3780.0) # 1800 * 2 * 1.05
        self.assertEqual(v3.rental_cost(2), 7500.0) # 3500 * 2 + 500

    def test_rate_validation(self):
        
        with self.assertRaises(ValueError):
            Bike(0.0)
        with self.assertRaises(ValueError):
            Car(-100.0)

        
        v = Bike(400.0)
        with self.assertRaises(ValueError):
            v.daily_rate = 0
        with self.assertRaises(ValueError):
            v.daily_rate = -50.0
            
        self.assertEqual(v.daily_rate, 400.0) # unchanged

if __name__ == "__main__":
    unittest.main()
