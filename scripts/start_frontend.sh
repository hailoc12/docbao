#!/bin/bash -l
set -a 
source SETTINGS.env
set +a
export localdir=$DOCBAO_BASE_DIR
cd $localdir/src/frontend
php -S $DOCBAO_FRONTEND_HOST:$DOCBAO_FRONTEND_PORT

