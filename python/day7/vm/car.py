class Car:
    def __init__(self,brand,model,year,owner=None):
        self.brand = brand
        self.model = model
        self.year = year
        self._owner = owner # Private attribute to store the owner of the car

    def start_engine(self):
        print(f"The engine of the {self.brand} {self.model} is starting")

    def show_info(self):
        print(f"Car Info: {self.year} {self.brand} {self.model}")

    # Abstraction - Public methods to set and get the owner of the car
    def set_owner(self,owner):
        if not self._owner: # Check if the car already has an owner
            self._owner = owner # Set the owner of the car
        else:
            print(f"The car already has an owner: {self._owner}")

    def get_owner(self):
        return self._owner # Get the owner of the car
