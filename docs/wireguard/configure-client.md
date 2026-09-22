# WireGuard-Clients einrichten

Split-Tunnel schickt nur interne VPS-Netze durch WireGuard, Full-VPN schickt den gesamten Internetverkehr durch den VPS.

## 1. wg-easy öffnen

Auf dem eigenen Rechner:

```powershell
ssh -L 51821:127.0.0.1:51821 -i "$HOME\.ssh\id_ed25519_vps" USER@SERVER_IP
```

Dann öffnen:

```text
http://localhost:51821
```

## 2. Split-Tunnel-Client anlegen

In wg-easy:

```text
New Client
→ z. B. windows-split
→ Konfiguration herunterladen / QR-Code anzeigen
```

Die erzeugte Konfiguration soll enthalten:

```ini
[Interface]
DNS = 172.30.0.3

[Peer]
AllowedIPs = 10.8.0.0/24, 172.30.0.0/24
Endpoint = SERVER_IP:51822
```

Importieren und aktivieren.

## 3. Full-VPN-Client anlegen

In wg-easy einen separaten Client anlegen:

```text
New Client
→ z. B. phone-full
→ Konfiguration herunterladen
```

In der heruntergeladenen `.conf` nur diese Zeile ändern:

```ini
AllowedIPs = 0.0.0.0/0, ::/0
```

Danach importieren; eine zweite WireGuard-Instanz auf dem VPS ist nicht nötig.

> Bei erneutem Download der Full-VPN-Konfiguration muss `AllowedIPs` erneut angepasst werden, weil wg-easy v14 den Split-Tunnel als globalen Standard erzeugt.

## 4. Windows

```text
WireGuard
→ Add Tunnel
→ Import tunnel(s) from file
→ .conf auswählen
→ Activate
```

## 5. Smartphone

```text
WireGuard-App
→ Add Tunnel
→ QR-Code scannen oder .conf importieren
```

Für das Handy kannst du z. B. zwei Profile behalten:

```text
phone-split
phone-full
```

## 6. Prüfen

Auf dem VPS:

```bash
docker exec wg-easy wg show
```

Split-Tunnel:

```powershell
nslookup google.de 172.30.0.3
```

Full-VPN: öffentliche IP prüfen; sie sollte der VPS-IP entsprechen.

## 7. Nach Ansible-Änderungen

```bash
cd /opt/wg-easy
docker compose up -d

docker compose ps
docker exec wg-easy wg show
```

Bestehende Clients übernehmen Änderungen an `WG_DEFAULT_DNS` oder `WG_ALLOWED_IPS` nicht automatisch und müssen neu heruntergeladen oder manuell angepasst werden.
