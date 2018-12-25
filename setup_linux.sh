echo "INSTALL DOCBAO"
echo "Step 1: install python libraries"
pip3 install -r requirements.txt
echo "Step 2: install firefox"
sudo apt install firefox
echo "Step 3: install rclone"
curl https://rclone.org/install.sh | sudo bash
echo "Step 4: config ftp host in rclone as 'docbao'"
echo "REMEMBER: use host name as 'docbao'"
rclone config
echo "Step 5: run test"
python3 ./backend/test.py
echo "Finish !"
