import json
import uuid
from cryptography.fernet import Fernet

class Vault:
    def __init__(self, encryption_key):
        """
        Initializes the vault with an encryption key.

        :param encryption_key: A key for encrypting/decrypting sensitive data.
        """
        self.encryption_key = encryption_key
        self.fernet = Fernet(encryption_key)
        self.data = {}

    def create_item(self, item_type, fields):
        """
        Creates a new item in the vault.

        :param item_type: The type of the item (e.g., 'Login', 'Credit Card').
        :param fields: A dictionary of fields (e.g., username, password, etc.).
        :return: The ID of the created item.
        """
        item_id = str(uuid.uuid4())
        encrypted_fields = {key: self.encrypt(value) for key, value in fields.items()}
        self.data[item_id] = {"type": item_type, "fields": encrypted_fields}
        print(f"Item created: {item_id}")
        return item_id

    def modify_item(self, item_id, fields):
        """
        Modifies an existing item in the vault.

        :param item_id: The ID of the item to modify.
        :param fields: A dictionary of fields to update.
        """
        if item_id not in self.data:
            print(f"Item {item_id} not found.")
            return

        encrypted_fields = {key: self.encrypt(value) for key, value in fields.items()}
        self.data[item_id]["fields"].update(encrypted_fields)
        print(f"Item {item_id} updated.")

    def delete_item(self, item_id):
        """
        Deletes an item from the vault.

        :param item_id: The ID of the item to delete.
        """
        if item_id in self.data:
            del self.data[item_id]
            print(f"Item {item_id} deleted.")
        else:
            print(f"Item {item_id} not found.")

    def retrieve_item(self, item_id):
        """
        Retrieves and decrypts an item from the vault.

        :param item_id: The ID of the item to retrieve.
        :return: The decrypted item or None if the item is not found.
        """
        if item_id not in self.data:
            print(f"Item {item_id} not found.")
            return None

        item = self.data[item_id]
        decrypted_fields = {key: self.decrypt(value) for key, value in item["fields"].items()}
        return {"type": item["type"], "fields": decrypted_fields}

    def list_items(self):
        """
        Lists all items in the vault.

        :return: A list of item IDs and types.
        """
        return [{"id": item_id, "type": item["type"]} for item_id, item in self.data.items()]

    def encrypt(self, plaintext):
        """
        Encrypts plaintext data.

        :param plaintext: The plaintext string to encrypt.
        :return: The encrypted string.
        """
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext):
        """
        Decrypts ciphertext data.

        :param ciphertext: The encrypted string to decrypt.
        :return: The decrypted string.
        """
        return self.fernet.decrypt(ciphertext.encode()).decode()

    def save_to_file(self, file_path):
        """
        Saves the vault data to a file.

        :param file_path: The path of the file to save to.
        """
        with open(file_path, "w") as file:
            json.dump(self.data, file)
        print(f"Vault saved to {file_path}.")

    def load_from_file(self, file_path):
        """
        Loads the vault data from a file.

        :param file_path: The path of the file to load from.
        """
        try:
            with open(file_path, "r") as file:
                self.data = json.load(file)
            print(f"Vault loaded from {file_path}.")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except json.JSONDecodeError:
            print(f"Invalid vault file format: {file_path}.")


# Example usage
if __name__ == "__main__":
    # Generate a key for encryption (use a secure storage mechanism for real apps)
    key = Fernet.generate_key()
    vault = Vault(key)

    # Create a new item
    item_id = vault.create_item("Login", {"username": "user1", "password": "pass123"})

    # Retrieve the item
    item = vault.retrieve_item(item_id)
    print("Retrieved item:", item)

    # Modify the item
    vault.modify_item(item_id, {"password": "newpass456"})

    # List all items
    print("Vault items:", vault.list_items())

    # Delete the item
    vault.delete_item(item_id)

    # Save vault to a file
    vault.save_to_file("vault.json")

    # Load vault from a file
    vault.load_from_file("vault.json")
