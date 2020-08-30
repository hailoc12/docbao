################################################################################
# File: install.sh
# Function: install docbao crawler in Ubuntu/Rasp OS
# Created date: 30/08/2020
#################################################################################

echo "INSTALL DOCBAO ON UBUNTU/RASPBERRY PI"
echo "__________________________________________________________________________"
export install_dir=$DOCBAO_BASE_DIR
cd $install_dir
sleep 1
echo "Step 1: Ensure python3, pip3 and curl are installed"
echo "__________________________________________________________________________"
sleep 1
sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo apt install curl
sleep 1
echo "Step 2: activate docbao virtual environment & install libraries"
echo "__________________________________________________________________________"
sleep 1
cd $install_dir
python3 -m venv docbao_env
source $install_dir/docbao_env/bin/activate
pip3 install -r requirements.txt
sleep 1
echo "Step 3: install firefox and xvfb"
echo "__________________________________________________________________________"
sleep 1
sudo apt install firefox
sudo apt install xvfb
sleep 1
echo "Step 4: copy resources files"
echo "__________________________________________________________________________"
sleep 1
sudo cp $install_dir/resources/firefox_driver/ubuntu/geckodriver /usr/bin
cp $install_dir/resources/firefox_extension/adblock.xpi $install_dir/src/backend/input
cp $install_dir/resources/configs/templates/default/config.yaml $install_dir/src/backend/input
sleep 1
echo "Step 5: run test"
echo "__________________________________________________________________________"
sleep 1
cd $install_dir/src/backend
python3 test.py
sleep 1
echo "Finish !"
