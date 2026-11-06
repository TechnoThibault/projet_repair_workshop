import re
from datetime import date, datetime


class Person:
    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        phone_number: str,
        email: str,
        address: str,
        birth_date: date,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.birth_date = birth_date
        if created_at is None:
            created_at = datetime.now()
        self.created_at = created_at

    def __str__(self):
        return f"\n - First name: {self.first_name}\n - Last name: {self.last_name}\n - Phone number: {self.phone_number}\n - Email: {self.email}"

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int):
        if not isinstance(id, int):
            raise TypeError("The ID must be a integer.")
        self.__id = id

    @property
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name: str):
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("First name must be a non-empty string.")
        self.__first_name = first_name

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name: str):
        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("Last name must be a non-empty string.")
        self.__last_name = last_name

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, phone_number: str):
        if not isinstance(phone_number, str):
            raise TypeError("Phone number must be a string.")

        if not re.fullmatch(r"\+?[0-9\s()-]{8,20}", phone_number):
            raise ValueError(
                "Invalid phone number. Please enter a valid phone number "
                "(e.g. +32 470 12 34 56)."
            )
        self.__phone_number = phone_number

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str):
        if not isinstance(email, str):
            raise TypeError("Email must be a string.")

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise ValueError("Invalid email address.")
        self.__email = email

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, address: str):
        if not isinstance(address, str) or not address.strip():
            raise ValueError("Address must be a non-empty string.")
        self.__address = address

    @property
    def birth_date(self) -> date:
        return self.__birth_date

    @birth_date.setter
    def birth_date(self, birth_date: date):
        if not isinstance(birth_date, date):
            raise TypeError("Birth date must be a datetime object.")

        if birth_date > datetime.now().date():
            raise ValueError("Birth date cannot be in the future.")

        self.__birth_date = birth_date

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        if not isinstance(created_at, datetime):
            raise TypeError("Created at must be a datetime object.")

        if created_at > datetime.now():
            raise ValueError("Creation date cannot be in the future.")
        self.__created_at = created_at

    @classmethod
    def validate_first_name(cls, value):
        if not value.strip():
            raise ValueError("First name cannot be empty.")

    @classmethod
    def validate_last_name(cls, value):
        if not value.strip():
            raise ValueError("Last name cannot be empty.")

    @classmethod
    def validate_email(cls, value):
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("Invalid email address.")

    @classmethod
    def validate_phone_number(cls, value):
        if not re.fullmatch(r"\+?[0-9\s()-]{8,20}", value):
            raise ValueError("Invalid phone number.")

    @classmethod
    def validate_address(cls, value):
        if not value.strip():
            raise ValueError("The address cannot")

    @classmethod
    def validate_birth_date(cls, value):
        try:
            valid_date = datetime.strptime(value, "%d/%m/%Y")
            if valid_date.date() >= datetime.now().date():
                raise ValueError("Invalid date format.")
        except ValueError:
            raise ValueError("Invalid date format.")
