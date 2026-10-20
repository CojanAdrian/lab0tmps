# S - Single Responsibility Principle
# These classes only hold order data.
# They do NOT calculate prices, save orders or send messages.


class OrderItem:
    def __init__(self, name, price, quantity):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1")

        self.name = name
        self.price = price
        self.quantity = quantity


class Order:
    def __init__(self, order_id, customer_name, customer_contact):
        self.order_id = order_id
        self.customer_name = customer_name
        self.customer_contact = customer_contact
        self.items = []

    def add_item(self, item):
        self.items.append(item)
