#!/bin/bash

DS="../data/nikcub.v3.datastore"
DH="../data/nikcub.v3.datastore.history"
BS="../data/nikcub.v3.blobstore"
IP=$1
PORT="9090"
PP=`whereis python`
HTTP_CLIENT=`whereis lynx`
APPSERVER="/usr/local/bin/dev_appserver.py"
APPCFG="/usr/local/bin/appcfg.py"

$PP $APPCFG download_data --application=nikcub --url=http://nikcub.appspot.com/_ah/remote_api --filename=../data/log.new

$PP $APPCFG upload_data --filename=../data/log.new --url=http://localhost:8090/remote_api --auth_domain=localhost:8080 --application=dev~nikcub .

# dev_appserver.py -p 9090 --use_sqlite --datastore_path=/Users/nik/Projects/nikcub-old/data/nikcub.datastore --history_path=/Users/nik/Projects/nikcub-old/data/nikcub.datastore.history --blobstore_path=/Users/nik/Projects/nikcub-old/data/blobstore  --disable_static_caching --skip_sdk_update_check .

