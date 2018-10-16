#!/bin/bash
PATH=/home/pi/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
echo "start running docbao_vietanh"
cd ~/docbao_vietanh/backend/category
rm *
cd ~/docbao_vietanh/backend
rclone sync -v docbao_vietanh:category ~/docbao_vietanh/backend/category
rclone copy -v docbao_vietanh:output ~/docbao_vietanh/backend/input
python3 ~/docbao_vietanh/backend/docbao.py
python3 ~/docbao_vietanh/backend/event_detect.py 
rclone delete docbao_vietanh:export/log_data.json
rclone copy -v ~/docbao_vietanh/backend/export docbao_vietanh:export	
echo "stop docbao_vietanh"

