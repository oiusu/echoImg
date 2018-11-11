#!/usr/bin/env bash

FWDIR="$(cd "`dirname "$0"`"; pwd)"
echo $FWDIR
cd $FWDIR



export PYTHONPATH=$PYTHONPATH:`pwd`
nohup python app/echoImg_run.py  &

