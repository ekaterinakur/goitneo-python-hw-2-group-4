# -- Custom error messages
error_messages = {
    "no_command": "Enter some command please.",
    "no_name": "Give me name please.",
    "no_name_and_phone": "Give me name and phone please.",
    "no_contact": "There is no such contact in your phone book.",
    "no_contacts": "There are no contacts in your phone book yet.",
}

# decorator for error handling
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as err:
            print(err)

    return inner

# -- Validations
validation_messages = {
    "invalid_phone": "The phone entered is not valid."
}

class ValidationError(Exception):
    pass

# decorator for validation handling
def validation_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as err:
            print(err)

    return inner
