from abc import ABC, abstractmethod
from collections import UserDict
from datetime import datetime as dtdt
import pickle


class AbstractBasic(ABC):
    @abstractmethod
    def show_contacts(self, contacts):
        pass

    @abstractmethod
    def show_commands(self, commands):
        pass


class ConsoleAbstract(AbstractBasic):
    def show_contacts(self, contacts):
        for contact in contacts:
            print(f"{contact['name']}: {', '.join(contact['phones'])}")

    def show_commands(self, commands):
        print("Available commands:")
        for command in commands:
            print(f"-{command}")


class WebAbstract(AbstractBasic):
    def show_contacts(self, contacts):
        # Implement displaying contacts in a web interface
        pass

    def show_commands(self, commands):
        # Implement displaying commands in a web interface
        pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if len(value) != 0:  # перевірка чи ім'я не порожнє
            super().__init__(value)
        else:
            raise ValueError("Enter your name")


class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():  # перевірка валідності номеру
            super().__init__(value)
        else:
            raise ValueError("Enter a valid phone number")


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = dtdt.strptime(value, "%d.%m.%Y")  # перевірка формату дати та перетворення на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):  # Функція додавання номера телефону
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):  # Функція видалення номера телефону
        for phone in self.phones:
            if phone.value == phone:
                self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):  # Функція редагування номера телефону
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                print(f"Contact phone numbe {old_phone} edited on {new_phone} ")

    def find_phone(self, phone):  # Функція знаходження номера телефону
        return [p for p in self.phones if p.value == phone]

    def add_birthday(self, birthday):  # Функція перевірки на наявність дня народження
        if self.birthday:
            raise ValueError("Birthday already set.")
        self.birthday = birthday  # Збереження дня народження

    def show_birthday(self):  # Функція перевірки на наявність дня народження
        if not self.birthday:
            raise ValueError("No birthday set.")
        return self.birthday.value.strftime("%d.%m.%Y")  # Виведення дня народження


class AddressBook(UserDict):
    def add_contact(self, args):  # Функція додавання контакту
        name, phone = args
        if name not in self.data:
            self.data[name] = Record(name)
        self.data[name].add_phone(phone)

    def change_contact(self, args):
        name, new_phone = args
        record = self.data.get(name)
        if record:
            old_phone = record.phones[0].value
            record.remove_phone(old_phone)
            record.add_phone(new_phone)
            return "Phone number updated."
        return "Contact not found."

    def show_phone(self, args):  # Функція пошуку  контакту
        name = args[0]
        record = self.data.get(name)
        if record:
            return record.phones[0].value
        return "Contact not found."

    def add_birthday(
        self, name, birthday
    ):  # Функція додавання дати народження до  контакту
        record = self.data.get(name)
        if record:
            record.add_birthday(birthday)
            return "Birthday added."
        else:
            return "Contact not found."

    def show_birthday(self, name):  # Функція,  яка показуємо день народження контакту
        record = self.data.get(name)
        if record and record.birthday:
            return record.show_birthday
        else:
            raise ValueError("Contact not found or no birthday set.")

    def birthdays(
        self,
    ):  # Функція яка повертає список користувачів, яких потрібно привітати по днях на наступному тижні
        upcoming_birthdays = (
            []
        )  # змінна для зберігання списку контактів яких потрібно привітати
        today = dtdt.combine(dtdt.today(), dtdt.min.time())  # отримання поточної дати
        for record in self.values():  # цикл перебору днів народження у всіх контактів
            if record.birthday:
                if (
                    record.birthday.value - today
                ).days <= 7:  # якщо день народження протягом наступних семи днів
                    upcoming_birthdays.append(
                        record.name.value
                    )  # додаємо контак у список
        return upcoming_birthdays  # повернення списку контактів

    def delete(self, name):  # Функція видалення запису за іменем
        if name in self.data:
            del self.data[name]

    def show_all(book):  # Функція відображення всіх контактів
        if not book.data:
            return "No contacts found."
        for name, record in book.data.items():
            print(f"{name}: {'; '.join(str(phone) for phone in record.phones)}")
        return ""


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command."
        except KeyError:
            return "No such name found "
        except IndexError:
            return "Not found"
        except Exception as e:
            return f"Error: {e}"

    return inner


def parse_input(
    user_input,
):  # функція розбивання введеного рядка на слова (використовує пробіл як розділювач )
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_birthday(args, book):
    name, birthday = args
    if name in book.data:
        book.data[name].add_birthday(birthday)
        return "Birthday added to contact."
    else:
        raise ValueError("Record not found or date of birth not set.")


@input_error
def show_birthday(args, book):
    name = args[0]
    if name in book.data and book.data[name].birthday:
        return f" Birthday:{book.data[name].birthday.value}"
    elif name in book.data:
        return "Birthday not set."
    else:
        return "Contact not found."


@input_error
def birthdays(args, book):
    if len(args) != 0:
        raise ValueError("Invalid command. Use birthdays.")
    return book.birthdays()


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

        # ГОЛОВНА ЛОГІКА #


if __name__ == "__main__":
    view = ConsoleAbstract()  # змінна для відображення інформації користувачу
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            book.add_contact(args)
            print("Contact added.")

        elif command == "change":
            print(book.change_contact(args))

        elif command == "phone":
            print(book.show_phone(args))

        elif command == "all":
            print(book.show_all())

        elif command == "add-birthday":
            name, birthday = args
            print(book.add_birthday(name, Birthday(birthday)))

        elif command == "show-birthday":
            name = args[0]
            print(book.show_birthday(name))

        elif command == "birthdays":
            print(book.birthdays())

        elif command == "help":  # відображення доступних команд
            view.show_commands(
                [
                    "close",
                    "exit",
                    "hello",
                    "add",
                    "change",
                    "phone",
                    "all",
                    "add_birthday",
                    "show-birthday",
                    "birthdays",
                ]
            )
        else:
            print("Invalid command.")
