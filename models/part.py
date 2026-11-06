from datetime import datetime


class Part:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        unit_price: float,
        stock_quantity: int,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.unit_price = float(unit_price)
        self.stock_quantity = stock_quantity
        if created_at is None:
            created_at = datetime.now()
        self.created_at = created_at
        if updated_at is None:
            updated_at = datetime.now()
        self.updated_at = updated_at

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int):
        if not isinstance(id, int):
            raise TypeError("The ID must be a integer.")
        self.__id = id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        self.__name = name.strip()

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        self.__description = description.strip()

    @property
    def unit_price(self) -> float:
        return self.__unit_price

    @unit_price.setter
    def unit_price(self, unit_price: float):
        if isinstance(unit_price, bool) or not isinstance(unit_price, (int, float)):
            raise TypeError("Unit price must be a number.")

        if unit_price < 0:
            raise ValueError("Unit price cannot be negative.")

        self.__unit_price = float(unit_price)

    @property
    def stock_quantity(self) -> int:
        return self.__stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, stock_quantity: int):
        if isinstance(stock_quantity, bool) or not isinstance(stock_quantity, int):
            raise TypeError("Stock quantity must be an integer.")

        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

        self.__stock_quantity = stock_quantity

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        if not isinstance(created_at, datetime):
            raise TypeError("Created at must be a datetime object.")

        if created_at > datetime.now(created_at.tzinfo):
            raise ValueError("Creation date cannot be in the future.")

        self.__created_at = created_at

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime):
        if not isinstance(updated_at, datetime):
            raise TypeError("Updated at must be a datetime object.")

        if updated_at > datetime.now(updated_at.tzinfo):
            raise ValueError("Update date cannot be in the future.")

        if updated_at < self.__created_at:
            raise ValueError("Update date cannot be earlier than creation date.")

        self.__updated_at = updated_at

    @classmethod
    def valid_name(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")

    @classmethod
    def valid_description(cls, value):
        if not value.strip():
            raise ValueError("Description cannot be empty.")

    @classmethod
    def valid_unit_price(cls, value):
        try:
            value = float(value)
            if value < 0:
                raise ValueError("Unit price must be equal or greater than zero.")
        except ValueError:
            raise ValueError("Unit price must be a number")

    @classmethod
    def valid_stock_quantity(cls, value):
        try:
            value = int(value)
            if value < 0:
                raise ValueError("Stock quantity must be equal or greater than zero.")
        except ValueError:
            raise ValueError("Stock quantity must be an integer.")
