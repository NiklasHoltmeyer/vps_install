# Ubuntu 24.04 VPS – Installation

Kurzanleitung für die Installation eines Ubuntu-24.04-Servers auf einer leeren KVM-VM.

## 1. SSH-Key lokal erstellen

Unter Windows in PowerShell:

```powershell
ssh-keygen -t ed25519 -a 100 -f "$HOME\.ssh\id_ed25519_vps" -C "vps"
```

Optional eine Passphrase setzen.

Danach existieren:

```text
$HOME\.ssh\id_ed25519_vps       # Private Key
$HOME\.ssh\id_ed25519_vps.pub   # Public Key
```

Der **Private Key bleibt ausschließlich lokal**.

Public Key anzeigen:

```powershell
Get-Content "$HOME\.ssh\id_ed25519_vps.pub"
```

Den kompletten Public Key bei GitHub hinterlegen:

https://github.com/settings/keys

Dort:

```text
SSH and GPG keys
→ New SSH key
```

Nur die `.pub`-Datei bzw. deren Inhalt hochladen.

---

## 2. Netzwerk im Ubuntu-Installer

Wenn DHCP/automa­tische Netzwerkkonfiguration nicht funktioniert:

```text
Network connections
→ Netzwerkkarte auswählen, z. B. ens3
→ Edit IPv4
→ Manual
```

Folgende Werte werden benötigt:

```text
Subnet / Network:
    Subnetz des Servers, z. B. 192.0.2.0/24

Address / IP Address:
    Öffentliche IPv4-Adresse des Servers

Gateway / Default Gateway:
    Gateway des Providers

Name servers / DNS servers:
    DNS-Server

Search domains:
    normalerweise leer
```

Beispiel:

```text
Subnet:        192.0.2.0/24
Address:       192.0.2.123
Gateway:       192.0.2.1
Name servers:  1.1.1.1,8.8.8.8
Search domains:
```

Die konkreten Werte müssen aus dem VPS-/Provider-Control-Panel übernommen werden.

### Begriffe

Je nach Installer oder Provider können die Felder unterschiedlich heißen:

| Ubuntu Installer | Andere übliche Bezeichnung |
|---|---|
| `Subnet` | Subnetz, Network, Network Address, CIDR |
| `Address` | IP Address, IPv4 Address, Server IP |
| `Gateway` | Default Gateway, Router |
| `Name servers` | DNS Server, DNS Resolver |
| `Search domains` | DNS Search Domain |

Bei einer Netzmaske wie:

```text
255.255.255.0
```

entspricht das beispielsweise:

```text
/24
```

Bei:

```text
255.255.252.0
```

entspricht das:

```text
/22
```

IPv6 kann zunächst automatisch konfiguriert oder später eingerichtet werden.

---

## 3. Proxy

Im Ubuntu-Installer:

```text
Proxy address:
```

normalerweise **leer lassen**.

Nur konfigurieren, wenn der Provider oder das eigene Netzwerk ausdrücklich einen HTTP-Proxy verlangt.

---

## 4. Festplatte

Für einen einfachen VPS:

```text
(X) Use an entire disk

[ ] Set up this disk as an LVM group
[ ] Encrypt the LVM group with LUKS
```

Damit entsteht im Wesentlichen eine große Linux-Partition:

```text
/   ext4
```

Für einen normalen VPS sind LVM und LUKS nicht zwingend erforderlich.

Bei LUKS muss insbesondere bedacht werden, dass nach einem Server-Neustart unter Umständen über die VPS-Konsole ein Passwort eingegeben werden muss.

---

## 5. Benutzer und Servername

Beispiel:

```text
Your name:          beliebiger Anzeigename
Your server's name: vps
Username:           admin
Password:           <starkes Passwort>
```

### Servername

`Your server's name` ist der Linux-Hostname.

Beispiel:

```text
vps
```

Er wird später beispielsweise angezeigt bei:

```bash
hostname
```

oder:

```text
admin@vps
```

Der Hostname muss nicht der Domain oder dem vom Provider vergebenen Servernamen entsprechen.

### Benutzername

Einen normalen Benutzer verwenden, beispielsweise:

```text
admin
```

Nicht direkt als `root` arbeiten. Der angelegte Benutzer erhält normalerweise `sudo`-Rechte.

---

## 6. OpenSSH im Ubuntu-Installer

Aktivieren:

```text
[X] Install OpenSSH server
```

Danach:

```text
Import SSH key
→ GitHub
```

Den GitHub-Benutzernamen angeben.

Ubuntu lädt dann die unter

https://github.com/settings/keys

hinterlegten **Public Keys** herunter und trägt sie für den Benutzer in:

```text
~/.ssh/authorized_keys
```

ein.

Der Private Key wird **nicht** auf GitHub gespeichert und nicht auf den Server kopiert.

Passwort-Authentifizierung zunächst aktiviert lassen, bis der Login mit dem SSH-Key erfolgreich getestet wurde.

---

## 7. SSH-Verbindung testen

Nach Abschluss der Ubuntu-Installation:

```powershell
ssh -i "$HOME\.ssh\id_ed25519_vps" admin@SERVER_IP
```

Beispiel:

```powershell
ssh -i "$HOME\.ssh\id_ed25519_vps" admin@192.0.2.123
```

Wenn der Login funktioniert, ist der SSH-Key korrekt eingerichtet.

---

## 8. Optional: SSH-Config anlegen

Datei:

```text
$HOME\.ssh\config
```

Inhalt:

```text
Host vps
    HostName SERVER_IP
    User admin
    IdentityFile ~/.ssh/id_ed25519_vps
```

Beispiel:

```text
Host vps
    HostName 192.0.2.123
    User admin
    IdentityFile ~/.ssh/id_ed25519_vps
```

Danach reicht:

```powershell
ssh vps
```

---

## 9. SSH absichern

Sobald der SSH-Key-Login erfolgreich getestet wurde, kann die Passwort-Authentifizierung deaktiviert werden.

Neue SSH-Konfiguration anlegen:

```bash
sudo tee /etc/ssh/sshd_config.d/00-hardening.conf > /dev/null <<'EOF'
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
EOF
```

Konfiguration prüfen:

```bash
sudo sshd -t
```

Wenn keine Fehlermeldung ausgegeben wird:

```bash
sudo systemctl reload ssh
```

> [!WARNING]
> Die bestehende SSH-Verbindung noch **nicht schließen**.
>
> Zuerst in einem zweiten Terminal eine neue Verbindung mit dem SSH-Key testen:
>
> ```powershell
> ssh -i "$HOME\.ssh\id_ed25519_vps" USER@SERVER_IP
> ```
>
> Erst wenn diese Verbindung erfolgreich funktioniert, die bestehende SSH-Sitzung schließen.

Danach:

```text
- System aktualisieren
- Firewall konfigurieren
- benötigte Dienste installieren
```

---

## 10. Per SSH verbinden

Falls auf derselben IP bereits vorher ein anderes bzw. neu installiertes System lief, kann noch ein alter SSH-Host-Key lokal gespeichert sein. Dann zuerst den alten Eintrag entfernen:

```powershell
ssh-keygen -R SERVER_IP
```

Anschließend mit dem privaten SSH-Key verbinden:

```powershell
ssh -i "$HOME\.ssh\id_ed25519_vps" USER@SERVER_IP
```

Beispielhafte Platzhalter:

```text
USER       = angelegter Ubuntu-Benutzer
SERVER_IP  = öffentliche IP-Adresse des VPS
```

Beim ersten Verbindungsaufbau den angezeigten Host-Key/Fingerprint prüfen und anschließend die Verbindung bestätigen.