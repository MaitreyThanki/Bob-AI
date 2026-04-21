#!/bin/bash
# Open WebUI Installation Script for BOB

set -e

INSTALL_DIR="$HOME/open-webui"
echo "📂 Creating installation directory at $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo "🐍 Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing Open WebUI (this may take a few minutes)..."
pip install --upgrade pip
pip install open-webui

echo ""
echo "✅ Installation Complete!"
echo "--------------------------------------------------"
echo "To start Open WebUI, run these commands:"
echo "  cd $INSTALL_DIR"
echo "  source venv/bin/activate"
echo "  open-webui serve"
echo "--------------------------------------------------"
echo "Then open http://localhost:8080 in your browser."
echo "(Note: If BOB is on 8080, Open WebUI will automatically try 8081 or 3000)"
