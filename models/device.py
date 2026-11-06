from datetime import datetime

from models.customer import Customer


class Device:
    def __init__(
        self,
        id: int,
        customer: Customer,
        brand: str,
        model: str,
        serial_number: str,
        device_type: str,
        created_at: datetime,
    ):
        self.id = id
        self.customer = customer
        self.brand = brand
        self.model = model
        self.serial_number = serial_number
        self.device_type = device_type
        self.created_at = created_at

    def __str__(self) -> str:
        return (
            f"{self.brand} {self.model} | Serial: {self.serial_number} | Device type: {self.device_type} | Created: {self.created_at}\n"
            f"    │\n"
            f"    └── Customer: {self.customer}"
        )

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int):
        if not isinstance(id, int):
            raise TypeError("The ID must be a integer.")
        self.__id = id

    @property
    def customer(self) -> Customer:
        return self.__customer

    @customer.setter
    def customer(self, customer: Customer):
        if not isinstance(customer, Customer):
            raise TypeError("Customer must be a Customer instance.")
        self.__customer = customer

    @property
    def brand(self) -> str:
        return self.__brand

    @brand.setter
    def brand(self, brand: str):
        if not isinstance(brand, str) or not brand.strip():
            raise ValueError("Brand must be a non-empty string.")
        self.__brand = brand.strip()

    @property
    def model(self) -> str:
        return self.__model

    @model.setter
    def model(self, model: str):
        if not isinstance(model, str) or not model.strip():
            raise ValueError("Model must be a non-empty string.")
        self.__model = model.strip()

    @property
    def serial_number(self) -> str:
        return self.__serial_number

    @serial_number.setter
    def serial_number(self, serial_number: str):
        if not isinstance(serial_number, str) or not serial_number.strip():
            raise ValueError("Serial number must be a non-empty string.")
        self.__serial_number = serial_number.strip()

    @property
    def device_type(self) -> str:
        return self.__device_type

    @device_type.setter
    def device_type(self, device_type: str):
        if not isinstance(device_type, str) or not device_type.strip():
            raise ValueError("Device type must be a non-empty string.")
        self.__device_type = device_type.strip()

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
