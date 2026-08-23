# Dokumentation

Übersicht der Anleitungen in diesem Repository.

## VPS installieren

### 1. Provider vorbereiten

- [`provider/1blu/prepare-kvm.md`](provider/1blu/prepare-kvm.md)  
  Leere KVM-Instanz bei 1blu erstellen, Ubuntu-ISO als `boot.iso` hochladen und die Installation über VNC starten.

### 2. Ubuntu installieren

- [`ubuntu/install-ubuntu.md`](ubuntu/install-ubuntu.md)  
  Ubuntu 24.04 installieren, Netzwerk konfigurieren, Benutzer anlegen und SSH-Key-Zugriff einrichten.

### 3. Ansible installieren

- [`ansible/install-ansible.md`](ansible/install-ansible.md)  
  Server vorbereiten, Ansible installieren, Collections aus `requirements.yml` installieren und `site.yml` ausführen.

### 4. WireGuard einrichten

- [`wireguard/configure-client.md`](wireguard/configure-client.md)  
  Auf wg-easy per SSH-Port-Forwarding zugreifen und WireGuard-Clients für Windows oder Smartphone einrichten.

## Lokale Entwicklungsumgebung

- [`windows-wsl/install-docker.md`](windows-wsl/install-docker.md)  
  WSL 2 mit Ubuntu 24.04 einrichten, Docker Engine installieren und Docker aus PowerShell verwenden.

## Verzeichnisübersicht

```text
docs/
├── ansible/
│   └── install-ansible.md
├── provider/
│   └── 1blu/
│       └── prepare-kvm.md
├── ubuntu/
│   └── install-ubuntu.md
├── windows-wsl/
│   └── install-docker.md
├── wireguard/
│   └── configure-client.md
└── README.md
```
