# VPS Setup

Dokumentation und Ansible-Konfiguration für einen Ubuntu-VPS mit Docker, Traefik, WireGuard, Pi-hole, Vikunja und Homepage.

## Dokumentation

Die vollständige Übersicht befindet sich unter [`docs/README.md`](docs/README.md).

### Installation

1. [1blu KVM-Instanz vorbereiten](docs/provider/1blu/prepare-kvm.md)
2. [Ubuntu 24.04 auf dem VPS installieren](docs/ubuntu/install-ubuntu.md)
3. [Ansible und Ansible Vault einrichten](docs/ansible/install-ansible.md)
4. [WireGuard-Clients einrichten](docs/wireguard/configure-client.md)
5. [Pi-hole einrichten und prüfen](docs/pihole/configure-pihole.md)
6. [Vikunja einrichten und prüfen](docs/vikunja/configure-vikunja.md)
7. [Homepage Dashboard einrichten und prüfen](docs/homepage/configure-homepage.md)

Die zentrale Übersicht aller Dienste und Zugriffe befindet sich unter [`docs/services.md`](docs/services.md).

Nach Verbindung mit WireGuard ist das zentrale Dashboard erreichbar unter:

```text
http://dashboard.home.arpa
```

### CI

GitHub Actions prüft Pull Requests und Pushes auf `main` automatisch auf YAML-/Ansible-Fehler, nicht renderbare Templates, ungültige Docker-Compose-Konfigurationen, Secrets und sicherheitsrelevante Fehlkonfigurationen. Es findet bewusst kein automatisches Deployment statt.

Details: [`docs/ci.md`](docs/ci.md)

### Lokale Umgebung

- [Docker unter WSL installieren](docs/windows-wsl/install-docker.md)

## WireGuard-Clients

Standard ist Split-Tunnel; für einen echten Full-VPN-Client wird ein separater Client angelegt und nur dessen `AllowedIPs` auf `0.0.0.0/0, ::/0` geändert.

Kurzanleitung: [`docs/wireguard/configure-client.md`](docs/wireguard/configure-client.md)

## Repository-Struktur

```text
.
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   ├── ci-requirements.txt
│   └── dependabot.yml
├── ansible/
│   ├── ci/
│   │   └── render-templates.yml
│   ├── group_vars/
│   │   └── all/
│   │       └── vars.yml
│   ├── inventory/
│   ├── roles/
│   │   ├── base/
│   │   ├── homepage/
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
│   ├── homepage/
│   ├── pihole/
│   ├── provider/
│   ├── ubuntu/
│   ├── vikunja/
│   ├── windows-wsl/
│   ├── wireguard/
│   ├── ci.md
│   ├── services.md
│   └── README.md
│
├── .ansible-lint
├── .gitattributes
├── .gitignore
├── .yamllint
└── README.md
```

## Ansible

Die Serverkonfiguration liegt unter [`ansible/`](ansible/). `site.yml` orchestriert die einzelnen Rollen; jeder Dienst hält seine Tasks und Compose-Templates in seiner eigenen Rolle.

Vor der ersten Ausführung müssen Ansible Vault und die lokalen Secrets eingerichtet werden.

Die vollständige Anleitung befindet sich unter:

[`docs/ansible/install-ansible.md`](docs/ansible/install-ansible.md)
