from data.datastore import DATASTORE
from models.subscriber import Subscriber
from models.plan import Prepaid, Postpaid, DataPack
from models.connection import Connection

def seed_data():
    """
    Clears current datastore and populates it with the initial sample dataset.
    Resets counter states to ensure consistent ID generation.
    """
    # 1. Clear datastore
    DATASTORE["subscribers"].clear()
    DATASTORE["plans"].clear()
    DATASTORE["connections"].clear()

    # 2. Reset counters
    Prepaid.auto_id_counter = 101
    Postpaid.auto_id_counter = 201
    DataPack.auto_id_counter = 301
    Connection.auto_id_counter = 9001

    # 3. Add plans
    p1 = Prepaid("Smart Saver", 0.0, 200.0)
    p2 = Postpaid("Business Pro", 0.0, 500.0)
    p3 = DataPack("NetMax 2GB/day", 2.0, 300.0)

    DATASTORE["plans"][p1.plan_id] = p1
    DATASTORE["plans"][p2.plan_id] = p2
    DATASTORE["plans"][p3.plan_id] = p3

    # 4. Add subscribers
    # We use some mock values for phone and mobile_no
    s1 = Subscriber(
        person_id="SUB01",
        name="Karthik",
        age=26,
        phone="9876543210",
        mobile_no="9998887771",
        id_proof="AAD-4821-9034",
        balance=2000.0
    )
    s2 = Subscriber(
        person_id="SUB02",
        name="Divya",
        age=34,
        phone="9876543211",
        mobile_no="9998887772",
        id_proof="AAD-7733-1268",
        balance=5000.0
    )
    s3 = Subscriber(
        person_id="SUB03",
        name="Vimal",
        age=16,
        phone="9876543212",
        mobile_no="9998887773",
        id_proof="none",
        balance=500.0
    )

    DATASTORE["subscribers"][s1.person_id] = s1
    DATASTORE["subscribers"][s2.person_id] = s2
    DATASTORE["subscribers"][s3.person_id] = s3
