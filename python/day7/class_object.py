'''
usecase
Imagine you are building a vehicle management system for a car rental company.

The class defines common attributes(brand,model,year) and behaviors(start engine, show info)
you can easily create multiple car objetcs and manage them withot repeating code
'''


#Define class
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

#create object for the class
car1 = Car("Toyata", "Camry", 2020)
car2 = Car("Honda","Civic",2019)
print(car1.brand) #output: Toyata
print(car1._owner)
car1.set_owner("Alice")
#print(car1.get_owner()) #output: Alice

car1.set_owner("Bob") #output: The car already has an owner: Alice
print(car1.get_owner()) #output: Bob



#Call methods on the subjects
car1.start_engine()
car1.show_info()

car2.start_engine()
car2.show_info()



#Another way to call methods on the objects using a list of cars
cars = [car1,car2]

for car in cars:
    car.start_engine()
    car.show_info()


