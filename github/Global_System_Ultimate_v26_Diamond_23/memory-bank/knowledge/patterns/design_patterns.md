# Design Patterns (Global System Ultimate Synchronized Intelligence Edition)

## 1. Singleton (Python)
Use when you need exactly one instance of a class (e.g., Database Connection, Config Loader).

```python
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def connect(self):
        pass
```

## 2. Factory Method
Use when you don't know the exact types of objects your code needs to work with beforehand.

```python
class Dialog:
    def create_button(self):
        raise NotImplementedError

class WindowsDialog(Dialog):
    def create_button(self):
        return WindowsButton()

class WebDialog(Dialog):
    def create_button(self):
        return HTMLButton()
```

## 3. Strategy
Use when you want to define a family of algorithms, encapsulate each one, and make them interchangeable.

```python
class PaymentStrategy:
    def pay(self, amount): pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount): print(f"Paid {amount} via Card")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount): print(f"Paid {amount} via PayPal")
```
