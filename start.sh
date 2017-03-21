#!/bin/bash

cd /opt/ood

service elasticsearch restart

sleep 20

supervisord -n -c conf/supervisor.conf
