#!/bin/bash

backup_name=b006
cd /root/projects/dyjango/poker

#heroku pg:backups capture

curl -o latest.dump `heroku pg:backups public-url $backup_name | tr -d '\r\n' | sed -e "s/.*'\(.*\).*'/\1/"`

mv latest.dump /root/projects/dyjango/poker/db

pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d sptpoker /root/projects/dyjango/poker/db/latest.dump
