#!/bin/sh

THISDIR=$(echo `pwd`)

DCDIR=$(which docker-compose)

crontab -l | \
{ cat;
echo \
"0 6 * * * $DCDIR -f $THISDIR/docker-compose.yml up -d"; } \
| crontab -
