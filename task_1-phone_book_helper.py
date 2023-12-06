import re

phone_pattern = re.compile(r'^\+?\d{1,4}?[-. ]?\(?\d{1,}\)?[-. ]?\d{1,}[-. ]?\d{1,}$')

def is_valid_phone_number(phone_number):
    return bool(phone_pattern.match(phone_number))

# Custom exceptions
class NoCommandError(Exception):
    pass

class NoNameError(Exception):
    pass

class NoNameAndPhoneError(Exception):
    pass

class NoContactsError(Exception):
    pass

class NoContactError(Exception):
    pass

class InvalidPhoneError(Exception):
    pass

# decorator for error handling
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoCommandError:
            return "Enter some command please."
        except NoNameError:
            return "Give me name please."
        except NoNameAndPhoneError:
            return "Give me name and phone please."
        except NoContactError:
            return "There is no such contact in your phone book."
        except NoContactsError:
            return "There are no contacts in your phone book yet."

    return inner

# decorator for validation handling
def validation_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidPhoneError:
            return "The phone entered is not valid."

    return inner

@input_error
def parse_input(user_input):
    if not len(user_input):
        raise NoCommandError
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
@validation_error
def add_contact(args, contacts):
    if len(args) < 2:
        raise NoNameAndPhoneError
    name, phone = args
    if not is_valid_phone_number(phone):
        raise InvalidPhoneError
    contacts[name] = phone
    return "Contact added."

@input_error
@validation_error
def change_contact(args, contacts):
    if len(args) < 2:
        raise NoNameAndPhoneError
    name, phone = args
    if not is_valid_phone_number(phone):
        raise InvalidPhoneError
    if not name in contacts:
        raise NoContactError
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone_by_user(args, contacts):
    if len(args) == 0:
        raise NoNameError
    name = args[0]
    if not name in contacts:
        raise NoContactError
    return contacts[name]

@input_error
def show_all(contacts):
    if not len(contacts):
        raise NoContactsError
    contacts_to_display = ''
    for name, phone in contacts.items():
        contacts_to_display += '{:<10}: {:}\n'.format(name, phone)
    return contacts_to_display.strip()

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone_by_user(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()