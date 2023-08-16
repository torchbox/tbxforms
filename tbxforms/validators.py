from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)


class StringMinValueValidator(MinValueValidator):
    def compare(self, a: str, b: str):
        try:
            return super().compare(int(a), int(b))
        except ValueError:
            return False


class StringMaxValueValidator(MaxValueValidator):
    def compare(self, a: str, b: str):
        try:
            return super().compare(int(a), int(b))
        except ValueError:
            return False
