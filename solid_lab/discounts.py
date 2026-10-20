# O - Open/Closed Principle
# To add a new discount, create a new class that inherits from Discount.
# No existing code has to be changed.

from abc import ABC, abstractmethod


class Discount(ABC):
    @abstractmethod
    def amount(self, subtotal):
        """Return how much money to take off the subtotal."""


class NoDiscount(Discount):
    def amount(self, subtotal):
        return 0


class PercentageDiscount(Discount):
    def __init__(self, percent):
        if percent < 0 or percent > 100:
            raise ValueError("Percent must be between 0 and 100")
        self.percent = percent

    def amount(self, subtotal):
        return subtotal * self.percent / 100


class FixedAmountDiscount(Discount):
    def __init__(self, value):
        if value < 0:
            raise ValueError("Discount value cannot be negative")
        self.value = value

    def amount(self, subtotal):
        # Never take off more than the subtotal itself
        return min(self.value, subtotal)
