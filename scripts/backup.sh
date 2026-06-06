#!/bin/bash

DATE=$(date +%Y%m%d_%H%M%S)
cp ammonia_monitor.db "backup/ammonia_$DATE.db"
echo "Backup saved: ammonia_$DATE.db"