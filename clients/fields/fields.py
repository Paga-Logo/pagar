import warnings
from typing import Union

from django.db.models import CharField, TextField

from clients.utils.crypt import encrypt, decrypt


class EncryptionWarning(RuntimeWarning):
    pass


class EncryptedCharField(CharField):
    """
    Extends CharField to handle the data for encryption and decryption
    """

    def __init__(self, max_length: int = 255, *args, **kwargs) -> None:
        super(EncryptedCharField, self).__init__(
            *args, **kwargs, max_length=max_length)

    def get_db_prep_value(self, value, connection, prepared=False) -> Union[str, None]:
        value = self.to_python(value)
        if value is not None:
            if self.max_length and len(value) > self.max_length:
                warnings.warn(
                    f"Truncating field {self.name} from {len(value)} to {self.max_length}",
                    EncryptionWarning)
                value = value[:self.max_length]
            value = encrypt(value)
            return value
        return value

    def to_python(self, value: str) -> str:
        try:
            if isinstance(value, str):
                return decrypt(value)
            return value
        except Exception:
            return value


class EncryptedTextField(TextField):
    """
    Extends TextField to handle the data for encryption and decryption
    """

    def __init__(self, *args, **kwargs):
        super(EncryptedTextField, self).__init__(*args, **kwargs)

    def get_db_prep_value(self, value, connection, prepared=False) -> Union[str, None]:
        """
        Prepare the value to encrypted for use in the query object
        :param value: String
        :return: String
        """
        value = self.to_python(value)
        if value is not None:
            value = encrypt(value)
            return value
        return value

    def to_python(self, value: str) -> str:
        """
        Transform the value for use in python
        :param value: String
        :return: String
        """
        try:
            if isinstance(value, str):
                return decrypt(value)
            return value
        except Exception as e:
            return value
