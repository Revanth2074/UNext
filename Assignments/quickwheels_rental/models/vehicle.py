from abc import ABC, abstractmethod

class Vehicle(ABC):
    """
    Abstract Base Class for all Vehicles.
    Handles general attributes, operator overloading, and daily rate validation.
    """
    company = "QuickWheels"
    id_prefix = ""
    deposit_days = 0
    auto_id_counter = 100

    def __init__(self, *args, **kwargs):
        # Flexible constructor:
        #   Vehicle(daily_rate)
        #   Vehicle(name, available, daily_rate)
        #   Vehicle(daily_rate, name, available)
        name = "Default Vehicle"
        available = True
        daily_rate = 0.0

        if len(args) == 1:
            daily_rate = args[0]
            name = kwargs.get("name", name)
            available = kwargs.get("available", available)
        elif len(args) == 3:
            name, available, daily_rate = args
        elif len(args) == 2:
            name, daily_rate = args
            available = kwargs.get("available", available)
        else:
            name = kwargs.get("name", name)
            available = kwargs.get("available", available)
            daily_rate = kwargs.get("daily_rate", daily_rate)

        self.name = name
        self.available = bool(available)
        # Trigger setter validation
        self.daily_rate = float(daily_rate)

        # Generate unique vehicle_id using subclass counter
        if "vehicle_id" in kwargs:
            self.vehicle_id = kwargs["vehicle_id"]
        else:
            cls = self.__class__
            self.vehicle_id = f"{cls.id_prefix}{cls.auto_id_counter}"
            cls.auto_id_counter += 1

    @property
    def daily_rate(self) -> float:
        return self._daily_rate

    @daily_rate.setter
    def daily_rate(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Daily rate must be greater than 0.")
        self._daily_rate = float(value)

    @abstractmethod
    def rental_cost(self, days: int) -> float:
        """Calculate the rental cost for a given number of days."""
        pass

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self.vehicle_id == other.vehicle_id

    def __lt__(self, other) -> bool:
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self.daily_rate < other.daily_rate

    def __str__(self) -> str:
        status_str = "Available" if self.available else "Rented"
        offer = getattr(self, "festival_offer", 0)
        offer_str = f" (Festival Offer: {offer}% off)" if offer > 0 else ""
        return f"{self.vehicle_id} [{self.name} ({status_str})] - ₹{self.daily_rate}/day{offer_str}"


class Bike(Vehicle):
    id_prefix = "B-"
    deposit_days = 1
    auto_id_counter = 101

    def rental_cost(self, days: int) -> float:
        discount = getattr(self, "festival_offer", 0)
        base = self.daily_rate * days
        return base * (1 - discount / 100.0)


class Car(Vehicle):
    id_prefix = "C-"
    deposit_days = 2
    auto_id_counter = 201

    def rental_cost(self, days: int) -> float:
        discount = getattr(self, "festival_offer", 0)
        base = self.daily_rate * days * 1.05
        return base * (1 - discount / 100.0)


class SUV(Vehicle):
    id_prefix = "S-"
    deposit_days = 3
    auto_id_counter = 301

    def rental_cost(self, days: int) -> float:
        discount = getattr(self, "festival_offer", 0)
        base = self.daily_rate * days + 500.0
        return base * (1 - discount / 100.0)
