Laboratory Work No. 0. SOLID Principles

Course: Software Design Techniques and Mechanisms (TMPS)

Student: ____________________

Group: ________

Verified by: Vasile Drumea, university assistant


1 Task

Implement 3 SOLID letters in a simple project.

I chose the Single Responsibility Principle (S), the Open/Closed Principle (O) and the Dependency Inversion Principle (D). The project is written in Python 3.11 without external libraries.


2 Theory

SOLID is a set of 5 OOP design principles that make code easier to understand, test and extend.

Single Responsibility Principle: a class should do only one thing, so it has only one reason to change.

Open/Closed Principle: a class should be open for extension but closed for modification. New behaviour is added by writing new code, not by editing the old one.

Dependency Inversion Principle: high-level classes should depend on abstractions, not on concrete classes. The concrete class is given from outside.


3 Project description

The program is a simple online shop checkout. For each order it calculates the subtotal, applies a discount, saves the order and sends a confirmation message to the customer.

The orders are written in main.py as test data. Orders are saved in a dictionary and the messages are printed to the console, because the goal of the lab is the structure of the code, not a real shop.

Files:

solid_lab/models.py - Order and OrderItem

solid_lab/pricing.py - PriceCalculator

solid_lab/discounts.py - Discount, NoDiscount, PercentageDiscount, FixedAmountDiscount

solid_lab/notifications.py - Notifier, EmailNotifier, SmsNotifier

solid_lab/repository.py - OrderRepository, InMemoryOrderRepository

solid_lab/order_service.py - OrderService

main.py - creates the objects and runs the program

tests/ - unit tests for each principle


4 Implementation

4.1 Single Responsibility Principle

Each class in the project has one job. Order and OrderItem only store data, PriceCalculator only calculates prices, InMemoryOrderRepository only stores orders, EmailNotifier and SmsNotifier only send messages, and OrderService only runs the checkout steps.

For example, the Order class only keeps data:

```
class Order:
    def __init__(self, order_id, customer_name, customer_contact):
        self.order_id = order_id
        self.customer_name = customer_name
        self.customer_contact = customer_contact
        self.items = []

    def add_item(self, item):
        self.items.append(item)
```

If Order also calculated the total, saved itself and sent emails, then any change in the email text or in the way orders are saved would mean editing this class. Now each change affects only one class.

4.2 Open/Closed Principle

Discounts are made with an abstract class Discount, and each discount type is a separate subclass:

```
class Discount(ABC):
    @abstractmethod
    def amount(self, subtotal):
        pass

class PercentageDiscount(Discount):
    def __init__(self, percent):
        self.percent = percent

    def amount(self, subtotal):
        return subtotal * self.percent / 100
```

PriceCalculator does not check which discount it received, it just calls amount():

```
def total(self, order, discount):
    subtotal = self.subtotal(order)
    result = subtotal - discount.amount(subtotal)
    return round(max(result, 0), 2)
```

Without this principle the calculator would have an if/elif for every discount type, and every new discount would mean editing it. In my project a new discount is just a new class. In tests/test_ocp.py I wrote a BuyOverHundredDiscount class only inside the test, and it works with PriceCalculator without changing it.

4.3 Dependency Inversion Principle

OrderService is the high-level class. It needs to save the order and send a message, but it does not create EmailNotifier or InMemoryOrderRepository by itself. It receives them through the constructor and only uses the methods of the abstract classes Notifier and OrderRepository:

```
class OrderService:
    def __init__(self, calculator, repository, notifier):
        self.calculator = calculator
        self.repository = repository
        self.notifier = notifier

    def checkout(self, order, discount):
        if not order.items:
            raise ValueError("Cannot checkout an empty order")

        total = self.calculator.total(order, discount)
        self.repository.save(order, total)
        self.notifier.send(order.customer_contact, "... Total: " + str(total))
        return total
```

The concrete classes are chosen in main.py:

```
email_service = OrderService(calculator, repository, EmailNotifier())
sms_service = OrderService(calculator, repository, SmsNotifier())
```

The same OrderService sends an email in one case and an SMS in the other, without any change in its code. To add a Telegram notifier or a database repository, I only need to write a new class and pass it in main.py.

In tests/test_dip.py I pass fake classes (FakeNotifier and FakeRepository) to OrderService, which shows that it depends only on the abstractions.

The difference between S and D in this project: S is about what is inside one class (one job), while D is about how classes are connected (OrderService is not tied to a specific notifier or repository). Creating different orders is just different data for the same class, so it is not an example of D. D is shown by swapping different classes, like EmailNotifier and SmsNotifier.


5 Results

Output of python main.py:

```
Subtotal: 1000
[EMAIL to ana@mail.com] Hi Ana, your order A-001 is confirmed. Total: 900.00 MDL

Subtotal: 3000
[SMS to +37360000000] Hi Ion, your order A-002 is confirmed. Total: 2900.00 MDL

Subtotal: 240
[EMAIL to maria@mail.com] Hi Maria, your order A-003 is confirmed. Total: 240.00 MDL
```

Output of python -m unittest:

```
Ran 11 tests in 0.000s

OK
```


6 Conclusion

In this laboratory work I implemented three SOLID principles in a small checkout program. Using SRP I split the program into small classes with one job each. Using OCP I made the discounts extensible, so a new discount does not require changes in the calculator. Using DIP I made OrderService depend on abstractions, so the notifier and the storage can be replaced from outside.

I understood that these principles do not change what the program does, but they make it easier to modify. When I wanted to add a new discount or a new notifier, I only had to write a new class without touching code that already worked. It also made testing easier, because I could replace real classes with fake ones.
