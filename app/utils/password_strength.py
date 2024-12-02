import re

class PasswordStrengthChecker:
    def __init__(self, min_length=8, require_upper=True, require_lower=True, require_digit=True, require_special=True):
        """
        Initializes the PasswordStrengthChecker.

        :param min_length: Minimum length of the password.
        :param require_upper: Whether at least one uppercase letter is required.
        :param require_lower: Whether at least one lowercase letter is required.
        :param require_digit: Whether at least one digit is required.
        :param require_special: Whether at least one special character is required.
        """
        self.min_length = min_length
        self.require_upper = require_upper
        self.require_lower = require_lower
        self.require_digit = require_digit
        self.require_special = require_special

    def check_strength(self, password):
        """
        Checks the strength of the provided password.

        :param password: The password to evaluate.
        :return: A dictionary with 'is_strong' (bool) and a list of 'issues' (str).
        """
        issues = []

        if len(password) < self.min_length:
            issues.append(f"Password must be at least {self.min_length} characters long.")

        if self.require_upper and not any(char.isupper() for char in password):
            issues.append("Password must include at least one uppercase letter.")

        if self.require_lower and not any(char.islower() for char in password):
            issues.append("Password must include at least one lowercase letter.")

        if self.require_digit and not any(char.isdigit() for char in password):
            issues.append("Password must include at least one digit.")

        if self.require_special and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            issues.append("Password must include at least one special character (e.g., !@#$%^&*).")

        is_strong = len(issues) == 0
        return {"is_strong": is_strong, "issues": issues}

    def suggest_password(self, length=12):
        """
        Generates a strong password with the specified length.

        :param length: The desired length of the password.
        :return: A strong password string.
        """
        import random
        import string

        if length < self.min_length:
            raise ValueError(f"Password length must be at least {self.min_length} characters.")

        characters = string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>"
        password = "".join(random.choices(characters, k=length))

        # Ensure the password meets all requirements
        if self.require_upper:
            password = self._replace_random(password, random.choice(string.ascii_uppercase))
        if self.require_lower:
            password = self._replace_random(password, random.choice(string.ascii_lowercase))
        if self.require_digit:
            password = self._replace_random(password, random.choice(string.digits))
        if self.require_special:
            password = self._replace_random(password, random.choice("!@#$%^&*(),.?\":{}|<>"))

        return password

    @staticmethod
    def _replace_random(password, replacement):
        """
        Replaces a random character in the password with the specified replacement.

        :param password: The original password string.
        :param replacement: The replacement character.
        :return: The modified password string.
        """
        import random
        password = list(password)
        index = random.randint(0, len(password) - 1)
        password[index] = replacement
        return "".join(password)


# Example usage
if __name__ == "__main__":
    checker = PasswordStrengthChecker()

    # Check password strength
    password = "WeakPass"
    result = checker.check_strength(password)
    if result["is_strong"]:
        print("Password is strong.")
    else:
        print("Password is weak. Issues:")
        for issue in result["issues"]:
            print("-", issue)

    # Generate a strong password
    print("Generated strong password:", checker.suggest_password(12))
