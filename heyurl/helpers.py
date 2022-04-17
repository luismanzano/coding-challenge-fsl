from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def validate_url(url_string: str) -> bool:
    valid_url = URLValidator()

    try:
        valid_url(url_string)
    except ValidationError as e:
        return False

    return True