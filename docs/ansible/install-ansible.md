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

Pi-hole-Passwort generieren:

```bash
PIHOLE_PASSWORD="$(openssl rand -base64 32 | tr -d '\n')"
```

Optional anzeigen:

```bash
echo "$PIHOLE_PASSWORD"
```

Lokale `vault.yml` erstellen:

```bash
printf '%s\n' \
  '---' \
  "pihole_password: \"$PIHOLE_PASSWORD\"" \
  > group_vars/all/vault.yml
```

Variable wieder aus der Shell entfernen:

```bash
unset PIHOLE_PASSWORD
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

Die entschlüsselten Variablen sollten angezeigt werden.

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

Die lokale Vault-Datei bearbeiten:

```bash
ansible-vault edit \
  group_vars/all/vault.yml \
  --vault-password-file ~/.ansible/vault-password
```

Beispiel:

```yaml
---
pihole_password: "..."
nextcloud_admin_password: "..."
nextcloud_db_password: "..."
```

## 12. Wichtig

Folgende Dateien enthalten Secrets und werden nicht eingecheckt:

```text
~/.ansible/vault-password
group_vars/all/vault.yml
```

`group_vars/all/vault.yml` ist über `.gitignore` ausgeschlossen.

Bei einer vollständigen Neuinstallation werden Vault-Key und Secrets neu generiert.
