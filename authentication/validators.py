import re
from django.core.exceptions import ValidationError


class CustomPasswordValidator:
    def validate(self, password, user=None):

        pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[=@$!%*?&])(.{8,})$'
        if not re.match(pattern, password):
            raise ValidationError(
                "La password deve essere lunga almeno 8 caratteri, deve contenere una maiuscola, un numero e almeno un carattere speciale (=@$!%*?&).", code='password_no_match'
            )

    def get_help_text(self):
        return "La password deve essere lunga almeno 8 caratteri, deve contenere una maiuscola, un numero e almeno un carattere speciale (@$!%*?&)."