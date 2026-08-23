# WireGuard nach Ansible-Installation einrichten

## 1. wg-easy öffnen

SSH-Verbindung mit lokalem Port-Forwarding aufbauen:

```powershell
ssh -L 51821:127.0.0.1:51821 -i "$HOME\.ssh\id_ed25519_vps" USER@SERVER_IP
```

`-L` richtet lokales Port-Forwarding ein:

```text
localhost:51821
```

auf dem eigenen PC wird über SSH auf

```text
127.0.0.1:51821
```

des Servers weitergeleitet.

Danach im Browser öffnen:

```text
http://localhost:51821
```

## 2. Client erstellen

In wg-easy:

```text
New Client
→ Namen vergeben
→ Konfiguration herunterladen oder QR-Code anzeigen
```

Die erzeugte Client-Konfiguration sollte für einen vollständigen VPN-Tunnel unter anderem Folgendes enthalten:

```ini
[Peer]
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = SERVER_IP_ODER_HOSTNAME:51822
```

`AllowedIPs = 0.0.0.0/0, ::/0` bedeutet, dass sowohl IPv4- als auch IPv6-Traffic über WireGuard geleitet werden.

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

Dann entweder:

```text
Add Tunnel
→ Scan from QR code
```

oder die `.conf` importieren.

Anschließend Tunnel aktivieren.

## 5. Internetzugriff prüfen

Nach dem Aktivieren des WireGuard-Tunnels zunächst prüfen, ob der Tunnel verbunden ist.

Auf dem Server:

```bash
docker exec wg-easy wg show
```

Bei einem verbundenen Client sollte beispielsweise Folgendes erscheinen:

```text
latest handshake: ... seconds ago
transfer: ... received, ... sent
```

Wenn kein `latest handshake` angezeigt wird, liegt das Problem noch vor dem eigentlichen Internet-Routing.

Danach auf dem Client testen:

```powershell
ping 10.8.0.1
```

Wenn das funktioniert:

```powershell
ping 1.1.1.1
```

Wenn auch das funktioniert:

```powershell
nslookup google.de
```

Damit lassen sich die Fehlerquellen unterscheiden:

```text
kein Handshake
    → Port / Firewall / WG_HOST prüfen

Handshake vorhanden, 10.8.0.1 nicht erreichbar
    → WireGuard-Konfiguration prüfen

10.8.0.1 erreichbar, 1.1.1.1 nicht erreichbar
    → Forwarding / NAT prüfen

1.1.1.1 erreichbar, google.de nicht erreichbar
    → DNS prüfen
```

## 6. Öffentliche IP prüfen

Wenn `WG_ALLOWED_IPS=0.0.0.0/0, ::/0` verwendet wird, läuft der komplette Internetverkehr über den VPS.

Vor Aktivierung von WireGuard die öffentliche IP prüfen.

Danach WireGuard aktivieren und erneut prüfen.

Die angezeigte öffentliche IPv4-Adresse sollte jetzt der öffentlichen IPv4-Adresse des VPS entsprechen.

## 7. Server-Konfiguration prüfen

Die von wg-easy erzeugte WireGuard-Konfiguration kann auf dem Server angezeigt werden:

```bash
docker exec wg-easy cat /etc/wireguard/wg0.conf
```

Wichtig ist insbesondere:

```ini
ListenPort = 51820
```

Der VPS verwendet dabei folgende Portweiterleitung:

```text
Internet
    ↓ UDP 51822
VPS
    ↓ Docker Port-Mapping
51822 → 51820
    ↓
wg-easy
    ↓
WireGuard ListenPort 51820
```

Die Client-Konfiguration verwendet dagegen:

```ini
Endpoint = SERVER_IP_ODER_HOSTNAME:51822
```

## 8. NAT und Forwarding prüfen

wg-easy v14 erstellt normalerweise automatisch die benötigten `iptables`-Regeln.

Prüfen:

```bash
docker exec wg-easy iptables -t nat -L POSTROUTING -n -v
```

Dort sollte eine `MASQUERADE`-Regel für das WireGuard-Netz vorhanden sein.

Zusätzlich:

```bash
docker exec wg-easy iptables -L FORWARD -n -v
```

Hier sollten Regeln für `wg0` vorhanden sein.

IPv4-Forwarding im Container prüfen:

```bash
docker exec wg-easy sysctl net.ipv4.ip_forward
```

Erwartung:

```text
net.ipv4.ip_forward = 1
```

## 9. UFW prüfen

Der externe WireGuard-Port muss auf dem VPS freigegeben sein:

```bash
sudo ufw status
```

Erwartet wird unter anderem:

```text
22/tcp       ALLOW
51822/udp    ALLOW
```

Der Web-Port `51821` muss nicht öffentlich freigegeben werden, wenn wg-easy ausschließlich über den SSH-Tunnel aufgerufen wird.

## 10. Nach Änderungen Container neu erstellen

Wenn die Compose-Konfiguration geändert wurde:

```bash
cd /opt/wg-easy
docker compose down
docker compose up -d
```

Danach:

```bash
docker compose ps
```

und:

```bash
docker exec wg-easy wg show
```

prüfen.

Wurde `WG_CONFIG_PORT`, `WG_ALLOWED_IPS`, DNS oder eine andere Einstellung verändert, sollte anschließend eine **neue Client-Konfiguration aus wg-easy heruntergeladen bzw. der QR-Code erneut eingescannt werden**.