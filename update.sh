#!/bin/bash
echo "Updating dependencies."

rm -rf venv/
python3 -m venv venv/

# Work in local environment
source venv/bin/activate

# Install dependencies

# rm -rf libs/pycord
# mkdir -p libs/pycord
# git clone https://github.com/Pycord-Development/pycord libs/pycord
# cd libs/pycord
# python3 -m pip install --upgrade --force-reinstall .[speed]
# cd ../..

rm -rf libs/servman
mkdir -p libs/servman
git clone /home/daniel/Code/Libs/ServiceManger libs/servman
cd libs/servman
python3 -m pip install --upgrade --force-reinstall .

python3 -m pip install --upgrade --force-reinstall orjson
python3 -m pip install --upgrade --force-reinstall path
python3 -m pip install --upgrade --force-reinstall dataset
python3 -m pip install --upgrade --force-reinstall websockets
python3 -m pip install -U --index-url https://test.pypi.org/simple/ servman-DGGFi


# done
deactivate
echo "Finished updating dependencies."