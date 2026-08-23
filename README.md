# VPS Setup

Dokumentation und Ansible-Konfiguration für die Einrichtung eines Ubuntu-VPS, WireGuard und einer lokalen Docker-Umgebung unter WSL.

## Dokumentation

Die vollständige Übersicht befindet sich unter [`docs/README.md`](docs/README.md).

### Installation

1. [1blu KVM-Instanz vorbereiten](docs/provider/1blu/prepare-kvm.md)
2. [Ubuntu 24.04 auf dem VPS installieren](docs/ubuntu/install-ubuntu.md)
3. [Ansible auf dem Server installieren](docs/ansible/install-ansible.md)
4. [WireGuard-Client nach der Ansible-Installation einrichten](docs/wireguard/configure-client.md)

### Lokale Umgebung

- [Docker unter WSL installieren](docs/windows-wsl/install-docker.md)

## Repository-Struktur

```text
.
├── ansible/                 # Ansible-Konfiguration für den VPS
│   ├── group_vars/
│   ├── inventory/
│   ├── roles/
│   ├── templates/
│   ├── ansible.cfg
│   ├── requirements.yml
│   └── site.yml
├── docs/                    # Installations- und Betriebsdokumentation
│   ├── ansible/
│   ├── provider/
│   ├── ubuntu/
│   ├── windows-wsl/
│   └── wireguard/
├── .gitattributes
├── .gitignore
└── README.md
```

## Ansible

Die eigentliche Serverkonfiguration liegt unter [`ansible/`](ansible/).

Einstiegspunkt:

```bash
cd ansible
ansible-playbook site.yml
```
