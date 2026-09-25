# Homepage Dashboard einrichten und prüfen

Homepage wird durch Ansible als internes Dashboard installiert und ist ausschließlich über das bestehende WireGuard-/Pi-hole-/Traefik-Setup erreichbar.

## 1. Dashboard öffnen

WireGuard verbinden und im Browser öffnen:

```text
http://dashboard.home.arpa
```

Das Dashboard enthält Links auf alle aktuell vorhandenen Web-UIs:

- Vikunja
- Pi-hole
- wg-easy / WireGuard

Zusätzlich zeigt es den HTTP-Status dieser Dienste sowie einen reduzierten Docker-Systemstatus.

## 2. DNS prüfen

Auf einem verbundenen Client:

```powershell
nslookup dashboard.home.arpa
```

Erwartete Adresse:

```text
172.30.0.2
```

## 3. Container prüfen

Auf dem VPS:

```bash
docker ps --filter name=homepage
```

Erwartet werden:

```text
homepage
homepage-status
```

Logs des Dashboards:

```bash
docker logs homepage --tail 100
```

## 4. Docker-Systemstatus

Das Dashboard erhält absichtlich **keinen Zugriff auf `/var/run/docker.sock`**.

Stattdessen erzeugt ein systemd-Timer auf dem Host alle 30 Sekunden eine reduzierte JSON-Datei. Darin stehen ausschließlich:

```text
Containername
State
Status / Health
aggregierte Zähler
```

Nicht ausgegeben werden unter anderem:

```text
Umgebungsvariablen
Secrets
Container-Dateien
Logs
Docker-Inspect-Daten
```

Timer prüfen:

```bash
systemctl status homepage-docker-health.timer
systemctl list-timers homepage-docker-health.timer
```

Status manuell aktualisieren:

```bash
sudo /usr/local/bin/homepage-docker-health /opt/homepage/status/status.json
```

Ergebnis prüfen:

```bash
cat /opt/homepage/status/status.json
```

Als Problem gelten Container, die nicht `running` sind oder deren Docker-Healthcheck `unhealthy` meldet.

## 5. Konfiguration als Code

Die Homepage-Konfiguration wird vollständig über Ansible verwaltet:

```text
ansible/roles/homepage/templates/services.yaml.j2
ansible/roles/homepage/templates/settings.yaml.j2
ansible/roles/homepage/templates/widgets.yaml.j2
```

Neue Web-UIs werden dort ergänzt. Ein erneuter Ansible-Lauf schreibt die gewünschte Konfiguration nach `/opt/homepage/config`.

## 6. Sicherheit

Homepage veröffentlicht keinen eigenen Host-Port. Der Zugriff erfolgt nur über Traefik im internen VPN-Netz.

`HOMEPAGE_ALLOWED_HOSTS` ist auf `dashboard.home.arpa` beschränkt und nicht auf `*` gesetzt. Suchmaschinen-Indexierung und die externe Versionsprüfung sind deaktiviert.

Der interne `homepage-status`-HTTP-Server hängt nur im privaten Compose-Netz und hat keinen Host-Port. Er läuft ohne Linux-Capabilities und mit read-only Root-Dateisystem.

Es werden keine zusätzlichen Secrets für Homepage benötigt und keine Zugangsdaten anderer Dienste in die Dashboard-Konfiguration kopiert.

## 7. Aktualisieren

Über Ansible:

```bash
cd ~/vps_install/ansible
ansible-playbook \
  --vault-password-file=/root/.ansible/vault-password \
  -i inventory/hosts.ini \
  site.yml
```

Oder nur den Compose-Stack manuell:

```bash
cd /opt/homepage
docker compose pull
docker compose up -d
docker compose ps
```
