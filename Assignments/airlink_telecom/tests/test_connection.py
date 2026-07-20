import unittest
from data.datastore import DATASTORE
from models.subscriber import Subscriber
from models.plan import Prepaid, Postpaid
from services.connection_service import activate

class TestConnection(unittest.TestCase):
    def setUp(self):
        DATASTORE["subscribers"].clear()
        DATASTORE["plans"].clear()
        DATASTORE["connections"].clear()
        
        # Reset counters
        Prepaid.auto_id_counter = 101
        Postpaid.auto_id_counter = 201

    def test_activate_success(self):
        # Setup subscriber and plan in DATASTORE
        s = Subscriber("SUB01", "Karthik", 26, "1234567890", "9998887771", "AAD-4821-9034", 2000.0)
        p = Postpaid("Business Pro", 0.0, 500.0) # ID will be POST-201, activation_fee 100
        
        DATASTORE["subscribers"][s.person_id] = s
        DATASTORE["plans"][p.plan_id] = p

        # Activating plan for 2 months
        # Bill for 2 months of Postpaid = 500 * 2 * 1.18 = 1180.0
        # Activation fee = 100.0
        # Total cost = 1280.0
        # Expected remaining balance = 2000.0 - 1280.0 = 720.0
        conn = activate("SUB01", "POST-201", 2)

        # Verify Connection is stored and active
        self.assertIn(conn.connection_id, DATASTORE["connections"])
        self.assertEqual(conn.status, "ACTIVE")
        self.assertEqual(conn.amount_paid, 1280.0)
        
        # Verify balance debited exactly
        self.assertEqual(s.balance, 720.0)

    def test_ineligible_blocked(self):
        # Vimal (age 16, no ID proof)
        s = Subscriber("SUB03", "Vimal", 16, "1234567890", "9998887773", "none", 500.0)
        p = Prepaid("Smart Saver", 0.0, 200.0) # ID will be PRE-101, activation fee 0
        
        DATASTORE["subscribers"][s.person_id] = s
        DATASTORE["plans"][p.plan_id] = p

        # Activating as Vimal is refused
        with self.assertRaises(ValueError):
            activate("SUB03", "PRE-101", 2)

        # Verify nothing is stored in connections
        self.assertEqual(len(DATASTORE["connections"]), 0)
        # Verify balance is unchanged
        self.assertEqual(s.balance, 500.0)

if __name__ == "__main__":
    unittest.main()
