# builder.py
import random
import string

class PasswordBuilder:
    def __init__(self):
        self._length = 12
        self._include_upper = True
        self._include_numbers = True
        self._include_symbols = True

    def set_length(self, length):
        self._length = length
        return self

    def include_uppercase(self, include):
        self._include_upper = include
        return self

    def include_numbers(self, include):
        self._include_numbers = include
        return self

    def include_symbols(self, include):
        self._include_symbols = include
        return self

    def build(self):
        characters = string.ascii_lowercase
        if self._include_upper:
            characters += string.ascii_uppercase
        if self._include_numbers:
            characters += string.digits
        if self._include_symbols:
            characters += string.punctuation

        return ''.join(random.choice(characters) for _ in range(self._length))

# Usage
builder = PasswordBuilder()
strong_password = builder.set_length(16).include_symbols(True).build()
print("Generated Password:", strong_password)
