#!/bin/bash -l
set -a
source SETTINGS.env
set +a
export local_dir=$DOCBAO_BASE_DIR
export PYTHONPATH=$PYTHONPATH:$local_dir
source $local_dir/docbao_env/bin/activate

cd $local_dir

# start crawl
cd $local_dir/src/backend
$local_dir/docbao_env/bin/python3 push_all_data_to_rabbitmq.py

echo "Finish"

