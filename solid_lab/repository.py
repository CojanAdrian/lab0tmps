# D - Dependency Inversion Principle
# OrderService depends on the OrderRepository abstraction,
# so storage can be swapped (memory, file, database) without changing it.
# S - this class only stores orders.

from abc import ABC, abstractmethod


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order, total):
        """Store the order and its final total."""

    @abstractmethod
    def find(self, order_id):
        """Return the saved order, or None if it doesn't exist."""


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.orders = {}
        self.totals = {}

    def save(self, order, total):
        self.orders[order.order_id] = order
        self.totals[order.order_id] = total

    def find(self, order_id):
        return self.orders.get(order_id)
