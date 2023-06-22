import datetime
from typing import Generator


def iter_dates(starting_date: datetime.date,
               ending_date: datetime.date) -> Generator[datetime.date,
                                                        None,
                                                        None]:
    """
    Iterate over two dates
    :param starting_date: initial date
    :param ending_date: ending date
    :return: each date between the two dates
    """
    for day in iter_days(starting_date=starting_date, ending_date=ending_date):
        yield starting_date + datetime.timedelta(days=day)


def iter_days(starting_date: datetime.date,
              ending_date: datetime.date) -> Generator[int, None, None]:
    """
    Iterate the days over two dates
    :param starting_date: initial date
    :param ending_date: ending date
    :return: relative day numbers between the two dates
    """
    for day in range(int((ending_date - starting_date).days) + 1):
        yield day
