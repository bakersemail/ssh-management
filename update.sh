#!/bin/bash

echo "`date '+%Y-%m-%d %H:%M:%S'` - update.sh" >> manage.log
cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.bak.`date +%Y%m%d`
if [ $? -ne 0 ]; then
  echo "Could not backup authorized_keys"
  exit 1
fi

cp newauth ~/.ssh/authorized_keys
if [ $? -ne 0 ]; then
  echo "Could not update authorized_keys"
  exit 1
fi
