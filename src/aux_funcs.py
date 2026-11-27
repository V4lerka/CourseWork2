import pycountry

def normalize_country(name) -> str | None:
    """Пытается найти страны по названию при вводе названий стран с небольшими ошибками"""
    try:
        country = pycountry.countries.lookup(name)
        return country.name
    except LookupError:
        pass

    try:
        matches = pycountry.countries.search_fuzzy(name)
        return matches[0].name
    except LookupError:
        return None