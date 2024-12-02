class Handler:
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, request):
        if self._successor:
            return self._successor.handle(request)

class SecurityQuestionHandler(Handler):
    def __init__(self, question, answer, successor=None):
        super().__init__(successor)
        self._question = question
        self._answer = answer

    def handle(self, request):
        response = input(f"{self._question}: ")
        if response.strip().lower() == self._answer.lower():
            return super().handle(request)
        else:
            print("Incorrect answer.")
            return False

# Usage
handler1 = SecurityQuestionHandler("What is your mother's maiden name?", "Smith")
handler2 = SecurityQuestionHandler("What is your first pet's name?", "Buddy", handler1)
handler3 = SecurityQuestionHandler("What is your favorite color?", "Blue", handler2)

if handler3.handle("Recover Password"):
    print("Security check passed. You can now reset your password.")
else:
    print("Failed security check.")
