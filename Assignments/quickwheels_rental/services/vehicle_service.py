from data.datastore import DATASTORE
from models.vehicle import Vehicle, Bike, Car, SUV
from typing import List, Optional

def add_vehicle(vehicle_type: str, name: str, daily_rate: float) -> Vehicle:
    """
    Creates and stores a new Vehicle subclass instance in the datastore.
    Recognized vehicle types: 'bike', 'car', 'suv' (case-insensitive).
    """
    vt_lower = vehicle_type.strip().lower()
    if vt_lower == "bike":
        vehicle = Bike(name, True, daily_rate)
    elif vt_lower == "car":
        vehicle = Car(name, True, daily_rate)
    elif vt_lower == "suv":
        vehicle = SUV(name, True, daily_rate)
    else:
        raise ValueError(f"Unknown vehicle type: {vehicle_type}. Must be Bike, Car, or SUV.")

    DATASTORE["vehicles"][vehicle.vehicle_id] = vehicle
    return vehicle

def get_vehicle(vehicle_id: str) -> Optional[Vehicle]:
    """Retrieves a vehicle by ID."""
    return DATASTORE["vehicles"].get(vehicle_id)

def list_vehicles() -> List[Vehicle]:
    """Lists all vehicles in the system."""
    return list(DATASTORE["vehicles"].values())

def delete_vehicle(vehicle_id: str) -> bool:
    """Deletes a vehicle from the datastore."""
    if vehicle_id in DATASTORE["vehicles"]:
        del DATASTORE["vehicles"][vehicle_id]
        return True
    return False

def apply_festival_offer(vehicle_id: str, pct: float) -> bool:
    """
    Applies a percentage discount to the specified vehicle using setattr.
    Returns True if successful, False if the vehicle was not found.
    """
    vehicle = get_vehicle(vehicle_id)
    if vehicle:
        if pct < 0 or pct > 100:
            raise ValueError("Festival offer percentage must be between 0 and 100.")
        setattr(vehicle, "festival_offer", float(pct))
        return True
    return False
