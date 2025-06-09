import random
import shutil 
from collections import deque
import json
import os
from pathlib import Path

"""
Python‑Lernkarten‑Quiz zur Vorbereitung von Prüfungen.
Das Script lädt automatisch alle JSON-Dateien im aktuellen Verzeichnis,
die Lernkarten enthalten. Jede JSON-Datei sollte folgende Struktur haben:
{
  "title": "Themenname",
  "description": "Beschreibung",
  "flashcards": [
    {"question": "Frage", "answer": "Antwort"},
    ...
  ]
}
"""

def load_flashcards_from_json():
    current_dir = Path.cwd()
    json_files = list(current_dir.glob("*.json"))
    
    if not json_files:
        print("❌ Keine JSON-Dateien mit Lernkarten gefunden.")
        print("Erstelle JSON-Dateien mit folgender Struktur:")
        print("""
{
  "title": "Themenname",
  "description": "Beschreibung",
  "flashcards": [
    {"question": "Frage", "answer": "Antwort"},
    ...
  ]
}
        """)
        return []
    
    topics = []
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Validierung der JSON-Struktur
            if not all(key in data for key in ["title", "flashcards"]):
                print(f"⚠️ Überspringe {json_file.name}: Fehlende 'title' oder 'flashcards' Felder")
                continue
                
            if not isinstance(data["flashcards"], list):
                print(f"⚠️ Überspringe {json_file.name}: 'flashcards' muss eine Liste sein")
                continue
                
            # Umwandlung in das erwartete Format (Tupel für Kompatibilität)
            flashcards = []
            for card in data["flashcards"]:
                if "question" in card and "answer" in card:
                    flashcards.append((card["question"], card["answer"]))
                else:
                    print(f"⚠️ Überspringe Karte in {json_file.name}: Fehlende 'question' oder 'answer'")
            
            if flashcards:  # Nur hinzufügen wenn gültige Karten vorhanden
                topics.append({
                    "title": data["title"],
                    "description": data.get("description", ""),
                    "flashcards": flashcards,
                    "filename": json_file.name
                })
                print(f"✅ Geladen: {data['title']} ({len(flashcards)} Karten aus {json_file.name})")
            
        except json.JSONDecodeError as e:
            print(f"❌ Fehler beim Lesen von {json_file.name}: {e}")
        except Exception as e:
            print(f"❌ Unerwarteter Fehler bei {json_file.name}: {e}")
    
    return topics

def select_topics(available_topics):
    """Lässt den Benutzer auswählen, welche Topics er lernen möchte."""
    if not available_topics:
        return []
    
    if len(available_topics) == 1:
        print(f"\n📚 Einziges verfügbares Thema: {available_topics[0]['title']}")
        return available_topics
    
    print("\n📚 Verfügbare Lernthemen:")
    for i, topic in enumerate(available_topics, 1):
        desc = f" - {topic['description']}" if topic['description'] else ""
        print(f"  {i}) {topic['title']} ({len(topic['flashcards'])} Karten){desc}")
    
    print("\n🎯 Auswahl-Optionen:")
    print("  • Einzelne Themen: z.B. '1,3' oder '2'")
    print("  • Alle Themen: 'all' oder 'alle'")
    print("  • Beenden: 'q' oder 'quit'")
    
    while True:
        choice = input("\n» Welche Themen möchtest du lernen? ").strip().lower()
        
        if choice in ['q', 'quit']:
            return []
        
        if choice in ['all', 'alle']:
            print(f"\n✅ Alle {len(available_topics)} Themen ausgewählt")
            return available_topics
        
        try:
            # Parse Komma-getrennte Nummern
            selected_indices = []
            for num_str in choice.replace(' ', '').split(','):
                if num_str:
                    num = int(num_str)
                    if 1 <= num <= len(available_topics):
                        selected_indices.append(num - 1)
                    else:
                        raise ValueError(f"Nummer {num} außerhalb des Bereichs")
            
            if selected_indices:
                selected_topics = [available_topics[i] for i in selected_indices]
                topic_names = [t['title'] for t in selected_topics]
                print(f"\n✅ Ausgewählt: {', '.join(topic_names)}")
                return selected_topics
            else:
                print("❌ Keine gültige Auswahl")
                
        except ValueError as e:
            print(f"❌ Ungültige Eingabe: {e}")
            print("Bitte verwende Zahlen (z.B. '1,2,3'), 'all' oder 'q'")

