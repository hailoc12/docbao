# load environments and base dir 
source SETTINGS.env
export local_dir=$DOCBAO_BASE_DIR
export PYTHONPATH=$PYTHONPATH:$local_dir

cd $local_dir
$local_dir/docbao_env/bin/python3 tools/config_manager.py

