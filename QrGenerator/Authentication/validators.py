import re
from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    def validate(self, password, user=None):

        pattern = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d.]{8,}$'
        if not re.match(pattern, password):
            raise ValidationError(
                "La password deve essere lunga almeno 8 caratteri, contenere solo caratteri alfanumerici, può contenere \".\" e deve contenere una maiuscola e un numero.", code='password_no_match'
            )

    def get_help_text(self):
        return "La password deve essere lunga almeno 8 caratteri, contenere solo caratteri alfanumerici, può contenere \".\" e deve contenere una maiuscola e un numero."