# Podcast Services

Provides a unified interface for interacting with podcast hosting APIs.  
This subpackage currently supports the **Podbean API** and is designed to simplify authentication, podcast info retrieval, and episode management.

## Interface Overview

Currently, the package supports **Podbean**. Examples below assume use of the Podbean API.

### PodbeanAPI

The `PodbeanAPI` class provides methods for interacting with the [Podbean REST API](https://developers.podbean.com/). All methods return data in JSON format.

#### Methods

- `get_podcast()`: Fetches metadata about your podcast, including title, author, and description.
- `get_episodes(offset=0, limit=10)`: Retrieves a paginated list of episodes for your podcast.
- `get_episode(episode_id)`: Fetches metadata for a specific episode using its ID.
## Usage Examples

Below are some examples of how to use the `PodbeanAPI` class.

### Initialize the PodbeanAPI class

```python
from podcast_services import PodbeanAPI
from secret_management.secret_manager_type import SecretManagerType

# Initialize PodbeanAPI with default secret manager (DOTENV)
podbean_api = PodbeanAPI(secret_manager_type=SecretManagerType.DOTENV)

