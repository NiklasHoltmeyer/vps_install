# Ansible Server Setup

Anleitung, um den VPS nach einer Neuinstallation mit Ansible einzurichten.

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

## 3. Ansible-Verzeichnis öffnen

```bash
cd ~/vps_install/ansible
```

## 4. Ansible Collections installieren

```bash
ansible-galaxy collection install -r requirements.yml
```

## 5. Ansible Vault einrichten

Vault-Verzeichnis erstellen:

```bash
mkdir -p ~/.ansible
chmod 700 ~/.ansible
```

Vault-Master-Passwort generieren:

```bash
openssl rand -base64 48 > ~/.ansible/vault-password
chmod 600 ~/.ansible/vault-password
```

Der Vault-Key liegt ausschließlich unter:

```text
~/.ansible/vault-password
```

und darf niemals ins Git-Repository eingecheckt werden.

## 6. Secrets erzeugen

Secrets generieren:

```bash
PIHOLE_PASSWORD="$(openssl rand -base64 32 | tr -d '\n')"
VIKUNJA_DB_PASSWORD="$(openssl rand -base64 32 | tr -d '\n')"
VIKUNJA_SERVICE_SECRET="$(openssl rand -base64 48 | tr -d '\n')"
```

Lokale `vault.yml` erstellen:

```bash
cat > group_vars/all/vault.yml <<EOF
---
pihole_password: "$PIHOLE_PASSWORD"
vikunja_db_password: "$VIKUNJA_DB_PASSWORD"
vikunja_service_secret: "$VIKUNJA_SERVICE_SECRET"
EOF
```

Variablen wieder aus der Shell entfernen:

```bash
unset PIHOLE_PASSWORD VIKUNJA_DB_PASSWORD VIKUNJA_SERVICE_SECRET
```

## 7. `vault.yml` verschlüsseln

```bash
ansible-vault encrypt \
  group_vars/all/vault.yml \
  --vault-password-file ~/.ansible/vault-password
```

Prüfen:

```bash
head group_vars/all/vault.yml
```

Der Anfang muss so aussehen:

```text
$ANSIBLE_VAULT;1.1;AES256
```

Die Datei

```text
group_vars/all/vault.yml
```

bleibt ausschließlich lokal auf dem VPS und wird nicht ins Git-Repository eingecheckt.

## 8. Vault testen

```bash
ansible-vault view \
  group_vars/all/vault.yml \
  --vault-password-file ~/.ansible/vault-password
```

Erwartete Variablen:

```yaml
pihole_password: "..."
vikunja_db_password: "..."
vikunja_service_secret: "..."
```

## 9. Konfiguration prüfen

```bash
ansible-playbook \
  -i inventory/hosts.ini \
  site.yml \
  --syntax-check \
  --vault-password-file ~/.ansible/vault-password
```

## 10. Playbook ausführen

```bash
ansible-playbook \
  -i inventory/hosts.ini \
  site.yml \
  --vault-password-file ~/.ansible/vault-password
```

## 11. Secrets bearbeiten

```bash
ansible-vault edit \
  group_vars/all/vault.yml \
  --vault-password-file ~/.ansible/vault-password
```

## 12. Wichtig

Folgende Dateien enthalten Secrets und werden nicht eingecheckt:

```text
~/.ansible/vault-password
group_vars/all/vault.yml
```

`group_vars/all/vault.yml` ist über `.gitignore` ausgeschlossen.

Bei einer vollständigen Neuinstallation werden Vault-Key und Secrets neu generiert oder aus einem sicheren Backup wiederhergestellt.
