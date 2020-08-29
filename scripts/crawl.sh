#!/bin/bash
export local_dir=$DOCBAO_BASE_DIR

echo "Start running docbao_crawler"
cd $local_dir
# activate virtual environment
source docbao_env/bin/activate

# start crawl
cd $local_dir/src/backend
python3 crawl.py

# copy json data to frontend
cp -r $local_dir/src/backend/export/* $local_dir/src/frontend/export/
# release temp & lock
rm $local_dir/backend/docbao.lock
killall -9 firefox
killall geckodriver
echo "stop docbao"

