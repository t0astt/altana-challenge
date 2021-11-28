import time

import click

from api import create_app, db
from api.models import Company

application = create_app()


@application.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Company": Company,
    }


class DataLoader:
    """
    Class for loading data from a CSV file into a database
    """

    # Configurable batch size for importing database entries.
    # Decrease/increase depending on available system memory.
    # Higher values will result in less batching but higher memory requirements.
    _BATCH_SIZE = 500000

    def __init__(self, filepath: str):
        """
        Instantiate a new DataLoader
        :param filepath: Path to the CSV file to load data from
        """
        self.filepath = filepath

    def load(self) -> None:
        """
        Load data into the application database.
        """
        self._print_log("Starting data import...")
        start = time.time()

        # Drop and recreate table
        db.drop_all()
        db.create_all()

        # Initialize values to track items and batch numbers.
        i, x = 0, 0
        companies = []  # Initialize empty list to hold batched entries.
        for row in self._read_csv():
            self._print_log(f"Adding item {x + i} to batch {x // self._BATCH_SIZE}")
            companies.append(row)
            i += 1  # Increment to track added entry.

            if i == self._BATCH_SIZE:  # If batch size is reached, then insert the batch into the database.
                self._insert(data=companies)
                companies.clear()  # Clear the batch list to free memory.
                x += i  # Increment the batch count
                i = 0  # Reset the item count

        # Insert the remaining companies that didn't fit evenly into the last batch
        if companies:
            self._insert(data=companies)

        end = time.time()

        self._print_log(f"Data import complete! Added {x + i} entries in {round(end - start)} seconds!")

    @staticmethod
    def _insert(data: [dict]) -> None:
        """
        Insert data into the database
        :param data: List of dictionaries to insert into the database
        :return: None
        """
        db.engine.execute(Company.__table__.insert(),
                          data)

    def _read_csv(self) -> dict:
        """
        Generator function for processing CSV files
        :return: Dictionary representing a row in the CSV file
        """
        with open(self.filepath) as f:
            from csv import excel_tab
            from csv import DictReader

            reader = DictReader(f, dialect=excel_tab)
            for row in reader:
                yield row

    @staticmethod
    def _print_log(msg: str) -> None:
        """
        Print a standardized message
        :param msg: Message to print
        :return: None
        """

        print(f"[*] {msg}")


@application.cli.command("load")
@click.argument("filepath")
def load(filepath: str) -> None:
    """
    Load data into the application database.
    """
    loader = DataLoader(filepath=filepath)
    loader.load()
