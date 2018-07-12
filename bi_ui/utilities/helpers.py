from functools import reduce
from flask import Markup


# https://mathieularose.com/function-composition-in-python/
def compose(*fns):
    return reduce(lambda f, g: lambda x: f(g(x)), fns, lambda x: x)


def convert_band(business: dict, key: str, not_found_key: str, bands: dict) -> dict:
    initial_value = business[key]
    not_found_msg = f'No {not_found_key} could be found.'
    description = bands.get(initial_value, not_found_msg)
    return {**business, key: f'{initial_value} - {description}'}


def highlight(business: dict, to_highlight: str) -> dict:
    original = business['BusinessName']
    # We need to use Markup so that Jinja will render our HTML properly
    new_name = Markup(original.replace(to_highlight.upper(), f'<em class="highlight">{to_highlight.upper()}</em>'))
    highlighted_business = {
        **business,
        "BusinessName": new_name
    }
    return highlighted_business
