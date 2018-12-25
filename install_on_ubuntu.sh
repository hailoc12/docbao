echo "INSTALL DOCBAO ON UBUNTU"
echo "Step 0: ensure python3 and pip3 are installed"
sudo apt update
sudo apt install python3
sudo apt install python3-pip
echo "Step 1: install python libraries"
pip3 install -r requirements.txt
echo "Step 2: install firefox and xvfb"
sudo apt install firefox
sudo apt install xvfb
echo "Step 3: copy geckodriver to /usr/bin and crawl.py to ./backend/lib"
sudo cp ./resources/firefox_driver/ubuntu/geckodriver /usr/bin/
sudo cp ./resources/firefox_driver/ubuntu/crawl.py ./backend/lib/
echo "Step 4: install rclone"
curl https://rclone.org/install.sh | sudo bash
echo "Step 5: config remoate ftp host in rclone as 'docbao'"
echo "REMEMBER: use remote hostname as 'docbao'"
rclone config
echo "Try to push frontend to remote host"
rclone sync -v ~/docbao/frontend/ docbao:
echo "Try to list remote host"
rclone ls docbao:
echo "Step 6: run test"
python3 ~/docbao/backend/test.py
echo "Finish !"
