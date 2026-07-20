import unittest
from data.datastore import DATASTORE
from services.subscriber_service import add_subscriber
from models.subscriber import Subscriber

class TestSubscriber(unittest.TestCase):
    def setUp(self):
        # Clear the datastore before every test to ensure a clean slate
        DATASTORE["subscribers"].clear()
        DATASTORE["plans"].clear()
        DATASTORE["connections"].clear()

    def test_add_subscriber(self):
        # Add subscriber using service
        sub = add_subscriber("Karthik", 26, "1234567890", "9998887771", "AAD-4821-9034", 2000.0)
        
        # Verify that the subscriber's ID appears in the datastore
        self.assertIn(sub.person_id, DATASTORE["subscribers"])
        self.assertEqual(DATASTORE["subscribers"][sub.person_id].name, "Karthik")

    def test_balance_encapsulation(self):
        # Create a subscriber directly
        s = Subscriber("SUB01", "Karthik", 26, "1234567890", "9998887771", "AAD-4821-9034", 2000.0)
        
        # Verify read-only property balance works
        self.assertEqual(s.balance, 2000.0)

        # deduct() within balance
        self.assertTrue(s.deduct(1500.0))
        self.assertEqual(s.balance, 500.0)

        # deduct() beyond balance returns False and keeps balance unchanged
        self.assertFalse(s.deduct(600.0))
        self.assertEqual(s.balance, 500.0)

        # reading s.__balance raises AttributeError (name mangling enforces private status)
        with self.assertRaises(AttributeError):
            _ = s.__balance

if __name__ == "__main__":
    unittest.main()
