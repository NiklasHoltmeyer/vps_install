# VPS Setup

Dokumentation und Ansible-Konfiguration für einen Ubuntu-VPS mit Docker, Traefik, WireGuard, Pi-hole und Vikunja.

## Dokumentation

Die vollständige Übersicht befindet sich unter [`docs/README.md`](docs/README.md).

### Installation

1. [1blu KVM-Instanz vorbereiten](docs/provider/1blu/prepare-kvm.md)
2. [Ubuntu 24.04 auf dem VPS installieren](docs/ubuntu/install-ubuntu.md)
3. [Ansible und Ansible Vault einrichten](docs/ansible/install-ansible.md)
4. [WireGuard-Clients einrichten](docs/wireguard/configure-client.md)
5. [Pi-hole einrichten und prüfen](docs/pihole/configure-pihole.md)
6. [Vikunja einrichten und prüfen](docs/vikunja/configure-vikunja.md)

Die zentrale Übersicht aller Dienste und Zugriffe befindet sich unter [`docs/services.md`](docs/services.md).

### Lokale Umgebung

- [Docker unter WSL installieren](docs/windows-wsl/install-docker.md)

## WireGuard-Clients

Standard ist Split-Tunnel; für einen echten Full-VPN-Client wird ein separater Client angelegt und nur dessen `AllowedIPs` auf `0.0.0.0/0, ::/0` geändert.

Kurzanleitung: [`docs/wireguard/configure-client.md`](docs/wireguard/configure-client.md)

## Repository-Struktur

```text
.
├── ansible/
│   ├── group_vars/
│   │   └── all/
│   │       └── vars.yml
│   ├── inventory/
│   ├── roles/
│   │   ├── base/
│   │   ├── pihole/
│   │   ├── traefik/
│   │   ├── vikunja/
│   │   └── wg_easy/
│   ├── ansible.cfg
│   ├── requirements.yml
│   └── site.yml
│
├── docs/
│   ├── ansible/
│   ├── pihole/
│   ├── provider/
│   ├── ubuntu/
│   ├── vikunja/
│   ├── windows-wsl/
│   ├── wireguard/
│   ├── services.md
│   └── README.md
│
├── .gitattributes
├── .gitignore
└── README.md
```

## Ansible

Die Serverkonfiguration liegt unter [`ansible/`](ansible/). `site.yml` orchestriert die einzelnen Rollen; jeder Dienst hält seine Tasks und Compose-Templates in seiner eigenen Rolle.

Vor der ersten Ausführung müssen Ansible Vault und die lokalen Secrets eingerichtet werden.

Die vollständige Anleitung befindet sich unter:

[`docs/ansible/install-ansible.md`](docs/ansible/install-ansible.md)
