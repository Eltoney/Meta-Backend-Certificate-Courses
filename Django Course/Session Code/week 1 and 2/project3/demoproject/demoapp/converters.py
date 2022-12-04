class FourDigitYearConvertor:
    regex = '[1-2][0-9]{3}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return f'{value}'
