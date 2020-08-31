#!/bin/bash -l
set -a 
source SETTINGS.env
set +a
export localdir=$DOCBAO_BASE_DIR
cd $localdir/src/backend/data
rm *
