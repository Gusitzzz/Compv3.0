#!/bin/bash

echo "Available backups:"
ls -la backup/

read -p "Enter backup filename: " FILE
cp "backup/$FILE" ammonia_monitor.db
echo "Restored: $FILE"