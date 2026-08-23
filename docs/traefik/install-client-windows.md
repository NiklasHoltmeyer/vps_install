# Windows Hosts-Konfiguration

Die internen Dienste des VPS werden über Traefik unter der privaten Domain

```text
home.arpa
```

bereitgestellt.

Aktuell verfügbar:

| Dienst | URL |
|---|---|
| WireGuard Admin | `http://wireguard.home.arpa` |

> `home.arpa` ist ausschließlich für interne/private Namensauflösung gedacht.

## 1. Traefik-IP bestimmen

Die IP des Traefik-Containers muss in die Windows-`hosts`-Datei eingetragen werden.

Auf dem VPS:

```bash
docker inspect \
  --format '{{with index .NetworkSettings.Networks "traefik"}}{{.IPAddress}}{{end}}' \
  traefik
```

Beispiel:

```text
172.30.0.2
```

### Optionale Bash-Funktion

Die Funktion kann beispielsweise in `/root/.bashrc` hinterlegt werden:

```bash
function traefik-ip() {
    docker inspect \
        --format '{{with index .NetworkSettings.Networks "traefik"}}{{.IPAddress}}{{end}}' \
        traefik
}
```

Danach:

```bash
source /root/.bashrc
```

Die IP kann anschließend jederzeit mit

```bash
traefik-ip
```

ermittelt werden.

Beispiel:

```text
172.30.0.2
```

---

## 2. Windows Hosts-Datei bearbeiten

Die Datei befindet sich unter:

```text
C:\Windows\System32\drivers\etc\hosts
```

Editor oder Terminal dafür **als Administrator** starten.

Für WireGuard beispielsweise:

```text
172.30.0.2 wireguard.home.arpa
```

Dabei muss `172.30.0.2` durch die Ausgabe von

```bash
traefik-ip
```

ersetzt werden.

---

## 3. DNS-Cache leeren

Nach einer Änderung der Hosts-Datei:

```powershell
ipconfig /flushdns
```

Anschließend testen:

```powershell
ping wireguard.home.arpa
```

Die Ausgabe sollte auf die Traefik-IP zeigen:

```text
Pinging wireguard.home.arpa [172.30.0.2]
```

---

## 4. WireGuard Admin öffnen

Zuerst die WireGuard-Verbindung herstellen.

Danach:

```text
http://wireguard.home.arpa
```

Der Request läuft dann über:

```text
Windows
   │
   │ WireGuard
   ▼
Traefik
   │
   ▼
wg-easy:51821
```

Der interne Port `51821` muss dadurch nicht mehr direkt im Browser angegeben werden.

---

## Interne Hostnamen

Alle Dienste können auf dieselbe Traefik-IP zeigen.

Beispiel für die Windows-Hosts-Datei:

```text
172.30.0.2 wireguard.home.arpa
172.30.0.2 nextcloud.home.arpa
172.30.0.2 grafana.home.arpa
172.30.0.2 traefik.home.arpa
```

Mögliche Links:

| Dienst | Interner Name | URL |
|---|---|---|
| WireGuard Admin | `wireguard.home.arpa` | `http://wireguard.home.arpa` |
| Nextcloud | `nextcloud.home.arpa` | `http://nextcloud.home.arpa` |
| Grafana | `grafana.home.arpa` | `http://grafana.home.arpa` |
| Traefik Dashboard | `traefik.home.arpa` | `http://traefik.home.arpa` |

Die zusätzlichen Namen funktionieren erst, nachdem der jeweilige Dienst in Traefik konfiguriert wurde.

### Hinweis zu CNAMEs

Die Windows-`hosts`-Datei unterstützt keine echten DNS-`CNAME`-Records.

Stattdessen werden mehrere Namen direkt derselben IP zugeordnet:

```text
172.30.0.2 wireguard.home.arpa
172.30.0.2 nextcloud.home.arpa
172.30.0.2 grafana.home.arpa
```

Traefik entscheidet anhand des angefragten Hostnamens, an welchen Container die Anfrage weitergeleitet wird.

Mit einem späteren internen DNS-Server könnten stattdessen echte DNS-Einträge verwendet werden, beispielsweise:

```text
proxy.home.arpa       A       172.30.0.2
wireguard.home.arpa   CNAME   proxy.home.arpa
nextcloud.home.arpa   CNAME   proxy.home.arpa
grafana.home.arpa     CNAME   proxy.home.arpa
```