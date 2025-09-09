import csv
from datetime import datetime

from src.db.session import db
from src.models.inflation import Inflation


def parse_date(date_str: str) -> tuple[int, int]:
    """Parse date string into year and month.

    Args:
        date_str: Date string in format YYYY/MM/DD

    Returns:
        tuple: (year, month)
    """
    date_obj = datetime.strptime(date_str, "%Y/%m/%d")
    return date_obj.year, date_obj.month


def populate_inflation_data():
    """Populate the inflation table with data from the CSV file."""
    csv_file_path = "assets/inflation.csv"

    # Get a database session
    session = db.session_local()

    try:
        # Read the CSV file
        with open(csv_file_path, "r") as file:
            csv_reader = csv.DictReader(file)

            # Process each row
            for row in csv_reader:
                # Parse the date
                year, month = parse_date(row["date"])

                # Convert target and inflation rate to float, handle empty values
                target = float(row["target"]) if row["target"] else None
                inflation_rate = float(row["inflation rate"]) if row["inflation rate"] else None

                # Create new Inflation record
                inflation_record = Inflation(
                    year=year,
                    month=month,
                    inflation_rate=inflation_rate,
                    target=target
                )

                # Add to session
                session.add(inflation_record)

            # Commit all records
            session.commit()
            print("Successfully populated inflation data")

    except Exception as e:
        print(f"Error populating inflation data: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    populate_inflation_data()
