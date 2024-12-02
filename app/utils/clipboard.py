import pyperclip
import threading
import time

class ClipboardManager:
    def __init__(self, clear_timeout=10):
        """
        Initializes the ClipboardManager.

        :param clear_timeout: Duration (in seconds) after which the clipboard is cleared.
        """
        self.clear_timeout = clear_timeout
        self.clear_timer = None

    def copy_to_clipboard(self, data):
        """
        Copies the given data to the clipboard and starts a timer to clear it.

        :param data: The sensitive data to copy to the clipboard.
        """
        pyperclip.copy(data)
        print(f"Copied to clipboard: {data[:4]}{'*' * (len(data) - 4)}")  # Masked preview

        # Cancel any existing timer
        if self.clear_timer and self.clear_timer.is_alive():
            self.clear_timer.cancel()

        # Start a new timer to clear the clipboard
        self.clear_timer = threading.Timer(self.clear_timeout, self.clear_clipboard)
        self.clear_timer.start()

    def clear_clipboard(self):
        """
        Clears the clipboard contents for security purposes.
        """
        pyperclip.copy("")  # Clears the clipboard
        print("Clipboard cleared.")

    def set_clear_timeout(self, timeout):
        """
        Updates the timeout for clearing the clipboard.

        :param timeout: New timeout duration in seconds.
        """
        self.clear_timeout = timeout
        print(f"Clipboard clear timeout set to {timeout} seconds.")


# Example usage
if __name__ == "__main__":
    clipboard_manager = ClipboardManager(clear_timeout=5)

    # Copy sensitive data
    clipboard_manager.copy_to_clipboard("SensitivePassword123!")

    # Change timeout (optional)
    clipboard_manager.set_clear_timeout(10)

    # Keep the script running to observe the timer
    time.sleep(15)
