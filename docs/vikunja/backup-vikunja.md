# Vikunja sichern und wiederherstellen

Für ein vollständiges Backup werden die PostgreSQL-Datenbank und das Vikunja-Dateiverzeichnis benötigt.

## Backup

Backup-Verzeichnis anlegen:

```bash
sudo mkdir -p /var/backups/vikunja
```

Datenbank exportieren:

```bash
sudo docker exec vikunja-db \
  pg_dump -U vikunja -d vikunja -Fc \
  > /var/backups/vikunja/vikunja-db.dump
```

Dateien sichern:

```bash
sudo tar -C /opt/vikunja \
  -czf /var/backups/vikunja/vikunja-files.tar.gz \
  files
```

Backups prüfen:

```bash
ls -lh /var/backups/vikunja/
```

## Restore

Stack anhalten:

```bash
cd /opt/vikunja
sudo docker compose down
```

Dateien wiederherstellen:

```bash
sudo rm -rf /opt/vikunja/files
sudo tar -C /opt/vikunja -xzf /var/backups/vikunja/vikunja-files.tar.gz
sudo chown -R 1000 /opt/vikunja/files
```

Datenbankcontainer wieder starten:

```bash
cd /opt/vikunja
sudo docker compose up -d db
```

Bestehende Datenbank leeren und Dump importieren:

```bash
sudo docker exec vikunja-db \
  dropdb -U vikunja --if-exists vikunja

sudo docker exec vikunja-db \
  createdb -U vikunja -O vikunja vikunja

cat /var/backups/vikunja/vikunja-db.dump | \
  sudo docker exec -i vikunja-db \
  pg_restore -U vikunja -d vikunja --clean --if-exists
```

Anschließend den kompletten Stack starten:

```bash
cd /opt/vikunja
sudo docker compose up -d
sudo docker compose ps
```

Nach einem Restore `http://todo.home.arpa` öffnen und Aufgaben, Projekte und Anhänge prüfen.
