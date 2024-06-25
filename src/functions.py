class Functions:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    @staticmethod
    def max_value(a, b):
        return max(a, b)

    @staticmethod
    def min_value(a, b):
        return min(a, b)

    @staticmethod
    def power(base, exponent):
        return base ** exponent

    @staticmethod
    def mod(a, b):
        if b == 0:
            raise ValueError("Cannot perform modulo operation with zero.")
        return a % b