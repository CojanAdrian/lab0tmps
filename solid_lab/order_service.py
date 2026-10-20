# D - Dependency Inversion Principle
# OrderService is the high-level logic. It receives its helpers from outside
# (through the constructor) and only uses their abstract methods.
# It never creates EmailNotifier or InMemoryOrderRepository itself.


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
        self.notifier.send(
            order.customer_contact,
            f"Hi {order.customer_name}, your order {order.order_id} is confirmed. Total: {total:.2f} MDL",
        )
        return total
