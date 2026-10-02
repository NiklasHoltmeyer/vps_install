# Vikunja einrichten und prüfen

Vikunja wird durch Ansible zusammen mit einer PostgreSQL-Datenbank als Docker-Compose-Stack installiert. Der Zugriff erfolgt intern über Traefik und WireGuard.

## 1. Container prüfen

Auf dem VPS:

```bash
docker ps --filter name=vikunja
```

Erwartet werden:

```text
vikunja
vikunja-db
```

Logs prüfen:

```bash
docker logs vikunja --tail 100
docker logs vikunja-db --tail 100
```

## 2. DNS prüfen

Mit aktivem WireGuard-Tunnel auf dem Client:

```powershell
nslookup todo
```

Erwartete Adresse:

```text
172.30.0.2
```

Der bisherige Name `todo.home.arpa` bleibt zusätzlich als Alias erhalten und zeigt ebenfalls auf `172.30.0.2`.

## 3. Weboberfläche öffnen

WireGuard verbinden und danach öffnen:

```text
http://todo
```

Vikunja selbst lauscht intern auf Port `3456`; dieser Port wird nicht auf dem VPS veröffentlicht. Traefik übernimmt den Zugriff über `todo` und weiterhin zusätzlich über `todo.home.arpa`.

## 4. Ersten Benutzer anlegen

Standardmäßig ist in `group_vars/all/vars.yml` gesetzt:

```yaml
vikunja_registration_enabled: true
```

Ersten Benutzer über die Weboberfläche registrieren.

Wenn nur dieser Benutzer benötigt wird, anschließend setzen:

```yaml
vikunja_registration_enabled: false
```

und Ansible erneut ausführen:

```bash
cd ~/vps_install/ansible
ansible-playbook -i inventory/hosts.ini site.yml --vault-password-file ~/.ansible/vault-password
```

## 5. iPhone / mDone / Client

Als Server-URL verwenden:

```text
http://todo
```

Der Single-Label-Hostname ist für lokale iOS-Clients wie mDone vorgesehen. Der WireGuard-Tunnel muss aktiv sein, weil Vikunja nicht öffentlich freigegeben wird.

Für bestehende Browser-Lesezeichen funktioniert weiterhin:

```text
http://todo.home.arpa
```

## 6. Aktualisieren

Images herunterladen und Stack neu erstellen:

```bash
cd /opt/vikunja
docker compose pull
docker compose up -d
docker compose ps
```

Alternativ die Images über das Ansible-Playbook verwalten.

## 7. Wichtige Pfade

```text
/opt/vikunja/compose.yaml
/opt/vikunja/files
/opt/vikunja/db
```

Secrets liegen nicht im Repository, sondern in der lokalen verschlüsselten `group_vars/all/vault.yml`.
