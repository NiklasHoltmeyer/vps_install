# Docker unter WSL einrichten

## 1. WSL + Ubuntu installieren

PowerShell als Administrator:

```powershell
wsl --install -d Ubuntu-24.04
```

Falls ein Neustart verlangt wird: Windows neu starten und anschließend Ubuntu einmal öffnen und Linux-Benutzer/Passwort anlegen.

Prüfen:

```powershell
wsl -l -v
```

Ubuntu sollte unter **WSL 2** laufen.

## 2. sudo ohne Passwort verwenden

Ubuntu/WSL öffnen:

```powershell
wsl
```

Dann:

```bash
echo "$USER ALL=(ALL:ALL) NOPASSWD:ALL" | sudo tee "/etc/sudoers.d/$USER-nopasswd" > /dev/null
sudo chmod 440 "/etc/sudoers.d/$USER-nopasswd"
sudo visudo -cf "/etc/sudoers.d/$USER-nopasswd"
```

Erwartung:

```text
parsed OK
```

> [!WARNING]
> `NOPASSWD:ALL` erlaubt dem WSL-Benutzer, beliebige Befehle ohne Passwort als `root` auszuführen.

## 3. Docker in Ubuntu installieren

Ubuntu/WSL öffnen:

```powershell
wsl
```

Dann:

```bash
sudo apt update
sudo apt install -y ca-certificates curl

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc

sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update

sudo apt install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin
```

Das installiert Docker Engine und `docker compose` direkt aus dem offiziellen Docker-Repository.

## 4. Docker ohne sudo verwenden

```bash
sudo usermod -aG docker $USER
```

> [!WARNING]
> Mitglieder der Gruppe `docker` besitzen praktisch **Root-Rechte** auf dem Linux-System.
>
> Füge daher nur vertrauenswürdige Benutzer zur `docker`-Gruppe hinzu.

WSL verlassen:

```bash
exit
```

Dann in PowerShell:

```powershell
wsl --shutdown
```

Danach testen:

```powershell
wsl docker run --rm hello-world
```

## 5. Docker direkt aus PowerShell verwenden

PowerShell-Profil öffnen:

```powershell
if (!(Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}

notepad $PROFILE
```

Folgendes eintragen:

```powershell
function docker {
    wsl.exe -d Ubuntu-24.04 -- docker @args
}

function docker-compose {
    wsl.exe -d Ubuntu-24.04 -- docker compose @args
}
```

Profil neu laden:

```powershell
. $PROFILE
```

Danach funktionieren beispielsweise:

```powershell
docker ps
docker compose up -d
docker-compose up -d
```
