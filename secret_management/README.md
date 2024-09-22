# Secret Management

This module provides a simple and modular approach to secret management for your applications. Currently, it supports Google Colab secrets, with future updates planned for Google Cloud Secrets, Azure Key Vault, and .env file support.

## Features

- **Current Support**: 
  - Google Colab Secrets
  - .env file support

- **Upcoming Features**:
  - Google Cloud Secrets
  - Azure Key Vault

## Usage

To use the current secret manager (Google Colab Secrets), you can create an instance of the secret manager like this:

```python
from secret_management import SecretManager, secret_manager_factory
from secret_management.enum import SecretManagerType

# Create a secret manager for Google Colab
secret_manager: SecretManager = secret_manager_factory(SecretManagerType.COLAB)

# Retrieve a secret
secret_value: str = secret_manager.get_secret("your_secret_name")
print(secret_value)

