from functools import reduce


# https://mathieularose.com/function-composition-in-python/
def compose(*fns):
    return reduce(lambda f, g: lambda x: f(g(x)), fns, lambda x: x)


def convert_band(business: dict, key: str, not_found_key: str, bands: dict) -> dict:
    initial_value = business[key]
    not_found_msg = f'No {not_found_key} could be found.'
    description = bands.get(initial_value, not_found_msg)
    return {**business, key: f'{initial_value} - {description}'}