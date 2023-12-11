import re
from error_utils import input_error, validation_error, error_messages, validation_messages, ValidationError

phone_pattern = re.compile(r'^\+?\d{1,4}?[-. ]?\(?\d{1,}\)?[-. ]?\d{1,}[-. ]?\d{1,}$')

def is_valid_phone_number(phone_number):
    return bool(phone_pattern.match(phone_number))

@input_error
def parse_input(user_input):
    if not len(user_input):
        raise ValueError(error_messages["no_command"])
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
@validation_error
def add_contact(args, contacts):
    if len(args) < 2:
        raise ValueError(error_messages["no_name_and_phone"])
    name, phone = args
    if not is_valid_phone_number(phone):
        raise ValidationError(validation_messages["invalid_phone"])
    contacts[name] = phone
    return "Contact added."

@input_error
@validation_error
def change_contact(args, contacts):
    if len(args) < 2:
        raise ValueError(error_messages["no_name_and_phone"])
    name, phone = args
    if not is_valid_phone_number(phone):
        raise ValidationError(validation_messages["invalid_phone"])
    if not name in contacts:
        raise IndexError(error_messages["no_contact"])
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone_by_user(args, contacts):
    if len(args) == 0:
        raise ValueError(error_messages["no_name"])
    name = args[0]
    if not name in contacts:
        raise IndexError(error_messages["no_contact"])
    return contacts[name]

@input_error
def show_all(contacts):
    if not len(contacts):
        raise IndexError(error_messages["no_contacts"])
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