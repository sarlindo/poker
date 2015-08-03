#!/bin/bash

cd /root/projects/dyjango/poker
heroku pgbackups:capture --expire
heroku pgbackups:capture

curl -o latest.dump `heroku pgbackups:url`

mv latest.dump /root/projects/dyjango/poker/db

pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d sptpoker /root/projects/dyjango/poker/db/latest.dump
