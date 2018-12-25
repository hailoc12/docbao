#!/bin/bash
PATH=/home/pi/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
echo "start running docbao"
cd ~/docbao/backend/category
#rm *
cd ~/docbao/backend
rclone sync -v docbao:category ~/docbao/backend/category
rclone copy -v docbao:output ~/docbao/backend/input
python3 ~/docbao/backend/docbao.py
python3 ~/docbao/backend/event_detect.py 
rclone delete docbao:export/log_data.json
rclone copy -v ~/docbao/backend/export docbao:export	
echo "stop docbao"

