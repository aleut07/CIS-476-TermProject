class Observer:
    def update(self, message):
        pass

class ExpiryObserver(Observer):
    def update(self, message):
        print(f"Notification: {message}")

class VaultNotifier:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

# Usage
notifier = VaultNotifier()
observer = ExpiryObserver()
notifier.register(observer)

notifier.notify("Your credit card has expired!")
