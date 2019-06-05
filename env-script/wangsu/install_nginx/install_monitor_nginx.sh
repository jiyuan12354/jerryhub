#!/bin/bash

BASE=/tmp/install_monitor_nginx
DOWNLOAD_PREFIX=http://nginx.org/download/
DOWNLOAD_FILENAME=nginx-1.16.0.tar.gz

set -e

rm -rf ${BASE}
mkdir ${BASE}

cd ${BASE}
wget ${DOWNLOAD_PREFIX}${DOWNLOAD_FILENAME}
tar xvf ${DOWNLOAD_FILENAME}

cd nginx-*
sh configure --with-stream
make
make install

cd /usr/local/nginx/conf
mv nginx.conf nginx.conf.bk
wget https://laynelin.gitee.io/pages/wangsu/install_monitor_nginx/nginx.conf
chmod 644 nginx.conf

cd /etc/init.d
rm -rf nginx
wget https://laynelin.gitee.io/pages/wangsu/install_monitor_nginx/nginx
chmod 755 nginx
chkconfig --add nginx
chkconfig nginx on
systemctl restart nginx
systemctl status nginx
