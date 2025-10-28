#!/usr/bin/env python3
"""
API Key Setup Utility

Interactive script to help set up your Anthropic API key.
"""

from pathlib import Path
import sys


def setup_api_key():
    """Guide user through API key setup."""

    print("\n" + "=" * 70)
    print("ANTHROPIC API KEY SETUP")
    print("=" * 70 + "\n")

    env_file = Path(__file__).parent / ".env"
    env_example = Path(__file__).parent / ".env.example"

    # Check if .env already exists
    if env_file.exists():
        print("✓ .env file already exists")
        print(f"  Location: {env_file}")
        print("\nTo update your API key, edit the .env file directly.")

        # Test if it's working
        try:
            from config import check_api_key_configured, get_api_key
            if check_api_key_configured():
                api_key = get_api_key()
                masked = f"{api_key[:8]}...{api_key[-8:]}"
                print(f"\n✓ Current API key: {masked}")
                print("\n✅ Configuration is working!")
            else:
                print("\n⚠️  API key in .env file but not loading correctly")
                print("   Make sure the format is: ANTHROPIC_API_KEY=your-key")
        except Exception as e:
            print(f"\n⚠️  Error checking configuration: {e}")

    else:
        print("Setting up .env file for the first time...\n")

        # Get API key from user
        print("Please enter your Anthropic API key")
        print("(You can find this at: https://console.anthropic.com/settings/keys)")
        print()

        api_key = input("API Key: ").strip()

        if not api_key:
            print("\n❌ No API key provided. Setup cancelled.")
            return False

        # Validate format (basic check)
        if not api_key.startswith("sk-ant-"):
            print("\n⚠️  Warning: API key doesn't start with 'sk-ant-'")
            print("   This might not be a valid Anthropic API key.")
            confirm = input("   Continue anyway? (y/N): ").strip().lower()
            if confirm != 'y':
                print("\n❌ Setup cancelled.")
                return False

        # Write .env file
        with open(env_file, 'w') as f:
            f.write("# Anthropic API Configuration\n")
            f.write(f"ANTHROPIC_API_KEY={api_key}\n")

        print(f"\n✓ API key saved to {env_file}")
        print("\n✅ Setup complete!")

        # Test configuration
        print("\nTesting configuration...")
        try:
            from config import check_api_key_configured, get_api_key
            if check_api_key_configured():
                test_key = get_api_key()
                masked = f"{test_key[:8]}...{test_key[-8:]}"
                print(f"✓ API key loaded successfully: {masked}")
            else:
                print("⚠️  Could not load API key")
        except Exception as e:
            print(f"⚠️  Error testing configuration: {e}")

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("\n1. Test content creation:")
    print("   python request_social_post.py \\")
    print("     --topic 'Test post' \\")
    print("     --platform Instagram \\")
    print("     --use-api")
    print("\n2. View configuration:")
    print("   python config.py")
    print("\n3. View documentation:")
    print("   cat CONTENT_MANAGEMENT_SYSTEM.md")
    print()

    return True


def main():
    """Main function."""
    try:
        success = setup_api_key()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
