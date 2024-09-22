# secret_management/__init__.py
from .secret_manager import SecretManager
from .secret_manager_type import SecretManagerType
from .dotenv_secret_manager import DotenvSecretManager
from .colab_secret_manager import ColabSecretManager

def secret_manager_factory(secret_manager_type: SecretManagerType) -> SecretManager:
    if secret_manager_type == SecretManagerType.COLAB:
        return ColabSecretManager()
    elif secret_manager_type == SecretManagerType.DOTENV:
        return DotenvSecretManager()
    # Add future conditions for Azure and Google Cloud
    raise ValueError(f"Unsupported Secret Manager Type: {secret_manager_type}")

