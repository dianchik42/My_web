class FourDigitYearConverter:
    """Конвертер для года из 4 цифр"""
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value).zfill(4)


class TwoDigitMonthConverter:
    """Конвертер для месяца из 2 цифр (01-12)"""
    regex = '0[1-9]|1[0-2]'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value).zfill(2)


class PositiveIntConverter:
    """Конвертер для положительных целых чисел"""
    regex = '[1-9][0-9]*'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)