def run_quiz():
    print("\n🧠 Lernkarten-Modus gestartet\n")
    
    # Lade alle verfügbaren Topics
    available_topics = load_flashcards_from_json()
    if not available_topics:
        print("❌ Keine Lernkarten gefunden. Beende Programm.")
        return
    
    # Benutzer wählt Topics aus
    selected_topics = select_topics(available_topics)
    if not selected_topics:
        print("\n👋 Keine Themen ausgewählt. Programm beendet.")
        return
    
    # Erstelle flashcards Dictionary für Kompatibilität mit existierender Logik
    flashcards = {}
    for topic in selected_topics:
        flashcards[topic["title"]] = topic["flashcards"]
    
    topics = list(flashcards.keys())
    total_cards_init = sum(len(flashcards[t]) for t in topics)     # Ausgangszahl
    seen = 0                       # insgesamt gezeigte Karten
    wrong_final = []               # Karten, die bis zuletzt falsch blieben

    for topic in topics:
        print(f"\n📚 Thema: {topic}\n{'-' * 40}")
        cards = deque(flashcards[topic][:])      # doppelt-ended queue
        random.shuffle(cards)
        total_cards = len(cards)                 # dynamisch: wächst bei Re-Insertion

        delay_queue = deque()   # (question, answer, counter) – wartet noch 2 Züge

        while cards:
            # -------- eventuell fällige Re-Insertion aus delay_queue -------- #
            if delay_queue and delay_queue[0][2] == 0:
                q_re, a_re, _ = delay_queue.popleft()
                cards.appendleft((q_re, a_re))   # sofort als Nächste fragen
                total_cards += 1                 # Fortschrittsbalken anpassen

            # -------- Karte ziehen -------- #
            question, answer = cards.popleft()
            seen += 1

            # -------- Fortschrittsbalken -------- #
            term_width = shutil.get_terminal_size().columns
            bar_len = min(30, term_width - 20)
            filled = int(bar_len * seen / total_cards)
            bar = "█" * filled + "░" * (bar_len - filled)
            print(f"[{bar}] {seen}/{total_cards}")

            # -------- Frage / Escape -------- #
            cmd = input(f"\n🃏 {question}\n⏎ = Antwort, q = Beenden » ").strip().lower()
            if cmd.startswith("q"):
                print("\n👋 Quiz abgebrochen.")
                _review_wrong(wrong_final + [qa[:2] for qa in delay_queue])
                return

            print(f"✅ Antwort: {answer}")

            # -------- Richtig? -------- #
            correct = input("Richtig beantwortet? (y/[n]) » ").strip().lower()
            if correct != "y":
                # ↓ in zwei Karten erneut abfragen
                delay_queue.append((question, answer, 2))
            else:
                # falls Karte zuvor schon im Re-Try-Modus war, nichts weiter tun
                pass

            # -------- Zähler für Delay-Karten herunterzählen -------- #
            delay_queue = deque([(q, a, c-1) for q, a, c in delay_queue])

        # Thema fertig – alles, was noch in delay_queue steckt, jetzt weiterziehen
        while delay_queue:
            q_re, a_re, c = delay_queue.popleft()
            cards.appendleft((q_re, a_re))
            total_cards += 1      # anpassen, falls Thema noch nicht durch
            # Schleife läuft weiter, weil while cards erneut aktiv wird
            while cards:
                break            # sofort zurück zur äußeren while – wird neu durchlaufen

    print("\n🎉 Alle Lernkarten durchlaufen!")
    _review_wrong(wrong_final)

# ------------------------------------------------------------------
def _review_wrong(wrong_cards):
    """End- oder Abbruch-Wiederholung der Karten, die bis zuletzt falsch waren."""
    if not wrong_cards:
        print("\n👍 Keine falschen Antworten übrig – stark!")
        return

    print(f"\n🔄 Noch {len(wrong_cards)} Karte(n) offen. Lass uns sie wiederholen!")
    for i, (q, a) in enumerate(wrong_cards, 1):
        input(f"\n❓ {i}. {q}\n⏎ = Antwort")
        print(f"✅ Antwort: {a}")
    print("\n🚀 Fertig – gute Arbeit!")

# ------------------------------------------------------------------

if __name__ == "__main__":
    run_quiz()