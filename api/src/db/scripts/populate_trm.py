import csv
from datetime import datetime

from sqlalchemy.orm import Session
from src.db.session import database_session
from src.models.trm import TRM


def populate_trm_data(db: Session):
    """
    Populate TRM (Tasa Representativa del Mercado) data from CSV file.
    """
    try:
        with open("assets/trm.csv", "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                date = datetime.strptime(row["date"], "%Y/%m/%d").date()
                value = float(row["value"])

                trm_entry = TRM(
                    date=date,
                    value=value,
                )
                db.add(trm_entry)

        db.commit()
        print("TRM data populated successfully!")

    except FileNotFoundError:
        print("Error: trm.csv file not found in assets directory")
    except Exception as e:
        print(f"Error populating TRM data: {str(e)}")
        db.rollback()


if __name__ == "__main__":
    db = next(database_session.get_db())
    populate_trm_data(db)
