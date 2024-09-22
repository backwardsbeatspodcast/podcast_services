from abc import ABC, abstractmethod

class SecretManager(ABC):
    """
    Abstract class for secret management. Secret_names are defined by SecretManagerTypes in secret_manager_types.py
    """
    
    @abstractmethod
    def get_secret(self, secret_name: str):
        pass

