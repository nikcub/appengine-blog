#!/bin/bash

DS="../data/nikcub.datastore"
DH="../data/nikcub.datastore.history"
BS="../data/nikcub.blobstore"
IP=$1
PORT="8090"
PP=`whereis python`
HTTP_CLIENT=`whereis lynx`
APPSERVER="/usr/local/bin/dev_appserver.py"

if [ "$IP" = "" ]; then 
	IP=`ifconfig -a | grep -A 1 ppp0 | tail -n 1 | cut -d" " -f2`

	echo "Updating DNS.."
	lynx -dump -auth=nikcub:delije4u "http://members.dyndns.org/nic/update?hostname=nikcub.dyndns.org&myip=$IP&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG"
fi

if [ "$IP" = "console" ]; then
	$PP
fi

echo "AppEngine Helper Script" 
echo "Usage: start.sh [ip] (defaults to ppp0)" 
echo "Using IP : " $IP 
echo "Using Port : " $PORT
echo "Using DS : " $DS
echo "Using DH : " $DH

echo "Starting client.."
sudo $PP $APPSERVER -a $IP -p $PORT --use_sqlite --datastore_path=$DS --history_path=$DH --blobstore_path=$BS --disable_static_caching --skip_sdk_update_check .

