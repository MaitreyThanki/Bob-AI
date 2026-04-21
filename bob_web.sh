#!/bin/bash
# Navigate to the project directory
cd "$(dirname "$0")"

echo "🚀 Starting BOB OpenAI Bridge on http://localhost:8080"
echo "Press CTRL+C to stop the server."
echo ""

# Run the API using the virtual environment
/home/maitrey/.config/bobai/bobenv/bin/python3 /home/maitrey/.config/bobai/bob_api.py
