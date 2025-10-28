#!/usr/bin/env python3
"""
Configuration Management

Loads API keys and configuration from .env file or environment variables.
"""

import os
from pathlib import Path
from typing import Optional


def load_env_file(env_path: Path = None) -> dict:
    """
    Load environment variables from .env file.

    Args:
        env_path: Path to .env file (defaults to .env in script directory)

    Returns:
        Dictionary of environment variables
    """
    if env_path is None:
        env_path = Path(__file__).parent / ".env"

    env_vars = {}

    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Parse KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()

    return env_vars


def get_api_key() -> Optional[str]:
    """
    Get Anthropic API key from environment or .env file.

    Returns:
        API key string or None if not found
    """
    # First check environment variable (takes precedence)
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if api_key:
        return api_key

    # Then check .env file
    env_vars = load_env_file()
    api_key = env_vars.get("ANTHROPIC_API_KEY")

    if api_key:
        # Set it in environment for other scripts
        os.environ["ANTHROPIC_API_KEY"] = api_key
        return api_key

    return None


def ensure_api_key() -> str:
    """
    Ensure API key is available, raise error if not.

    Returns:
        API key string

    Raises:
        ValueError: If API key is not configured
    """
    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "Anthropic API key not found. Please either:\n"
            "1. Set ANTHROPIC_API_KEY environment variable:\n"
            "   export ANTHROPIC_API_KEY='your-key'\n"
            "2. Create a .env file with:\n"
            "   ANTHROPIC_API_KEY=your-key\n"
            "\nSee .env.example for template."
        )

    return api_key


def check_api_key_configured() -> bool:
    """
    Check if API key is configured.

    Returns:
        True if API key is available, False otherwise
    """
    return get_api_key() is not None


# Auto-load .env file when module is imported
_env_vars = load_env_file()
for key, value in _env_vars.items():
    if key not in os.environ:  # Don't override existing env vars
        os.environ[key] = value


if __name__ == "__main__":
    # Test configuration
    print("Configuration Test")
    print("=" * 60)

    if check_api_key_configured():
        api_key = get_api_key()
        # Show only first/last 8 characters for security
        masked_key = f"{api_key[:8]}...{api_key[-8:]}"
        print(f"✓ API Key configured: {masked_key}")
        print("\nYou're ready to use the content creation tools!")
    else:
        print("✗ API Key not configured")
        print("\nPlease configure your API key:")
        print("1. Copy .env.example to .env")
        print("2. Add your Anthropic API key to .env")
        print("\nOr set environment variable:")
        print("  export ANTHROPIC_API_KEY='your-key'")
