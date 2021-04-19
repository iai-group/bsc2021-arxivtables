#/bin/sh

THISDIR=$(echo `pwd`)

crontab -l | \
{ cat; \
echo "0 6 * * * docker-compose -f $THISDIR/docker-compose.yml up -d --build"; } \
| crontab -

