import datetime


class StrictDate(datetime.date):
    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield cls.validate

    @classmethod
    def validate(cls, value: datetime.date, **kwargs) -> datetime.date:
        if not isinstance(value, datetime.date):
            raise ValueError("Value must be a datetime.date object")
        return value
