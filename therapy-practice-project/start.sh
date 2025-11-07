#!/bin/bash

# Quick launcher for Hendersonville Counseling Content Creator
# Usage: ./start.sh

cd "$(dirname "$0")"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  Warning: ANTHROPIC_API_KEY not set"
    echo "   The system will guide you through setup if needed"
    echo ""
fi

# Launch the CLI
python3 content_cli.py
