# Pi-hole einrichten und prüfen

Pi-hole wird durch Ansible als Docker-Container installiert und von WireGuard als DNS-Server verwendet.

## 1. Container prüfen

Auf dem VPS:

```bash
docker ps
```

Pi-hole sollte als laufender Container erscheinen.

Details:

```bash
docker logs pihole --tail 50
```

## 2. DNS prüfen

Pi-hole verwendet im Docker-Netz:

```text
172.30.0.3
```

Ein Split-Tunnel-Client sollte enthalten:

```ini
[Interface]
DNS = 172.30.0.3

[Peer]
AllowedIPs = 10.8.0.0/24, 172.30.0.0/24
```

Auf dem Client testen:

```powershell
nslookup google.de 172.30.0.3
```

> **Wichtig bei bestehenden WireGuard-Clients**
>
> Bereits vorhandene Clients übernehmen Änderungen von `WG_DEFAULT_DNS` oder `WG_ALLOWED_IPS` nicht automatisch.
>
> Konfiguration neu herunterladen bzw. QR-Code neu einscannen oder die Werte im bestehenden Tunnel manuell anpassen.

## 3. Weboberfläche öffnen

WireGuard verbinden.

Danach im Browser öffnen:

```text
http://pihole.home.arpa/admin/
```

Anmeldung mit dem über Ansible Vault gesetzten Pi-hole-Passwort.

## 4. Pi-hole-Passwort anzeigen

Auf dem VPS:

```bash
ansible-vault view group_vars/all/vault.yml --vault-password-file /root/.ansible/vault-password
```

## 5. Interne DNS-Namen prüfen

Pi-hole löst die internen Dienste auf Traefik auf.

Test:

```powershell
nslookup pihole.home.arpa
nslookup wireguard.home.arpa
```

Erwartete Adresse:

```text
172.30.0.2
```

## 6. DNS-Anfragen prüfen

In Pi-hole:

```text
Query Log
```

öffnen.

Beim Aufrufen von Webseiten sollten dort DNS-Anfragen des WireGuard-Clients erscheinen.

## 7. Pi-hole aktualisieren

Das Docker-Image wird über Ansible verwaltet.

Nach einer Änderung:

```bash
cd /opt/pihole
docker compose pull
docker compose up -d

docker compose ps
```

## 8. Wichtig

DNS-Port `53` wird nicht öffentlich auf dem VPS freigegeben.

Pi-hole ist nur innerhalb des Docker-/WireGuard-Setups als DNS-Server vorgesehen.
