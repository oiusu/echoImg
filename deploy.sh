#!/usr/bin/env bash


FWDIR="$(cd "`dirname "$0"`"; pwd)"
echo $FWDIR
cd $FWDIR


# prod conf
deploy_host=$1
work_path=/home/chenc/apps/echoImg_new
user_name=chenc
port=22


rm -rf echoImg.zip

echo "finish rm echoImg.zip..."

zip -r echoImg.zip app service.sh

echo "finish zip... "


ssh -p ${port} ${user_name}@${deploy_host} "mkdir -p ${work_path};rm -rf ${work_path}/*; "

scp   echoImg.zip  ${user_name}@${deploy_host}:${work_path}
echo "finish scp ..."
ssh -p ${port} ${user_name}@${deploy_host} "cd ${work_path}; unzip echoImg.zip ; "

echo "finish ..."
