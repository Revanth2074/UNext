import unittest
from data.datastore import DATASTORE
from services.customer_service import add_customer
from models.customer import Customer

class TestCustomer(unittest.TestCase):
    def setUp(self):
        DATASTORE["customers"].clear()
        DATASTORE["vehicles"].clear()
        DATASTORE["rentals"].clear()

    def test_add_customer(self):
        cust = add_customer("Arjun", 24, "9876543210", "TN10-2021-0042", 5000.0)
        
        self.assertIn(cust.person_id, DATASTORE["customers"])
        self.assertEqual(DATASTORE["customers"][cust.person_id].name, "Arjun")

    def test_wallet_encapsulation(self):
        c = Customer("CU01", "Arjun", 24, "9876543210", "TN10-2021-0042", 5000.0)
        
        self.assertEqual(c.balance, 5000.0)

        self.assertTrue(c.pay(3000.0))
        self.assertEqual(c.balance, 2000.0)

        self.assertFalse(c.pay(2500.0))
        self.assertEqual(c.balance, 2000.0)

        with self.assertRaises(AttributeError):
            _ = c.__wallet

if __name__ == "__main__":
    unittest.main()
