#/bin/sh

crontab -l | \
{ cat; \
echo "0 6 * * * docker-compose -f $THISDIR/docker-compose.yml up -d --build" } \
| crontab -

