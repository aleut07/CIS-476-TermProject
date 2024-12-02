from vault import Vault
from clipboard import ClipboardManager
from encryptions import EncryptionManager
from password_strength import PasswordStrengthChecker
import os

# Constants for file storage
VAULT_FILE = "vault_data.json"
ENCRYPTION_KEY_FILE = "encryption_key.txt"

# Helper function to load or generate encryption key
def load_or_generate_key():
    if os.path.exists(ENCRYPTION_KEY_FILE):
        with open(ENCRYPTION_KEY_FILE, "r") as key_file:
            return key_file.read().encode()
    else:
        key = EncryptionManager().key
        with open(ENCRYPTION_KEY_FILE, "w") as key_file:
            key_file.write(key.decode())
        return key

def main():
    # Initialize components
    encryption_key = load_or_generate_key()
    encryption_manager = EncryptionManager(encryption_key)
    vault = Vault(encryption_key)
    clipboard_manager = ClipboardManager(clear_timeout=10)
    password_checker = PasswordStrengthChecker()

    # Load existing vault data if available
    if os.path.exists(VAULT_FILE):
        vault.load_from_file(VAULT_FILE)

    # Command-line interface
    while True:
        print("\nWelcome to MyPass Password Manager")
        print("1. Add a new item")
        print("2. Modify an item")
        print("3. Delete an item")
        print("4. View an item")
        print("5. Generate a strong password")
        print("6. List all items")
        print("7. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            # Add new item
            item_type = input("Enter item type (e.g., Login, Credit Card): ").strip()
            fields = {}
            print("Enter fields (key=value), type 'done' to finish:")
            while True:
                field_input = input("> ").strip()
                if field_input.lower() == "done":
                    break
                try:
                    key, value = field_input.split("=", 1)
                    fields[key.strip()] = value.strip()
                except ValueError:
                    print("Invalid format. Use key=value.")
            item_id = vault.create_item(item_type, fields)
            print(f"Item added successfully! ID: {item_id}")

        elif choice == "2":
            # Modify an item
            item_id = input("Enter the ID of the item to modify: ").strip()
            fields = {}
            print("Enter fields to update (key=value), type 'done' to finish:")
            while True:
                field_input = input("> ").strip()
                if field_input.lower() == "done":
                    break
                try:
                    key, value = field_input.split("=", 1)
                    fields[key.strip()] = value.strip()
                except ValueError:
                    print("Invalid format. Use key=value.")
            vault.modify_item(item_id, fields)

        elif choice == "3":
            # Delete an item
            item_id = input("Enter the ID of the item to delete: ").strip()
            vault.delete_item(item_id)

        elif choice == "4":
            # View an item
            item_id = input("Enter the ID of the item to view: ").strip()
            item = vault.retrieve_item(item_id)
            if item:
                print(f"Item Type: {item['type']}")
                for key, value in item["fields"].items():
                    print(f"{key}: {value}")
                # Copy to clipboard option
                if input("Copy any field to clipboard? (y/n): ").lower() == "y":
                    field_to_copy = input("Enter field name: ").strip()
                    if field_to_copy in item["fields"]:
                        clipboard_manager.copy_to_clipboard(item["fields"][field_to_copy])
                    else:
                        print(f"Field '{field_to_copy}' not found.")
            else:
                print("Item not found.")

        elif choice == "5":
            # Generate a strong password
            try:
                length = int(input("Enter desired password length (minimum 8): ").strip())
                password = password_checker.suggest_password(length)
                print("Generated password:", password)
                if input("Copy to clipboard? (y/n): ").lower() == "y":
                    clipboard_manager.copy_to_clipboard(password)
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif choice == "6":
            # List all items
            items = vault.list_items()
            if items:
                print("Vault Items:")
                for item in items:
                    print(f"ID: {item['id']}, Type: {item['type']}")
            else:
                print("No items in the vault.")

        elif choice == "7":
            # Save and exit
            vault.save_to_file(VAULT_FILE)
            print("Vault saved. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
