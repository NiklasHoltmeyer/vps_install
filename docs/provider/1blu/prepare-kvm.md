# 1blu VPS – Leere KVM-Instanz für Ubuntu vorbereiten

Diese Anleitung beschreibt die Vorbereitung einer **leeren KVM-Instanz bei 1blu**, bevor Ubuntu über eine eigene ISO installiert wird.

## 1. Leere KVM-Instanz erstellen

Im 1blu-Control-Panel:

```text
Neuinstallation
→ Betriebssystem auswählen
→ Leere KVM-Instanz
→ Ubuntu
→ Installieren
```

Danach steht eine leere virtuelle Maschine zur Verfügung, auf der Ubuntu manuell per ISO installiert werden kann.

---

## 2. Ubuntu-ISO hochladen

Auf der **Übersicht-Seite** des Servers die FTP-Zugangsdaten auslesen.

Die gewünschte Ubuntu-Server-ISO herunterladen, z. B.:

```text
Ubuntu Server 24.04 LTS
```

Die ISO vor dem Upload umbenennen in:

```text
boot.iso
```

Anschließend `boot.iso` über FTP mit den von 1blu bereitgestellten Zugangsdaten hochladen.

Wichtig:

```text
Dateiname: boot.iso
```

Die Reihenfolge von **Schritt 1 und Schritt 2** ist grundsätzlich egal. Entscheidend ist nur, dass vor dem Start der Installation sowohl die leere KVM-Instanz als auch die `boot.iso` vorhanden sind.

---

## 3. Installation starten

Voraussetzungen:

```text
- Leere KVM-Instanz wurde erstellt
- boot.iso wurde hochgeladen
```

Auf der **Übersicht-Seite**:

```text
Booten von DVD
```

auswählen.

Danach:

```text
VNC-Fernsteuerung beantragen
```

Die Bereitstellung der VNC-Verbindung kann etwas dauern.

Erst warten, bis die VNC-Fernsteuerung vollständig bereitgestellt wurde.

Anschließend über VNC verbinden.

Der Server sollte jetzt von `boot.iso` starten und den Ubuntu-Installer anzeigen.

Ab hier mit der separaten **Ubuntu-24.04-VPS-Installationsanleitung** fortfahren.

---

## 4. Nach abgeschlossener Ubuntu-Installation

Nachdem Ubuntu vollständig installiert wurde:

Auf der **Übersicht-Seite**:

```text
Booten von HDD
```

einstellen.

Dadurch startet der VPS künftig von der installierten virtuellen Festplatte und nicht erneut von `boot.iso`.

Danach die bestehende VNC-Verbindung nicht weiterverwenden, sondern:

```text
VNC-Fernsteuerung neu generieren lassen
```

Anschließend kann der Server bei Bedarf über die neu erzeugte VNC-Verbindung kontrolliert werden.

Im Normalbetrieb sollte die Administration danach über SSH erfolgen.

---

## Kurzablauf

```text
1. Neuinstallation
   → Leere KVM-Instanz
   → Ubuntu
   → Installieren

2. FTP-Daten auf der Übersicht-Seite auslesen
   → Ubuntu-ISO in boot.iso umbenennen
   → boot.iso per FTP hochladen

3. Übersicht-Seite
   → Booten von DVD
   → VNC-Fernsteuerung beantragen
   → auf Bereitstellung warten
   → Ubuntu installieren

4. Nach der Installation
   → Booten von HDD
   → VNC-Fernsteuerung neu generieren

5. Danach
   → per SSH mit dem installierten Ubuntu verbinden
```
