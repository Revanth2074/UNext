from data.datastore import DATASTORE
from models.rental import Rental
import services.customer_service as customer_service
import services.vehicle_service as vehicle_service
import utils.validator as validator
from typing import List, Optional

def rent(cust_id: str, veh_id: str, days: int) -> Rental:
    """
    Rents a vehicle to a customer.
    Validates customer eligibility, vehicle availability, and charges cost + deposit.
    """
    customer = customer_service.get_customer(cust_id)
    if not customer:
        raise ValueError(f"Customer {cust_id} not found.")

    vehicle = vehicle_service.get_vehicle(veh_id)
    if not vehicle:
        raise ValueError(f"Vehicle {veh_id} not found.")

    if not validator.is_eligible(customer):
        raise ValueError(f"Customer {cust_id} is ineligible (must be age 18+ and have a license).")

    if not validator.is_available(vehicle):
        raise ValueError(f"Vehicle {veh_id} is currently unavailable/rented.")

    if not validator.positive_int(days):
        raise ValueError("Rental duration in days must be a positive integer.")

    days = int(days)
    
    # Calculate costs
    cost = vehicle.rental_cost(days)
    deposit = vehicle.daily_rate * vehicle.deposit_days
    total_charge = cost + deposit

    # Charge customer
    if not customer.pay(total_charge):
        raise ValueError(
            f"Insufficient wallet balance. Total cost is ₹{total_charge:.2f} (rental: ₹{cost:.2f} + deposit: ₹{deposit:.2f}), "
            f"but current balance is ₹{customer.balance:.2f}."
        )

    # Update vehicle status
    vehicle.available = False

    # Create and store rental
    rental = Rental(customer, vehicle, days, cost, deposit, status="ACTIVE")
    DATASTORE["rentals"][rental.rental_id] = rental
    return rental

def return_vehicle(rental_id: int, actual_days: int, damage_note: Optional[str] = None) -> float:
    """
    Returns a rented vehicle, processes late fees/damage fines, and refunds remaining deposit.
    Charges = late_fee (extra_days * rate * 1.5) + damage_fine (₹1000 if damage_note is provided).
    Refund = max(0, deposit - charges) credited back to customer's wallet.
    """
    rental_key = int(rental_id)
    rental = DATASTORE["rentals"].get(rental_key)
    if not rental:
        raise ValueError(f"Rental #{rental_id} not found.")

    if rental.status == "CLOSED":
        raise ValueError(f"Rental #{rental_id} is already closed/returned.")

    actual_days = int(actual_days)
    if actual_days < 0:
        raise ValueError("Actual days of rental cannot be negative.")

    # Calculate charges
    extra_days = max(0, actual_days - rental.planned_days)
    late_fee = extra_days * rental.vehicle.daily_rate * 1.5
    
    has_damage = damage_note is not None and damage_note.strip().lower() not in ("", "none", "(none)")
    damage_fine = 1000.0 if has_damage else 0.0
    
    charges = late_fee + damage_fine
    refund = max(0.0, rental.deposit - charges)

    # Process return
    rental.customer.add_money(refund)
    rental.vehicle.available = True
    rental.status = "CLOSED"

    # Attach damage note via setattr if applicable
    if has_damage:
        setattr(rental, "damage_note", damage_note.strip())

    return refund

def get_rental(rental_id: int) -> Optional[Rental]:
    """Retrieves a rental by ID."""
    return DATASTORE["rentals"].get(int(rental_id))

def list_rentals() -> List[Rental]:
    """Lists all rentals in the system."""
    return list(DATASTORE["rentals"].values())

def delete_rental(rental_id: int) -> bool:
    """Deletes a rental from the datastore."""
    rental_key = int(rental_id)
    if rental_key in DATASTORE["rentals"]:
        del DATASTORE["rentals"][rental_key]
        return True
    return False
