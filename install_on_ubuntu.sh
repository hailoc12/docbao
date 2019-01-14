echo "INSTALL DOCBAO ON UBUNTU"
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
sudo cp ./resources/firefox_driver/ubuntu/geckodriver /usr/bin/
sudo cp ./resources/firefox_driver/ubuntu/crawl.py ./backend/lib/
sudo cp ./resources/configs/templates/default/config.txt ./backend/input/
sleep 1
echo "Step 4: install rclone"
sleep 1
curl https://rclone.org/install.sh | sudo bash
sleep 1
echo "Step 5: config remoate ftp host in rclone as 'docbao'"
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
rclone sync -v ~/docbao/frontend/ docbao:
sleep 1
echo "Try to list remote host"
sleep 1
rclone ls docbao:
sleep 1
echo "Step 6: run test"
sleep 1
python3 ~/docbao/backend/test.py
sleep 1
echo "Finish !"
