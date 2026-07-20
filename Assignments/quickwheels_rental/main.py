import sys
import gc
from services.rental_system import RentalSystem


if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_input(prompt: str) -> str:
    return input(prompt).strip()

def get_positive_int(prompt: str) -> int:
    while True:
        val = get_input(prompt)
        try:
            res = int(val)
            if res > 0:
                return res
            print("Please enter a positive integer greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_non_negative_float(prompt: str) -> float:
    while True:
        val = get_input(prompt)
        try:
            res = float(val)
            if res >= 0:
                return res
            print("Please enter a non-negative number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_positive_float(prompt: str) -> float:
    while True:
        val = get_input(prompt)
        try:
            res = float(val)
            if res > 0:
                return res
            print("Please enter a positive number greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():
    # Auto-loads seed data on initialization
    system = RentalSystem(load_seed=True)

    while True:
        print("\n====== QUICKWHEELS VEHICLE RENTAL ======")
        print("1. Register customer")
        print("2. Add vehicle")
        print("3. View vehicles (sorted by rate)")
        print("4. Rent a vehicle")
        print("5. Return a vehicle")
        print("6. View rentals")
        print("7. Exit (archive rentals -> destructors fire)")
        
        choice = get_input("Enter choice: ")

        if choice == "1":
            print("\n--- Register Customer ---")
            name = get_input("Enter name: ")
            age = get_positive_int("Enter age: ")
            phone = get_input("Enter phone: ")
            license_no = get_input("Enter license number (or 'none'): ")
            wallet = get_positive_float("Enter initial wallet balance: ₹")
            
            cust = system.register_customer(name, age, phone, license_no, wallet)
            print(f"Customer registered successfully! Generated ID: {cust.person_id}")

        elif choice == "2":
            print("\n--- Add Vehicle ---")
            print("Types: Bike, Car, SUV")
            vehicle_type = get_input("Enter vehicle type: ")
            name = get_input("Enter vehicle name: ")
            daily_rate = get_positive_float("Enter daily rate: ₹")
            
            try:
                vehicle = system.add_vehicle(vehicle_type, name, daily_rate)
                print(f"Vehicle added successfully! Generated ID: {vehicle.vehicle_id}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            print("\n--- View Vehicles (Sorted by Rate) ---")
            vehicles = system.list_vehicles()
            if not vehicles:
                print("No vehicles available in the system.")
            else:
                sorted_vehicles = sorted(vehicles)
                for v in sorted_vehicles:
                    print(v)

        elif choice == "4":
            print("\n--- Rent Vehicle ---")
            cust_id = get_input("Enter customer ID: ")
            veh_id = get_input("Enter vehicle ID: ")
            days = get_positive_int("Enter rental duration in days: ")
            
            try:
                rental = system.rent_vehicle(cust_id, veh_id, days)
                print(f"Vehicle rented successfully! Generated Rental ID: {rental.rental_id}")
            except ValueError as e:
                print(f"Rental Refused: {e}")

        elif choice == "5":
            print("\n--- Return Vehicle ---")
            rental_id_str = get_input("Enter rental ID: ")
            try:
                rental_id = int(rental_id_str)
            except ValueError:
                print("Invalid Rental ID. Must be an integer.")
                continue

            actual_days = get_positive_int("Enter actual rental days: ")
            damage_note = get_input("Enter damage note (leave empty or 'none' if no damage): ")

            try:
                refund = system.return_vehicle(rental_id, actual_days, damage_note)
                print(f"Vehicle returned successfully. Refund of ₹{refund:.2f} credited to customer wallet.")
            except ValueError as e:
                print(f"Return Failed: {e}")

        elif choice == "6":
            print("\n--- View Rentals ---")
            rentals = system.list_rentals()
            if not rentals:
                print("No active or closed rentals in the system.")
            else:
                for r in rentals:
                    print(r)

        elif choice == "7":
            print("\nExiting system...")
            
            system.exit_system()
            
            gc.collect()
            print("Destructors fired. System shut down. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice! Please select a number from 1 to 7.")

if __name__ == "__main__":
    main()
