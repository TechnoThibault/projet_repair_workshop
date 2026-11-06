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

        # Generate the width of each column based on the length of the max value inside each of them
        widths = [
            max(
                len(str(headers[i])),
                max(len(str(row[i])) for row in rows),
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
            print(" | ".join(f"{value!s:<{widths[i]}}" for i, value in enumerate(row)))
