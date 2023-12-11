from collections import UserDict
import re
from error_utils import input_error, validation_error, error_messages, validation_messages, ValidationError

phone_pattern = re.compile(r'\d{10}')

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        self.value = Field(name)

class Phone(Field):
    def __init__(self, phone):
        self.set_value(phone)

    @validation_error
    def set_value(self, phone):
        if not bool(phone_pattern.match(phone)):
            raise ValidationError(validation_messages["invalid_phone"])
        self.value = Field(phone)

class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    
    def get_str_name(self):
        return str(self.name)

    def get_str_phones(self):
        return list(map(str, self.phones))
        
    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)
        print(f"New phone for {self.name} was added successfully")

    @input_error
    def edit_phone(self, oldPhone, newPhone):
        str_phones = self.get_str_phones()
        if not oldPhone in str_phones:
            raise IndexError(f"{self.name}'s contact hasn't such phone")
        idx = str_phones.index(oldPhone)
        self.phones[idx] = Phone(newPhone)
        print(f"{self.name}'s phone was updated successfully")

    @input_error 
    def find_phone(self, phone):
        str_phones = self.get_str_phones()
        if not phone in str_phones:
            raise IndexError(f"{self.name}'s contact hasn't such phone")
        idx = str_phones.index(phone)
        return self.phones[idx]
    
    @input_error 
    def remove_phone(self, phone):  
        str_phones = self.get_str_phones()      
        if not phone in self.get_str_phones():
            raise IndexError(f"{self.name}'s contact hasn't such phone")
        idx = str_phones.index(phone)
        self.phones.pop(idx)
        print(f"{self.name}'s phone was removed successfully")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p.value) for p in self.phones)}"

class AddressBook(UserDict):
    def get_str_names(self):
        return list(map(str, self.data))
    
    def add_record(self, record):
        key = record.get_str_name()
        self.data[key] = record
        print(f"{key} was added to your contacts")

    @input_error
    def find(self, name):
        if not name in self.data:
            raise KeyError(error_messages["no_contact"])
        return self.data[name]

    @input_error
    def delete(self, name):
        if not name in self.data:
            raise KeyError(error_messages["no_contact"])
        del self.data[name]
        print(f"{name} was removed from your contacts")
