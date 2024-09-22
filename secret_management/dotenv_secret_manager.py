# secret_management/.env_secret_manager.py
import os
from dotenv import load_dotenv
from .secret_manager import SecretManager

class DotenvSecretManager(SecretManager):
    """
    A secret manager that reads secrets from a .env file. The .env file should be in the root of the project. But you can specify the path to the .env file.
    
    Args:
        env_file (str): The path to the .env file. Default is '.env'

    Example:
    ```python
    from secret_management import DotenvSecretManager
    
    """
    def __init__(self, env_file: str = '.env'):
        load_dotenv(env_file)

    def get_secret(self, secret_name: str) -> str:
        return os.getenv(secret_name)

