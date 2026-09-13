# VPS Setup

Dokumentation und Ansible-Konfiguration für einen Ubuntu-VPS mit Docker, Traefik, WireGuard und Pi-hole.

## Dokumentation

Die vollständige Übersicht befindet sich unter [`docs/README.md`](docs/README.md).

### Installation

1. [1blu KVM-Instanz vorbereiten](docs/provider/1blu/prepare-kvm.md)
2. [Ubuntu 24.04 auf dem VPS installieren](docs/ubuntu/install-ubuntu.md)
3. [Ansible und Ansible Vault einrichten](docs/ansible/install-ansible.md)
4. [WireGuard-Client einrichten](docs/wireguard/configure-client.md)
5. [Pi-hole einrichten und prüfen](docs/pihole/configure-pihole.md)

### Lokale Umgebung

- [Docker unter WSL installieren](docs/windows-wsl/install-docker.md)

## Repository-Struktur

```text
.
├── ansible/
│   ├── group_vars/
│   │   └── all/
│   │       └── vars.yml
│   ├── inventory/
│   ├── roles/
│   ├── templates/
│   ├── ansible.cfg
│   ├── requirements.yml
│   └── site.yml
│
├── docs/
│   ├── ansible/
│   ├── pihole/
│   ├── provider/
│   ├── ubuntu/
│   ├── windows-wsl/
│   └── wireguard/
│
├── .gitattributes
├── .gitignore
└── README.md
```

## Ansible

Die Serverkonfiguration liegt unter [`ansible/`](ansible/).

Vor der ersten Ausführung müssen Ansible Vault und die lokalen Secrets eingerichtet werden.

Die vollständige Anleitung befindet sich unter:

[`docs/ansible/install-ansible.md`](docs/ansible/install-ansible.md)
