#!/bin/bash

PP=`whereis python`
HTTP_CLIENT=`whereis lynx`
APPSERVER="/usr/local/bin/dev_appserver.py"
APPCFG="/usr/local/bin/appcfg.py"

java -jar ~/Projects/javascript/jquery-mobile/build/yuicompressor-2.4.4.jar --type css -o ./static/css/nikcub.min.css ./static/css/nikcub.css 
cd ~/Projects/nikcub-static/
./update.sh
cd ~/Projects/nikcub-old/site
$PP $APPCFG -A nikcub -e nikcub@gmail.com --skip_sdk_update_check update ~/Projects/nikcub-old/site
