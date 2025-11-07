#!/bin/bash

# Ada Content Creator - Global Command Uninstaller

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                  ADA CONTENT CREATOR - UNINSTALLER                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

INSTALL_PATH="/usr/local/bin/acc"

# Check if acc command exists
if [ ! -L "$INSTALL_PATH" ] && [ ! -f "$INSTALL_PATH" ]; then
    echo "ℹ️  'acc' command is not installed."
    exit 0
fi

echo "⚠️  This will remove the global 'acc' command."
read -p "   Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Uninstallation cancelled."
    exit 0
fi

echo "🗑️  Removing 'acc' command..."
sudo rm "$INSTALL_PATH"

if [ ! -e "$INSTALL_PATH" ]; then
    echo ""
    echo "✅ 'acc' command has been removed successfully."
    echo ""
    echo "To reinstall, run:"
    echo "  ./install_command.sh"
    echo ""
else
    echo ""
    echo "❌ Uninstallation failed. Please check permissions."
    exit 1
fi
