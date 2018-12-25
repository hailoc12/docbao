echo "INSTALL DOCBAO"
echo "Step 1: install python libraries"
pip3 install -r requirements.txt
echo "Step 2: install firefox"
sudo apt install firefox
if [$? -eq 0 ]; then
	echo OK
else
	sudo apt install firefox-esr
fi
echo "Step 3: install rclone"
curl https://rclone.org/install.sh | sudo bash
echo "Step 4: config remoate ftp host in rclone as 'docbao'"
echo "REMEMBER: use remote hostname as 'docbao'"
rclone config
echo "Try to push frontend to remote host"
rclone copy -v ./frontend/* docbao:
echo "Step 5: run test"
python3 ./backend/test.py
echo "Finish !"
