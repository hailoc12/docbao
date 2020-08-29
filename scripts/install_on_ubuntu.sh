echo "INSTALL DOCBAO ON UBUNTU"
export install_dir="~/docbao2.0"
sleep 1
echo "Step 0: ensure python3, pip3 and curl are installed"
sleep 1
sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo apt install curl
sleep 1
echo "Step 1: install python libraries"
sleep 1
pip3 install -r requirements.txt
sleep 1
echo "Step 2: install firefox and xvfb"
sleep 1
sudo apt install firefox
sudo apt install xvfb
sleep 1
echo "Step 3: copy resources files"
sleep 1
sudo cp $install_dir/resources/firefox_driver/ubuntu/geckodriver /usr/bin
sudo cp $install_dir/resources/firefox_extension/adblock.xpi $install_dir/backend/input
sleep 1
echo "Step 5: install elasticsearch and kibana"
sudo apt install default-jre
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list
sudo apt-get update && sudo apt-get install elasticsearch
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service

sudo apt install kibana
sudo systemctl daemon-reload
sudo systemctl enable kibana.service
sudo systemctl start kibana.service

echo "Step 5: install rclone"
sleep 1
curl https://rclone.org/install.sh | sudo bash
sleep 1
echo "Step 6: config remoate ftp host in rclone as 'docbao'"
sleep 1
echo "REMEMBER: use remote hostname as 'docbao'"
sleep 1
echo "You can use demo host if you don't have one"
echo "name: docbao"
echo "host: ftp.tudonghoamaytinh.com"
echo "user: admin@demo.theodoibaochi.com"
echo "pass: docbaotheotukhoa"
sleep 1
rclone config
sleep 1
echo "Try to push frontend to remote host"
sleep 1
rclone sync -v $install_dir/frontend/ docbao:
sleep 1
echo "Try to list remote host"
sleep 1
rclone ls docbao:
sleep 1
echo "Step 7: run test"
sleep 1
cd $install_dir/backend
python3 test.py
sleep 1
echo "Finish !"
