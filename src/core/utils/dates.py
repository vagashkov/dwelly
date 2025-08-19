from datetime import date, timedelta


def daterange_generator(start_date: date, end_date: date):
    """Generates dates between start_date and end_date (inclusive)."""
    for counter in range(
            int(
                (end_date - start_date).days
            ) + 1
    ):
        yield start_date + timedelta(counter)
