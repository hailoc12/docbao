#!/bin/bash
export baonoi_api="baonoi_api"
export local_dir="docbao_bangtin"
export remote_dir="docbao_vietnam"
export bangtin_api="bangtin_api"

echo $local_dir
echo $remote_dir
echo $bangtin_api

PATH=/home/pi/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
echo "start running docbao"
cd ~/$local_dir/backend/category
#rm *
cd ~/$local_dir/backend
# rclone sync -v $remote_dir:category ~/$local_dir/backend/category
# rclone copy -v $remote_dir:output ~/$local_dir/backend/input
python3 crawl.py
rclone copy ~/$local_dir/backend/data $bangtin_api:bangtin_api/backend/data
rclone copy ~/$local_dir/backend/data $baonoi_api:bangtin_api/backend/data
rclone delete $remote_dir:export/log_data.json
rclone delete $remote_dir:export/keyword_freq_log.json
rclone copy -v ~/$local_dir/backend/export $remote_dir:export
rm ~/$local_dir/backend/docbao.lock
killall -9 firefox
killall geckodriver
echo "stop docbao"

