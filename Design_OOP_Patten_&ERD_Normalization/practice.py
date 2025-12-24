# Adapter Pattern in Real Software How it work Pyment System
# class PayPal:
#     def send_payment(self, amount):
#         print(f"PayPal payment: {amount}")

# class Stripe:
#     def make_payment(self, amount):
#         print(f"Stripe payment: {amount}")

# class PayPalAdapter:
#     def __init__(self, paypal):
#         self.paypal = paypal
#     def pay(self, amount):
#         self.paypal.send_payment(amount)

# class StripeAdapter:
#     def __init__(self, stripe):
#         self.stripe = stripe
#     def pay(self, amount):
#         self.stripe.make_payment(amount)

# # Client code uses same interface
# payments = [PayPalAdapter(PayPal()), StripeAdapter(Stripe())]
# for payment in payments:
#     payment.pay(100)

# builder patten

# class Student:
#     def __init__(self, name, age=None, email=None, phone=None):
#         self.name = name
#         self.age = age
#         self.email = email
#         self.phone = phone

#     def __str__(self):
#         return f"Student(name={self.name}, age={self.age}, email={self.email}, phone={self.phone})"


# class StudentBuilder:
#     def __init__(self, name):
#         self.name = name
#         self.age = None
#         self.email = None
#         self.phone = None

#     def set_age(self, age):
#         self.age = age
#         return self

#     def set_email(self, email):
#         self.email = email
#         return self

#     def set_phone(self, phone):
#         self.phone = phone
#         return self

#     def build(self):
#         return Student(self.name, self.age, self.email, self.phone)


# # Usage
# student = (
#     StudentBuilder("Raihan")
#     .set_age(22)
#     .set_email("raihan@example.com")
#     .set_phone("123456789")
#     .build()
# )

# print(student)

age = 10

if age > 18:
    print("You are eligible to vote.")
else:
    print("You are not eligible to vote.")
