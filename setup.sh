echo "Setting up the bot..."

# Purge
rm -rf venv/
rm -rf conf/
rm -rf libs/pycord
rm -rf logs/

# Renew
python3 -m venv venv

# Work in local environment
source venv/bin/activate

# Install dependencies
mkdir -p libs/pycord
git clone https://github.com/Pycord-Development/pycord libs/pycord
cd libs/pycord

python3 -m pip install -U .[speed]
python3 -m pip install -U orjson
python3 -m pip install -U path
python3 -m pip install -U dataset
python3 -m pip install -U websockets
python3 -m pip install -U --index-url https://test.pypi.org/simple/ servman-DGGFi

cd ../..

# Configuration
mkdir conf
mkdir logs

# Defer finishing touches
python3 setup.py

# Done
deactivate

echo "Setup complete."