from datetime import date, datetime
from enum import Enum


class Helpers:
    @classmethod
    def get_validated_input(cls, question, validator_function):
        """
        Shows an input to the user based on the provided question and uses the validator function to verify if the user's answer can be accepted.
        """
        while True:
            value = input(question)

            try:
                validator_function(value)
                return value

            except (ValueError, TypeError) as error:
                print(f"Error: {error}")
                print("Please try again.\n")

    @staticmethod
    def get_optional_input(question: str, previous_value: str, validator_function):
        """
        Shows an input to the user with a default/previous value between []. If the user presses Enter without any character, it will return the previous value, otherwise it will use the provided validator function.
        """
        while True:
            value = input(
                f"{question} [{previous_value if len(str(previous_value)) <= 30 else "..."}]: "
            ).strip()
            # User has pressed Enter with an empty string, return the previous/default value.
            if not value:
                return previous_value

            try:
                validator_function(value)
                return value
            except (ValueError, TypeError) as error:
                print(f"Error: {error}")
                print("Please try again.\n")

    @staticmethod
    def display_table(headers: tuple, rows: list, attributes: tuple | None = None):
        """
        Show a table to the user based on the data given to it. Works with list of tuples and list of objects.
        """
        if not rows:
            print("No records found.")
            return

        # If attributes are given, extract them into rows.
        if attributes:
            rows = [tuple(getattr(row, attr) for attr in attributes) for row in rows]

        def format_value(value):
            if isinstance(value, datetime):
                return value.strftime("%d/%m/%Y %H:%M:%S")

            if isinstance(value, date):
                return value.strftime("%d/%m/%Y")

            if isinstance(value, Enum):
                return value.value.capitalize().replace("_", " ")

            return str(value) if value is not None else ""

        # Format all values before calculating column widths.
        rows = [tuple(format_value(value) for value in row) for row in rows]

        # Calculate column widths.
        widths = [
            max(
                len(str(headers[i])),
                max(len(row[i]) for row in rows),
            )
            for i in range(len(headers))
        ]

        # Using the previously obtained width, create headers
        header = " | ".join(f"{value:<{widths[i]}}" for i, value in enumerate(headers))

        separator = "-+-".join("-" * width for width in widths)

        print(header)
        print(separator)

        # Print each row and column using the width
        for row in rows:
            print(" | ".join(f"{value:<{widths[i]}}" for i, value in enumerate(row)))

    @staticmethod
    def header(title: str):
        print(
            f"\n==================================================================== {title} ===================================================================="
        )

    @staticmethod
    def format_datetime(value: datetime):
        return value.strftime("%d/%m/%Y %H:%M:%S")

    @staticmethod
    def format_date(value: date):
        return value.strftime("%d/%m/%Y")
