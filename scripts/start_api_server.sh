#!/bin/bash -l
export localdir="bangtin_api"
export port=8080
cd ~/$localdir/backend
python3 docbao_api.py
cd ~/$localdir/
cd ~
#./ngrok http 0.0.0.0:$port -region ap -subdomain=theodoibaochi 

