from enum import Enum

class SecretManagerType(Enum):
    COLAB = "colab"
    DOTENV = "dotenv"
    GOOGLE_CLOUD = "google_cloud"
    AZURE = "azure"

