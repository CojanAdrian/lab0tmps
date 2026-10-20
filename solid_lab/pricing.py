# S - this class only calculates prices.
# O - it works with ANY Discount, so new discounts don't require changes here.


class PriceCalculator:
    def subtotal(self, order):
        total = 0
        for item in order.items:
            total += item.price * item.quantity
        return total

    def total(self, order, discount):
        subtotal = self.subtotal(order)
        result = subtotal - discount.amount(subtotal)
        return round(max(result, 0), 2)
