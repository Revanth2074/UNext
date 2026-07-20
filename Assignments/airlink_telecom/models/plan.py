from abc import ABC, abstractmethod

class Plan(ABC):
    """
    Abstract Base Class for all plans.
    Handles general attributes, operator overloading, and validation.
    """
    company = "AirLink"
    id_prefix = ""
    activation_fee = 0.0
    auto_id_counter = 100

    def __init__(self, *args, **kwargs):
        # Determine arguments flexibly
        # Supports:
        #   Plan(monthly_price)
        #   Plan(name, data_per_day, monthly_price)
        #   Plan(monthly_price, name, data_per_day)
        
        name = "Default Plan"
        data_per_day = 0.0
        monthly_price = 0.0

        if len(args) == 1:
            monthly_price = args[0]
            name = kwargs.get("name", name)
            data_per_day = kwargs.get("data_per_day", data_per_day)
        elif len(args) == 3:
            name, data_per_day, monthly_price = args
        elif len(args) == 2:
            name, monthly_price = args
            data_per_day = kwargs.get("data_per_day", data_per_day)
        else:
            name = kwargs.get("name", name)
            data_per_day = kwargs.get("data_per_day", data_per_day)
            monthly_price = kwargs.get("monthly_price", monthly_price)

        self.name = name
        self.data_per_day = float(data_per_day)
        # Trigger setter validation
        self.monthly_price = float(monthly_price)

        # Generate unique plan_id using subclass counter
        if "plan_id" in kwargs:
            self.plan_id = kwargs["plan_id"]
        else:
            cls = self.__class__
            self.plan_id = f"{cls.id_prefix}{cls.auto_id_counter}"
            cls.auto_id_counter += 1

    @property
    def monthly_price(self) -> float:
        return self._monthly_price

    @monthly_price.setter
    def monthly_price(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Monthly price must be greater than 0.")
        self._monthly_price = float(value)

    @abstractmethod
    def bill(self, months: int) -> float:
        """Calculate the bill for a given number of months."""
        pass

    def __eq__(self, other) -> bool:
        if not isinstance(other, Plan):
            return NotImplemented
        return self.plan_id == other.plan_id

    def __lt__(self, other) -> bool:
        if not isinstance(other, Plan):
            return NotImplemented
        return self.monthly_price < other.monthly_price

    def __str__(self) -> str:
        data_info = f"{self.data_per_day}GB/day" if self.data_per_day > 0 else "No data"
        offer = getattr(self, "festival_offer", 0)
        offer_str = f" (Festival Offer: {offer}% off)" if offer > 0 else ""
        return f"{self.plan_id} [{self.name} - {data_info}] - ₹{self.monthly_price}/month{offer_str}"


class Prepaid(Plan):
    id_prefix = "PRE-"
    activation_fee = 0.0
    auto_id_counter = 101

    def bill(self, months: int) -> float:
        discount = getattr(self, "festival_offer", 0)
        base = self.monthly_price * months
        return base * (1 - discount / 100.0)


class Postpaid(Plan):
    id_prefix = "POST-"
    activation_fee = 100.0
    auto_id_counter = 201

    def bill(self, months: int) -> float:
        discount = getattr(self, "festival_offer", 0)
        base = self.monthly_price * months * 1.18
        return base * (1 - discount / 100.0)


class DataPack(Plan):
    id_prefix = "DATA-"
    activation_fee = 50.0
    auto_id_counter = 301

    def bill(self, months: int) -> float:
        discount = getattr(self, "festival_offer", 0)
        base = self.monthly_price * months + 50.0
        return base * (1 - discount / 100.0)
