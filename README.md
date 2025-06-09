# Python Lernquiz

Ein interaktives Python-Lernkarten-Quiz zur Prüfungsvorbereitung mit JSON-basiertem Content-Management.

## Übersicht

Dieses Quiz-System wurde entwickelt, um das Lernen von Pflanzenarten, Vegetationstypen und ökologischen Zusammenhängen zu unterstützen, kann aber auf alle möglichen Gebiete angewendet werden. Das System trennt die Quiz-Logik vom Inhalt durch die Verwendung von JSON-Dateien, wodurch es einfach erweiterbar und anpassbar ist.

## Features

- **Adaptive Wiederholung**: Falsch beantwortete Karten werden automatisch erneut abgefragt
- **Fortschrittsanzeige**: Visueller Fortschrittsbalken während des Quiz
- **Themenauswahl**: Wähle einzelne Themen oder alle auf einmal
- **JSON-basiert**: Einfache Erweiterung durch neue JSON-Dateien
- **Auto-Erkennung**: Automatisches Laden aller Quiz-Dateien im Verzeichnis
- **Validierung**: Robuste Fehlerbehandlung und Strukturprüfung

## Beispiel Themenbereiche

Das Repository enthält vier Beispiel-Themenbereiche der Vegetationsökologie:

### 1. Biome der Welt (27 Karten)
- Äquatoriale Regenwälder
- Sommerfeuchte Savannen
- Subtropische Trockengebiete
- Immerfeuchte Subtropen
- Winterfeuchte Subtropen
- Steppengebiete
- Laubmischwälder der Mittelbreiten
- Boreale Wälder (Taiga)
- Polare & subpolare Zone (Tundra)

### 2. Vegetationsregionen Europas (26 Karten)
- Arktische Tundra (A1)
- Alpine Rasen & Zwergsträucher (A2)
- Birken-Kiefernwälder (B1-B3)
- Eichenmischwälder (T1-T2)
- Buchenwälder (T4)
- Mediterrane Vegetationstypen (M1-M2)
- Waldsteppen und Steppen (P1-P2)

### 3. Azonale Vegetation Europas (21 Karten)
- Dünen- und Küstensysteme
- Flussauen (Weichholz- und Hartholzauen)
- Moore und Feuchtgebiete
- Felsfluren
- Ökologische Anpassungsstrategien

### 4. Höhenstufen der Schweiz (30 Karten)
- **Kolline Stufe**: Buchenwälder, Eichenwälder, Kastanienwälder
- **Montane Stufe**: Weisstannen-Buchenwälder, Ahorn-Schluchtwald
- **Subalpine Stufe**: Fichtenwälder, Lärchen-Arvenwälder
- **Alpine Stufe**: Borstgrasweiden, Krummseggenrasen
- **Nivale Stufe**: Felsfluren

Damit kann die Funktion des Scripts getestet werden, ohne gleich eine eigene kompatible JSON Datei erstellen zu müssen.

## Installation & Verwendung

### Voraussetzungen
- Python 3.6 oder höher
- Keine zusätzlichen Pakete erforderlich (nur Standard-Bibliothek)

### Quiz starten
```bash
python3 lernquiz.py
```

### Bedienung
1. **Themenauswahl**: 
   - Einzelne Themen: `1,3` oder `2`
   - Alle Themen: `all` oder `alle`
   - Beenden: `q` oder `quit`

2. **Während des Quiz**:
   - `Enter` = Antwort anzeigen
   - `y` = Richtig beantwortet
   - `n` oder `Enter` = Falsch (wird wiederholt)
   - `q` = Quiz beenden

## Dateistruktur

```
├── lernquiz.py                      # Haupt-Quiz-Script
├── biome_der_welt.json             # Biome der Welt
├── vegetationsregionen_europas.json # Europäische Vegetationsregionen
├── azonale_vegetation_europas.json  # Azonale Vegetation
├── hoehenstufen_schweiz.json       # Schweizer Höhenstufen
└── README.md                       # Diese Dokumentation
```

## Eigene Inhalte hinzufügen

Das System kann einfach mit eigenen Lernkarten erweitert werden:

### 1. Neue JSON-Datei erstellen
```json
{
  "title": "Mein neues Thema",
  "description": "Beschreibung des Themas",
  "flashcards": [
    {
      "question": "Was ist Photosynthese?",
      "answer": "Der Prozess, bei dem Pflanzen aus CO₂ und Wasser unter Lichteinwirkung Glucose und Sauerstoff produzieren."
    },
    {
      "question": "Welche Rolle spielt Chlorophyll?",
      "answer": "Chlorophyll absorbiert Lichtenergie für die Photosynthese."
    }
  ]
}
```

### 2. Datei im Projektverzeichnis speichern
Das Script erkennt automatisch alle `.json`-Dateien im aktuellen Verzeichnis.

### 3. Quiz neu starten
Das neue Thema erscheint automatisch in der Themenauswahl.

## Lernstrategie

Das Quiz implementiert ein sehr grundlegendes **Spaced Repetition System**:

1. **Erste Runde**: Alle Karten werden einmal gezeigt
2. **Wiederholung**: Falsch beantwortete Karten kommen nach 2 anderen Karten erneut
3. **Endwiederholung**: Alle noch offenen Karten werden am Ende nochmals gezeigt

### Tipps für effektives Lernen:
- Beginne mit einem Thema, bevor du alle gleichzeitig lernst
- Wiederhole falsche Antworten mehrmals
- Notiere dir schwierige Arten/Konzepte separat
- Mache regelmäßige, kurze Lernsessions


## Beitragen

Verbesserungen und Erweiterungen sind willkommen! 

### Mögliche Erweiterungen:
- Multiple-Choice Modus
- Lernstatistiken und Performance-Tracking
- Timer-basierte Modi
- Spaced Repetition Algorithmus (SM-2)
- Fortschritt speichern zwischen Sessions
- Web-Interface

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe die Datei für Details.


---
