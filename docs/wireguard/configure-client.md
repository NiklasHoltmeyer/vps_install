# WireGuard nach Ansible-Installation einrichten

## 1. wg-easy öffnen

SSH-Verbindung mit lokalem Port-Forwarding aufbauen:

```powershell
ssh -L 51821:127.0.0.1:51821 -i "$HOME\.ssh\id_ed25519_vps" USER@SERVER_IP
```

Danach im Browser öffnen:

```text
http://localhost:51821
```

Der Port `51821` ist nur lokal auf dem VPS erreichbar und wird über SSH weitergeleitet.

## 2. Client erstellen

In wg-easy:

```text
New Client
→ Namen vergeben
→ Konfiguration herunterladen oder QR-Code anzeigen
```

Die Client-Konfiguration sollte enthalten:

```ini
[Interface]
DNS = 172.30.0.3

[Peer]
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = SERVER_IP:51822
```

`172.30.0.3` ist der Pi-hole-DNS-Server.

## 3. Windows

WireGuard installieren:

```text
https://www.wireguard.com/install/
```

Dann:

```text
Add Tunnel
→ Import tunnel(s) from file
→ .conf auswählen
→ Activate
```

## 4. Smartphone

WireGuard-App installieren.

Dann:

```text
Add Tunnel
→ Scan from QR code
```

oder die `.conf` importieren.

Anschließend Tunnel aktivieren.

## 5. Verbindung prüfen

Auf dem Server:

```bash
docker exec wg-easy wg show
```

Bei einem verbundenen Client sollte ein aktueller Handshake erscheinen:

```text
latest handshake: ... seconds ago
transfer: ... received, ... sent
```

Auf dem Client:

```powershell
ping 10.8.0.1
```

Danach:

```powershell
ping 1.1.1.1
```

DNS über Pi-hole prüfen:

```powershell
nslookup google.de 172.30.0.3
```

## 6. Öffentliche IP prüfen

Da

```ini
AllowedIPs = 0.0.0.0/0, ::/0
```

gesetzt ist, läuft der Internetverkehr über den VPS.

WireGuard aktivieren und anschließend die öffentliche IPv4-Adresse prüfen.

Sie sollte der öffentlichen IPv4-Adresse des VPS entsprechen.

## 7. Server-Konfiguration prüfen

```bash
docker exec wg-easy cat /etc/wireguard/wg0.conf
```

Wichtig:

```ini
ListenPort = 51822
```

Portfluss:

```text
Internet
    ↓ UDP 51822
VPS
    ↓
Docker 51822 → 51822
    ↓
wg-easy
```

Die Client-Konfiguration verwendet:

```ini
Endpoint = SERVER_IP:51822
```

## 8. Firewall prüfen

```bash
sudo ufw status
```

Erwartet:

```text
22/tcp       ALLOW
51822/udp    ALLOW
```

Port `51821` wird nicht öffentlich freigegeben.

## 9. Nach Änderungen

```bash
cd /opt/wg-easy
docker compose up -d
```

Danach:

```bash
docker compose ps
docker exec wg-easy wg show
```

Wenn DNS, `WG_PORT`, `WG_ALLOWED_IPS` oder andere Client-Einstellungen geändert wurden, eine neue Client-Konfiguration herunterladen bzw. den QR-Code erneut einscannen.
