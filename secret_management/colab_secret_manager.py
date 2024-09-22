from secret_management.secret_manager import SecretManager
import sys

class ColabSecretManager(SecretManager):
    """
    A secret manager that uses Google Colab's userdata to store secrets.
    """

    RED = "\033[91m"
    RESET = "\033[0m"

    class ColabError(Exception):
        pass

    def __init__(self):
        if 'google.colab' not in sys.modules:
            print(f"{self.RED}Warning: This module is intended to be used in Google Colab.{self.RESET}")

    def get_secret(self, secret_name: str):
        if 'google.colab' not in sys.modules:
            raise self.ColabError("Attempting to access Colab secrets outside of Google Colab.")
        from google.colab import userdata
        return userdata.get(secret_name)

