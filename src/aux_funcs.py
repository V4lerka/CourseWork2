import pycountry


def normalize_country(name: str) -> str | None:
    """Приводит имя страны к названию по ISO при вводе названий стран с небольшими ошибками или заменяет на
    название-синоним по ISO"""
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
