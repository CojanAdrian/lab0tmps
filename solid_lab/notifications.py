# D - Dependency Inversion Principle
# OrderService depends on the Notifier abstraction, not on Email or SMS directly.
# S - each notifier only knows how to send one kind of message.

from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, recipient, message):
        """Send a message to the recipient."""


class EmailNotifier(Notifier):
    def send(self, recipient, message):
        print(f"[EMAIL to {recipient}] {message}")


class SmsNotifier(Notifier):
    def send(self, recipient, message):
        print(f"[SMS to {recipient}] {message}")
