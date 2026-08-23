# Ansible Server Setup

Kurze Anleitung, um den Server nach einer Neuinstallation wieder mit Ansible aufzusetzen.

## 1. System vorbereiten

```bash
sudo ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime
echo "Europe/Berlin" | sudo tee /etc/timezone

sudo DEBIAN_FRONTEND=noninteractive dpkg --configure tzdata
sudo dpkg --configure -a
sudo apt --fix-broken install -y

sudo apt update
sudo apt upgrade -y
```

## 2. Ansible installieren

```bash
bash <<'EOF'
set -euo pipefail

echo "==> Paketlisten aktualisieren"
sudo apt update

echo "==> Ansible installieren"
sudo apt install -y ansible

echo "==> Installation prüfen"
ansible --version

echo "==> Ansible wurde erfolgreich installiert."
EOF
```

## 3. Ansible Collections installieren

Die in `requirements.yml` definierten Collections installieren:

```bash
ansible-galaxy collection install -r requirements.yml
```

## 4. Playbook ausführen

```bash
ansible-playbook site.yml
```
