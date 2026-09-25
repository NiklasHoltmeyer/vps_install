# Dienste und Zugriffe

Zentrale Übersicht der durch Ansible installierten bzw. konfigurierten Dienste.

Die Webdienste sind absichtlich nicht öffentlich erreichbar. Interne Namen werden über Pi-hole auf Traefik (`172.30.0.2`) aufgelöst und sind nach Verbindung mit WireGuard erreichbar.

| Dienst | Zugriff | Port / Protokoll | Öffentlich | Daten |
| --- | --- | --- | --- | --- |
| SSH | VPS-IP | `22/tcp` | Ja | System |
| WireGuard | VPS-IP | `51822/udp` | Ja | `/volume1/docker/wireguard/Config` |
| wg-easy UI | `http://wireguard.home.arpa` | intern `51821/tcp` | Nein | wie WireGuard |
| Pi-hole UI | `http://pihole.home.arpa/admin/` | intern `80/tcp` | Nein | `/opt/pihole/etc-pihole` |
| Pi-hole DNS | `172.30.0.3` | intern `53/tcp+udp` | Nein | `/opt/pihole/etc-pihole` |
| Vikunja | `http://todo.home.arpa` | intern `3456/tcp` | Nein | `/opt/vikunja/files`, `/opt/vikunja/db` |
| PostgreSQL (Vikunja) | nur Compose-Netz | `5432/tcp` | Nein | `/opt/vikunja/db` |
| Traefik | `172.30.0.2` | intern `80/tcp` | Nein | `/opt/traefik` |

## Interne Docker-Adressen

| Dienst | Adresse |
| --- | --- |
| Traefik | `172.30.0.2` |
| Pi-hole | `172.30.0.3` |
| wg-easy | `172.30.0.4` |
| Vikunja | `172.30.0.5` |

Das gemeinsame Service-Netz ist `172.30.0.0/24`. Das WireGuard-Clientnetz ist `10.8.0.0/24`.

## Schnelltest

Mit aktivem WireGuard-Tunnel:

```powershell
nslookup pihole.home.arpa
nslookup wireguard.home.arpa
nslookup todo.home.arpa
```

Die drei Namen sollten auf `172.30.0.2` zeigen.
