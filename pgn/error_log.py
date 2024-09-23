
class ErrorLog:
    def __init__(self):
        self.__errors: (int, str) = []

    def add_error(self, line_number: int = -1, error_msg: str = ""):
        self.__errors.append((line_number, error_msg))

    def has_errors(self):
        return len(self.__errors)

    def print_errors(self):
        for next_error in self.__errors:
            print(next_error)