# Dokumentation

Übersicht der Anleitungen in diesem Repository.

## VPS installieren

### 1. Provider vorbereiten

- [`provider/1blu/prepare-kvm.md`](provider/1blu/prepare-kvm.md)  
  Leere KVM-Instanz bei 1blu erstellen und Ubuntu-Installation vorbereiten.

### 2. Ubuntu installieren

- [`ubuntu/install-ubuntu.md`](ubuntu/install-ubuntu.md)  
  Ubuntu 24.04 installieren, Netzwerk konfigurieren, Benutzer anlegen und SSH einrichten.

### 3. Ansible einrichten

- [`ansible/install-ansible.md`](ansible/install-ansible.md)  
  Ansible installieren, Collections, Ansible Vault und die benötigten Secrets einrichten und `site.yml` ausführen.

### 4. WireGuard einrichten

- [`wireguard/configure-client.md`](wireguard/configure-client.md)  
  Split-Tunnel- und Full-VPN-Clients für Windows oder Smartphone einrichten.

### 5. Pi-hole prüfen

- [`pihole/configure-pihole.md`](pihole/configure-pihole.md)  
  Pi-hole-Weboberfläche öffnen sowie DNS und Werbeblocker prüfen.

### 6. Vikunja einrichten

- [`vikunja/configure-vikunja.md`](vikunja/configure-vikunja.md)  
  Vikunja prüfen, ersten Benutzer anlegen und Clientzugriff konfigurieren.
- [`vikunja/backup-vikunja.md`](vikunja/backup-vikunja.md)  
  PostgreSQL-Datenbank und Vikunja-Dateien sichern und wiederherstellen.

## Dienste

- [`services.md`](services.md)  
  Übersicht aller Dienste, internen Namen, Ports, IP-Adressen und persistenten Datenpfade.

## Lokale Entwicklungsumgebung

- [`windows-wsl/install-docker.md`](windows-wsl/install-docker.md)  
  WSL 2 mit Ubuntu 24.04 und Docker Engine einrichten.

## Verzeichnisübersicht

```text
docs/
├── ansible/
│   └── install-ansible.md
├── pihole/
│   └── configure-pihole.md
├── provider/
│   └── 1blu/
│       └── prepare-kvm.md
├── ubuntu/
│   └── install-ubuntu.md
├── vikunja/
│   ├── backup-vikunja.md
│   └── configure-vikunja.md
├── windows-wsl/
│   └── install-docker.md
├── wireguard/
│   └── configure-client.md
├── services.md
└── README.md
```
