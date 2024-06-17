from datetime import date

from django.core.exceptions import ValidationError


def validate_not_future_date(value: date) -> None:
    if value > date.today():
        raise ValidationError('Дата не может быть в будущем.')
