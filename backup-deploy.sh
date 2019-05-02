# -----------------------------------------------------------------------------
# PK-DB backup
# -----------------------------------------------------------------------------
# TODO: compress backup
# TODO: run via cron job
# TODO: differential backup
# TODO: check that backup can be restored
#
# usage:
#	./backup-deploy.sh
# -----------------------------------------------------------------------------

echo "-------------------------------"
echo "Backup PKDB docker volumes"
echo "-------------------------------"
cd /var/git/pkdb

# create directory for backup
BACKUP_DIR=/var/backups/pkdb/$(date '+%F')
sudo mkdir -p $DIR
sudo chown -R mkoenig:mkoenig $DIR
echo "Backup to" $BACKUP_DIR


echo *** backup django volumes***
# django_media
docker run -it --rm -v pkdb_django_media:/volume -v /tmp:/backup pkdb_backup \
    tar -cvzf $BACKUP_DIR/django_media.tar.gz -C /volume ./

# django_static
# FIXME:
# elasticsearch_data

# postgres_data

# vue_dist


echo "----------------------------"
echo "Dump PKDB database"
echo "----------------------------"
# FIXME:
# sudo -u postgres pg_dump pkdb > $DIR/pkdb_dump.psql

