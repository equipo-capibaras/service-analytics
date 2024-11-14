import secrets

from demo import continent_contry_city_list


def get_random_ubication() -> dict[str, str]:
    ubication = secrets.choice(continent_contry_city_list)
    return {'continent': ubication['continent'], 'country': ubication['country'], 'city': ubication['city']}


def get_random_sex() -> str:
    return secrets.choice(['Male', 'Female', 'Other'])


def get_random_languaje() -> str:
    return secrets.choice(['es', 'en', 'pt'])
