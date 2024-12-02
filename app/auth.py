import hashlib

class UserSession:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserSession, cls).__new__(cls)
            cls._instance.user = None
        return cls._instance

    def login(self, email, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if self._validate_credentials(email, hashed_password):
            self.user = email
            print("Logged in successfully!")
        else:
            print("Invalid credentials.")

    def logout(self):
        self.user = None
        print("Logged out.")

    def _validate_credentials(self, email, hashed_password):
        # Logic to check the credentials from a database
        return True  # Placeholder
