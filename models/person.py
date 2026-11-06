import re
from datetime import date, datetime


class Person:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        phone_number: str,
        email: str,
        address: str,
        birth_date: date,
        created_at: datetime,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.birth_date = birth_date
        self.created_at = created_at

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.email}"

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

        if not re.fullmatch(r"\+?[0-9\s().-]{7,20}", phone_number):
            raise ValueError("Invalid phone number format.")
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
