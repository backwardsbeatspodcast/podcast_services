import requests
from secret_management.secret_manager_type import SecretManagerType
from secret_management.secret_manager_factory import secret_manager_factory

class BaseAPI:
    """
    Base class for APIs that require authentication via a client ID and secret.
    This class handles the retrieval of an access token using the client client_credentials grant type.
    """

    def __init__(self, secret_manager_type: SecretManagerType, token_url: str,
                 client_id_key: str, client_secret_key: str):
        self.secret_manager = secret_manager_factory(secret_manager_type)
        self.token_url = token_url
        self.client_id = self.secret_manager.get_secret(client_id_key)
        self.client_secret = self.secret_manager.get_secret(client_secret_key)
        self.access_token = None

    def get_access_token(self):
        if self.access_token:
            return self.access_token

        try:
            response = requests.post(
                self.token_url,
                data={'grant_type': 'client_credentials'},
                auth=(self.client_id, self.client_secret)
            )
            response.raise_for_status()
            self.access_token = response.json().get('access_token')
            return self.access_token
        except requests.RequestException as e:
            print(f"[BaseAPI] Error retrieving access token: {e}")
            return None

