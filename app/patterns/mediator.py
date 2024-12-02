class Mediator:
    def __init__(self):
        self._components = {}

    def register_component(self, name, component):
        self._components[name] = component
        component.set_mediator(self)

    def notify(self, sender, event, data=None):
        if sender in self._components:
            if event == "login_success":
                self._components["vault"].show_vault()
            elif event == "add_item":
                self._components["vault"].add_item(data)
            elif event == "delete_item":
                self._components["vault"].delete_item(data)
            elif event == "generate_password":
                self._components["password_generator"].generate_password(data)
            elif event == "logout":
                self._components["auth"].logout()
            # Add more event handling as needed


class Component:
    def __init__(self):
        self._mediator = None

    def set_mediator(self, mediator):
        self._mediator = mediator


# Specific components

class AuthComponent(Component):
    def login(self, email, password):
        # Simulate login logic
        print(f"Logging in as {email}")
        # Notify mediator about the successful login
        self._mediator.notify("auth", "login_success")

    def logout(self):
        print("Logging out...")
        # Notify mediator about the logout event


class VaultComponent(Component):
    def show_vault(self):
        print("Vault is now visible.")

    def add_item(self, item):
        print(f"Adding item to vault: {item}")

    def delete_item(self, item_id):
        print(f"Deleting item with ID {item_id} from vault.")


class PasswordGeneratorComponent(Component):
    def generate_password(self, options):
        # Simulate password generation logic
        print(f"Generating password with options: {options}")
        generated_password = "StrongP@ssw0rd!"  # Placeholder
        print(f"Generated Password: {generated_password}")


# Example usage
if __name__ == "__main__":
    mediator = Mediator()

    # Create components
    auth = AuthComponent()
    vault = VaultComponent()
    password_generator = PasswordGeneratorComponent()

    # Register components with mediator
    mediator.register_component("auth", auth)
    mediator.register_component("vault", vault)
    mediator.register_component("password_generator", password_generator)

    # Simulate interactions
    auth.login("user@example.com", "password123")
    vault.add_item({"type": "Login", "username": "user1", "password": "pass123"})
    password_generator.generate_password({"length": 16, "include_symbols": True})
    auth.logout()
