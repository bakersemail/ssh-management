#!/bin/bash

echo "`date '+%Y-%m-%d %H:%M:%S'` - manage.py $1 $2 $3 $4 $5" >> manage.log
python manage.py $1 $2 $3 $4 $5
