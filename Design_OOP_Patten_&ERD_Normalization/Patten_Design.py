"""""# Creational Design Patterns
# These patterns deal with object creation.
# (A) Singleton Pattern
# Ensures only one instance of a class exists."""

class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# obj1 = Singleton()
# obj2 = Singleton()

# print(obj1 is obj2)   # True

"""(B) Factory Pattern
Creates objects without exposing the creation logic."""

# class Shape:
#     def draw(self):
#         pass

# class Circle(Shape):
#     def draw(self):
#         print("Drawing Circle")

# class Square(Shape):
#     def draw(self):
#         print("Drawing Square")

# class ShapeFactory:
#     def get_shape(self, shape_type):
#         if shape_type == "circle":
#             return Circle()
#         elif shape_type == "square":
#             return Square()

# factory = ShapeFactory()
# shape = factory.get_shape("circle")
# shape.draw()

""""(C) Builder Pattern
Used to construct complex objects step-by-step."""

# class BurgerBuilder:
#     def __init__(self):
#         self.burger = {}

#     def add_bread(self):
#         self.burger['bread'] = 'sesame'
#         return self

#     def add_meat(self):
#         self.burger['meat'] = 'chicken'
#         return self

#     def build(self):
#         return self.burger

# burger = BurgerBuilder().add_bread().add_meat().build()
# print(burger)

"""""2. Structural Design Patterns
These patterns deal with class and object composition, making structures flexible.
(A) Adapter Pattern
Allows incompatible classes to work together."""

# class EuropeanPlug:
#     def connect_eu(self):
#         print("Using European plug")

# class USAdapter:
#     def __init__(self, plug):
#         self.plug = plug

#     def connect_us(self):
#         self.plug.connect_eu()

# plug = EuropeanPlug()
# adapter = USAdapter(plug)
# adapter.connect_us()


"""""(B) Decorator Pattern
Adds new features to an object without modifying its structure."""

# def make_uppercase(func):
#     def wrapper():
#         return func().upper()
#     return wrapper

# @make_uppercase
# def say_hello():
#     return "hello world"

# print(say_hello())


"""(C) Facade Pattern
Hides complex logic behind a simple interface."""

# class CPU:
#     def start(self): print("CPU started")

# class Memory:
#     def load(self): print("Memory loaded")

# class ComputerFacade:
#     def start_computer(self):
#         CPU().start()
#         Memory().load()

# pc = ComputerFacade()
# pc.start_computer()


"""""3. Behavioral Design Patterns
These patterns deal with communication between objects."""

# class Observer:
#     def update(self, msg):
#         print("Received:", msg)

# class Subject:
#     def __init__(self):
#         self.observers = []

#     def add(self, obs):
#         self.observers.append(obs)

#     def notify(self, msg):
#         for obs in self.observers:
#             obs.update(msg)

# s = Subject()
# s.add(Observer())
# s.notify("Data Updated")

""""(B) Strategy Pattern
Define multiple algorithms and let the user choose."""

# class Add:
#     def execute(self, a, b): return a + b

# class Multiply:
#     def execute(self, a, b): return a * b

# class Context:
#     def __init__(self, strategy):
#         self.strategy = strategy

#     def perform(self, a, b):
#         return self.strategy.execute(a, b)

# ctx = Context(Add())
# print(ctx.perform(5, 3))

# ctx = Context(Multiply())
# print(ctx.perform(5, 3))

""""(C) Command Pattern
Encapsulate a request as an object."""

class Light:
    def on(self): print("Light ON")
    def off(self): print("Light OFF")

class Command:
    def execute(self): pass

class TurnOn(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.off()

light = Light()
cmd = TurnOn(light)
cmd.execute()

"""""""""
⭐ Summary Table
Pattern Type	Name	Purpose
Creational	Singleton	One instance only
Creational	Factory	    Creates objects dynamically
Creational	Builder	    Build complex objects
Structural	Adapter	    Connect incompatible classes
Structural	Decorator	Add features dynamically
Structural	Facade	    Simplify system complexity
Behavioral	Observer	Notifies subscribers
Behavioral	Strategy	Switch algorithms
Behavioral	Command	    Encapsulate requests

"""

