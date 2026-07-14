def logging_decorator(func):
    def wrapper():
        print("before calling the function")
        func()
        print("after calling the function")
    return wrapper

@logging_decorator
def say_hello():
    print("Hello!")
@logging_decorator
def say_goodbye():
    print("Goodbye!")
@logging_decorator
def say_welcome():
    print("Welcome!")