from models.part import Part


class RepairPart:
    def __init__(self, part: Part, quantity: int, unit_price: float):
        self.part = part
        self.quantity = quantity
        self.unit_price = unit_price

    @property
    def part(self) -> Part:
        return self.__part

    @part.setter
    def part(self, part: Part):
        if not isinstance(part, Part):
            raise TypeError("Part must be a Part instance.")
        self.__part = part

    @property
    def quantity(self) -> int:
        return self.__quantity

    @quantity.setter
    def quantity(self, quantity: int):
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        self.__quantity = quantity

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
