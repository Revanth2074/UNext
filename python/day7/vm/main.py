from car import Car
from ev import EV
from polymorphism import Overloadingdemo
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

ev1 = EV("Tesla", "Model S", 2022, 100)
ev1.start_engine()
ev1.charge_battery()




#Another way to call methods on the objects using a list of cars
cars = [car1,car2]

for car in cars:
    car.start_engine()
    car.show_info()


