import requests
from shared_services import BaseAPI
from secret_management.secret_manager_type import SecretManagerType


class PodbeanAPI(BaseAPI):
    BASE_URL='https://api.podbean.com/v1'  # Base URL for Podbean API

    def __init__(self, secret_manager_type=SecretManagerType.DOTENV):
        super().__init__(
            secret_manager_type,
            token_url=f'{self.BASE_URL}/oauth/token',
            client_id_key='PODBEAN_CLIENT_ID',
            client_secret_key='PODBEAN_CLIENT_SECRET'
        )


    def _make_get_request(self, endpoint: str, params: dict = None):
        access_token = self.get_access_token()
        if not access_token:
            print("[PodbeanAPI] No access token available.")
            return None
    
        headers = {'Authorization': f'Bearer {access_token}'}
        url = f'{self.BASE_URL}/{endpoint}'
    
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[PodbeanAPI] Error calling '{endpoint}': {e}")
            return None

    def _make_post_request(self, endpoint: str, data: dict = None):
        access_token = self.get_access_token()
        if not access_token:
            print("[PodbeanAPI] No access token available.")
            return None
    
        headers = {'Authorization': f'Bearer {access_token}'}
        url = f'{self.BASE_URL}/{endpoint}'
    
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[PodbeanAPI] Error calling '{endpoint}': {e}")
            return None

            
    def get_podcast(self):
        """
        Retrieves the podcast information using the Podbean API.
        """
        return self._make_get_request('podcast')

    def get_episodes(self, offset: int = 0, limit: int = 10):
        """
        Retrieves the episodes of the podcast using the Podbean API.
        """
        return self._make_get_request('episodes', params={'offset': offset, 'limit': limit})

    def get_episode(self, episode_id: str):
        """
        Retrieves a specific episode using the Podbean API.
        """
        return self._make_get_request(f'episodes/{episode_id}')

