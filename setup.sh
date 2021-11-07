echo "Setting up the bot..."

# Purge
rm -rf bot-env
rm -rf conf

# Renew
python3 -m venv bot-env

# Work in local environment
source bot-env/bin/activate

# Install dependencies
python3 -m pip install -U discord.py
python3 -m pip install -U path
python3 -m pip install -U dataset
python3 -m pip install -U websockets
python3 -m pip install -U --index-url https://test.pypi.org/simple/ servman-DGGFi

# Configuration
mkdir conf

# Defer finishing touches
python3 setup.py

# Done
deactivate

echo "Setup complete."