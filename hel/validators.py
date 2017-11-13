from django.core.validators import RegexValidator

NameValidator = RegexValidator(regex=r'^([А-ЯЁ][а-яё]*)(-[А-ЯЁ]?[а-яё]*)?$')
PhoneValidator = RegexValidator(regex=r'^\d{11}$')
PasswordValidator = RegexValidator(regex=r'^[A-Za-z0-9_]{8,30}$')
HashedPasswordValidator = RegexValidator(regex=r'^[a-z0-9]{128}$')

