from cryptography.fernet import Fernet


class EncryptionManager:
    def __init__(self, key=None):
        """
        Initializes the EncryptionManager.

        :param key: An encryption key. If None, a new key is generated.
        """
        if key:
            self.key = key
        else:
            self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

    def encrypt(self, plaintext):
        """
        Encrypts plaintext data.

        :param plaintext: The plaintext string to encrypt.
        :return: The encrypted string.
        """
        if not isinstance(plaintext, str):
            raise ValueError("Plaintext must be a string.")
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext):
        """
        Decrypts ciphertext data.

        :param ciphertext: The encrypted string to decrypt.
        :return: The decrypted string.
        """
        if not isinstance(ciphertext, str):
            raise ValueError("Ciphertext must be a string.")
        return self.fernet.decrypt(ciphertext.encode()).decode()

    def get_key(self):
        """
        Returns the encryption key.

        :return: The encryption key as a string.
        """
        return self.key.decode()


# Example usage
if __name__ == "__main__":
    # Initialize encryption manager
    encryption_manager = EncryptionManager()

    # Display the generated encryption key
    print("Encryption Key:", encryption_manager.get_key())

    # Encrypt data
    plaintext = "SensitiveData123!"
    ciphertext = encryption_manager.encrypt(plaintext)
    print("Encrypted:", ciphertext)

    # Decrypt data
    decrypted = encryption_manager.decrypt(ciphertext)
    print("Decrypted:", decrypted)
