import secrets
from typing import Any

from faker import Faker

from demo import continent_contry_city_list, time_list

faker = Faker()


def get_random_ubication() -> dict[str, str]:
    ubication = secrets.choice(continent_contry_city_list)
    return {'continent': ubication['continent'], 'country': ubication['country'], 'city': ubication['city']}


def get_random_sex() -> str:
    return secrets.choice(['Male', 'Female', 'Other'])


def get_random_languaje() -> str:
    return secrets.choice(['Portugués (Brasil)', 'Español (Colombia)', 'Español (Argentina)'])


def get_random_time() -> dict[str, Any]:
    time = secrets.choice(time_list)
    return {'id': time['id'], 'hour': time['hour'], 'minute': time['minute'], 'part_of_day': time['part_of_day']}


def count_time() -> int:
    return len(time_list)


def get_initial_final_date() -> dict[str, Any]:
    initial_date = faker.date_time_this_decade(before_now=True, after_now=False)

    final_date = faker.date_between_dates(date_start=initial_date, date_end=None)

    return {'initial_date': initial_date, 'final_date': final_date}
