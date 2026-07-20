import unittest
from data.datastore import DATASTORE
from models.plan import Prepaid, Postpaid, DataPack

class TestPlan(unittest.TestCase):
    def setUp(self):
        DATASTORE["subscribers"].clear()
        DATASTORE["plans"].clear()
        DATASTORE["connections"].clear()

    def test_bill_overriding(self):
        # Instantiate with price only (supports single argument constructor)
        p1 = Prepaid(200.0)
        p2 = Postpaid(500.0)
        p3 = DataPack(300.0)

        # Assert bill calculations
        self.assertEqual(p1.bill(2), 400.0)
        self.assertEqual(p2.bill(2), 1180.0) # 500 * 2 * 1.18
        self.assertEqual(p3.bill(2), 650.0)  # 300 * 2 + 50

    def test_price_validation(self):
        # Setting monthly_price to 0 or negative during instantiation raises ValueError
        with self.assertRaises(ValueError):
            Prepaid(0.0)
        with self.assertRaises(ValueError):
            Postpaid(-100.0)

        # Modifying monthly_price to 0 or negative via property setter raises ValueError
        p = Prepaid(200.0)
        with self.assertRaises(ValueError):
            p.monthly_price = 0
        with self.assertRaises(ValueError):
            p.monthly_price = -10.0
            
        self.assertEqual(p.monthly_price, 200.0) # unchanged

if __name__ == "__main__":
    unittest.main()
