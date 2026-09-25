# Continuous Integration

Dieses Repository verwendet GitHub Actions als CI-as-Code. Die Pipeline prüft Änderungen, führt aber bewusst kein Deployment auf dem VPS aus.

Workflow:

```text
.github/workflows/ci.yml
```

Die CI läuft automatisch bei Pull Requests, bei Pushes auf `main` und kann zusätzlich manuell über GitHub Actions gestartet werden.

## Checks

### YAML and Ansible lint

Prüft:

- YAML mit `yamllint`
- Ansible mit `ansible-lint`
- benötigte Ansible Collections aus `ansible/requirements.yml`

Die für CI verwendeten Python-Pakete sind in `.github/ci-requirements.txt` versioniert.

### Render and validate configuration

Prüft zuerst das komplette Playbook mit:

```bash
ansible-playbook -i inventory/hosts.ini site.yml --syntax-check
```

CI verwendet ausschließlich Dummy-Werte für Secrets. Es werden keine echten Vault-Dateien oder GitHub Secrets benötigt.

Danach rendert `ansible/ci/render-templates.yml` die produktiven Jinja-Templates mit Ansible. Dadurch werden auch Fehler erkannt, die ein reiner `--syntax-check` nicht findet, zum Beispiel eine nicht definierte Variable in einem Compose-Template.

Für alle gerenderten Compose-Dateien wird anschließend ausgeführt:

```bash
docker compose config --quiet
```

Zusätzlich wird das Homepage-Docker-Health-Skript kompiliert, ausgeführt und dessen JSON-Ausgabe validiert.

## Security scans

### Gitleaks

Gitleaks scannt die vollständige Git-Historie auf versehentlich eingecheckte Secrets. Die Ausgabe wird mit `--redact` bereinigt, damit gefundene Werte nicht erneut in CI-Logs erscheinen.

Es wird bewusst Gitleaks `v8.29.1` verwendet und per Container-Digest fixiert. `v8.30.1` wird nicht verwendet, da für diese Version 2026 eine Regression bei der Secret-Erkennung gemeldet wurde.

### Trivy

Trivy scannt das Repository auf:

- Secrets im aktuellen Dateistand
- IaC-/Konfigurationsfehler mit Schweregrad `HIGH` oder `CRITICAL`

Trivy läuft ohne Docker-Socket und erhält das Repository nur read-only.

## Supply-Chain-Schutz

Die verwendeten GitHub Actions sind nicht nur auf Major-Versionen, sondern auf konkrete Commit-SHAs gepinnt. Kommentare im Workflow dokumentieren die zugehörigen Release-Versionen.

Dependabot prüft wöchentlich Updates für GitHub Actions über:

```text
.github/dependabot.yml
```

Die Security-Scanner laufen als versionierte Container mit festem Digest.

## Kein Deployment

Die CI verbindet sich nicht mit dem VPS und besitzt keine SSH-Keys, Vault-Passwörter oder produktiven Zugangsdaten.

Deployment bleibt bewusst manuell, zum Beispiel:

```bash
var
```

Damit gilt:

```text
Pull Request -> CI -> Merge -> manuelles Deployment
```

## Merge-Schutz aktivieren

Nach dem ersten erfolgreichen Workflow-Lauf können die CI-Jobs als erforderliche Statuschecks für `main` konfiguriert werden. Dann kann ein Pull Request erst gemerged werden, wenn die gewünschten Checks erfolgreich sind.

Sinnvolle Required Checks sind:

```text
YAML and Ansible lint
Render and validate configuration
Security scans
```
