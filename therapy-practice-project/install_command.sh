#!/bin/bash

# Ada Content Creator - Global Command Installer
# This script creates a global 'acc' command that works from anywhere

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    ADA CONTENT CREATOR - INSTALLER                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACC_SCRIPT="$SCRIPT_DIR/acc"
INSTALL_DIR="/usr/local/bin"
INSTALL_PATH="$INSTALL_DIR/acc"

# Check if acc script exists
if [ ! -f "$ACC_SCRIPT" ]; then
    echo "❌ Error: acc script not found at $ACC_SCRIPT"
    exit 1
fi

# Check if /usr/local/bin exists
if [ ! -d "$INSTALL_DIR" ]; then
    echo "📁 Creating $INSTALL_DIR directory..."
    sudo mkdir -p "$INSTALL_DIR"
fi

# Check if acc command already exists
if [ -L "$INSTALL_PATH" ]; then
    echo "⚠️  'acc' command already exists."
    read -p "   Overwrite? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Installation cancelled."
        exit 0
    fi
    echo "🔄 Removing old symlink..."
    sudo rm "$INSTALL_PATH"
fi

# Create symlink
echo "🔗 Creating symlink..."
sudo ln -s "$ACC_SCRIPT" "$INSTALL_PATH"

# Verify installation
if [ -L "$INSTALL_PATH" ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════════════════════╗"
    echo "║                          ✅ INSTALLATION COMPLETE!                         ║"
    echo "╚════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🎉 The 'acc' command is now available globally!"
    echo ""
    echo "Usage:"
    echo "  Just type:  acc"
    echo "  From anywhere in your terminal!"
    echo ""
    echo "Example:"
    echo "  $ cd ~"
    echo "  $ acc"
    echo "  → Ada Content Creator launches! 🚀"
    echo ""
    echo "To uninstall, run:"
    echo "  sudo rm /usr/local/bin/acc"
    echo ""
else
    echo ""
    echo "❌ Installation failed. Please check permissions."
    exit 1
fi
