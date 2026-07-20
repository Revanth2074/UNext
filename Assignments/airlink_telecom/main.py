import sys
import gc
from services.telecom_system import TelecomSystem

# Force UTF-8 encoding for stdout and stderr to handle the Indian Rupee symbol (₹) on Windows
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
    system = TelecomSystem(load_seed=True)

    while True:
        print("\n======= AIRLINK TELECOM PORTAL =======")
        print("1. Register subscriber")
        print("2. Add plan")
        print("3. View plans (sorted by price)")
        print("4. Activate a connection")
        print("5. Deactivate a connection")
        print("6. View connections")
        print("7. Exit (archive connections -> destructors fire)")
        
        choice = get_input("Enter choice: ")

        if choice == "1":
            print("\n--- Register Subscriber ---")
            name = get_input("Enter name: ")
            age = get_positive_int("Enter age: ")
            phone = get_input("Enter phone: ")
            mobile_no = get_input("Enter mobile number: ")
            id_proof = get_input("Enter ID proof (or 'none'): ")
            balance = get_positive_float("Enter initial balance: ₹")
            
            sub = system.register_subscriber(name, age, phone, mobile_no, id_proof, balance)
            print(f"Subscriber registered successfully! Generated ID: {sub.person_id}")

        elif choice == "2":
            print("\n--- Add Plan ---")
            print("Types: Prepaid, Postpaid, DataPack")
            plan_type = get_input("Enter plan type: ")
            name = get_input("Enter plan name: ")
            data_per_day = get_non_negative_float("Enter data per day (GB): ")
            monthly_price = get_positive_float("Enter monthly price: ₹")
            
            try:
                plan = system.add_plan(plan_type, name, data_per_day, monthly_price)
                print(f"Plan added successfully! Generated ID: {plan.plan_id}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            print("\n--- View Plans (Sorted by Price) ---")
            plans = system.list_plans()
            if not plans:
                print("No plans available in the system.")
            else:
                # Option 3 must print sorted(plans) (works because of Plan.__lt__)
                sorted_plans = sorted(plans)
                for p in sorted_plans:
                    print(p)

        elif choice == "4":
            print("\n--- Activate Connection ---")
            sub_id = get_input("Enter subscriber ID: ")
            plan_id = get_input("Enter plan ID: ")
            months = get_positive_int("Enter duration in months: ")
            
            try:
                conn = system.activate_connection(sub_id, plan_id, months)
                print(f"Connection activated successfully! Generated ID: {conn.connection_id}")
            except ValueError as e:
                print(f"Activation Refused: {e}")

        elif choice == "5":
            print("\n--- Deactivate Connection ---")
            conn_id_str = get_input("Enter connection ID: ")
            try:
                conn_id = int(conn_id_str)
            except ValueError:
                print("Invalid Connection ID. Must be an integer.")
                continue

            used_months = get_positive_int("Enter used months: ")
            port_out_input = get_input("Is this a port out request? (y/n): ").lower()
            port_out = port_out_input == "y" or port_out_input == "yes"

            try:
                refund = system.deactivate_connection(conn_id, used_months, port_out)
                print(f"Connection deactivated successfully. Refund of ₹{refund:.2f} credited to subscriber.")
            except ValueError as e:
                print(f"Deactivation Failed: {e}")

        elif choice == "6":
            print("\n--- View Connections ---")
            connections = system.list_connections()
            if not connections:
                print("No active or deactivated connections in the system.")
            else:
                for c in connections:
                    print(c)

        elif choice == "7":
            print("\nExiting system...")
            # Triggers connection destructors by clearing active connections in the system
            system.exit_system()
            # Explicitly invoke Python garbage collector to fire the __del__ methods immediately
            gc.collect()
            print("Destructors fired. System shut down. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice! Please select a number from 1 to 7.")

if __name__ == "__main__":
    main()
