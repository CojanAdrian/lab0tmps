from solid_lab.models import Order, OrderItem
from solid_lab.discounts import NoDiscount, PercentageDiscount, FixedAmountDiscount
from solid_lab.pricing import PriceCalculator
from solid_lab.notifications import EmailNotifier, SmsNotifier
from solid_lab.repository import InMemoryOrderRepository
from solid_lab.order_service import OrderService


def main():
    calculator = PriceCalculator()
    repository = InMemoryOrderRepository()

    # Order 1: email notification, 10% discount  S Single Responsibility, "one job per person"
    order1 = Order("A-001", "Ana", "ana@mail.com")
    order1.add_item(OrderItem("Keyboard", 500, 1))
    order1.add_item(OrderItem("Mouse", 250, 2))

    # D Dependency Inversion, "plug in, don't hard-wire"
    email_service = OrderService(calculator, repository, EmailNotifier())
    print("Subtotal:", calculator.subtotal(order1))
    email_service.checkout(order1, PercentageDiscount(10))
    print()

    # Order 2: SMS notification, fixed 100 MDL discount
    order2 = Order("A-002", "Ion", "+37360000000")
    order2.add_item(OrderItem("Monitor", 3000, 1))

    sms_service = OrderService(calculator, repository, SmsNotifier())
    print("Subtotal:", calculator.subtotal(order2))
    sms_service.checkout(order2, FixedAmountDiscount(100))
    print()

    # Order 3: no discount   O Open/Closed, "add new things without changing old things"
    order3 = Order("A-003", "Maria", "maria@mail.com")
    order3.add_item(OrderItem("USB cable", 80, 3))

    print("Subtotal:", calculator.subtotal(order3))
    email_service.checkout(order3, NoDiscount())


if __name__ == "__main__":
    main()
