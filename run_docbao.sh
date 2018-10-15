#!/bin/bash
PATH=/home/pi/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
echo "start running docbao_congnghe"
cd ~/docbao_congnghe/backend/category
rm *
cd ~/docbao_congnghe/backend
rclone sync -v docbao_congnghe:category ~/docbao_congnghe/backend/category
rclone copy -v docbao_congnghe:output ~/docbao_congnghe/backend/input
python3 ~/docbao_congnghe/backend/docbao.py
python3 ~/docbao_congnghe/backend/event_detect.py 
rclone delete docbao_congnghe:export/log_data.json
rclone copy -v ~/docbao_congnghe/backend/export docbao_congnghe:export	
echo "stop docbao_congnghe"

