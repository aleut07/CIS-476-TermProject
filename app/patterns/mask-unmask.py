class SensitiveDataProxy:
    def __init__(self, real_data):
        self._real_data = real_data
        self._is_masked = True

    def get_data(self):
        if self._is_masked:
            return '*' * len(self._real_data)
        return self._real_data

    def toggle_mask(self):
        self._is_masked = not self._is_masked

# Usage
credit_card = SensitiveDataProxy("1234-5678-9876-5432")
print("Masked:", credit_card.get_data())  # Output: Masked: ****************
credit_card.toggle_mask()
print("Unmasked:", credit_card.get_data())  # Output: Unmasked: 1234-5678-9876-5432
