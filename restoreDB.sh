#!/bin/bash
# Restore the database from backup.sql
docker cp backup.sql database:/backup.sql
docker exec -i database psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} < /backup.sql
echo "Database restored successfully."
