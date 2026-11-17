# Manifest: Testbett Dokumentwissen

Alle geteilten Dateien. Freigegeben sind die Testdaten (zwei fiktive Dokumente, Faktenliste, zurückgehaltene Testfragen), die Bewertungsregel und eine Ergebnistabelle.

| Pfad | Zweck | Herkunft | Größe (Bytes) |
|---|---|---|---|
| `.gitignore` | schließt Caches und lokale Antwortdateien aus | neu erstellt | 155 |
| `requirements.txt` | keine externen Pakete | neu erstellt | 76 |
| `testbett/data/doc_quorvex.md` | fiktives Dokument: Firmenprofil Quorvex Instruments, 1.641 Tokens | Prototyp, unverändert | 7.065 |
| `testbett/data/doc_kethara.md` | fiktives Dokument: Planet Kethara, 1.513 Tokens | Prototyp, unverändert | 6.275 |
| `testbett/data/facts.jsonl` | 154 Fakten mit Goldantworten und Aliasen (Fakten, Zwei-Schritt-Ketten, Wortlaut-Sätze) | Prototyp, unverändert | 29.414 |
| `testbett/data/test_questions.jsonl` | 295 zurückgehaltene Testfragen: direkt, umformuliert, Zwei-Schritt, Umkehr, Wortlaut | Prototyp, unverändert | 60.616 |
| `testbett/score_answers.py` | Bewertungsregel (Alias-Abgleich nach Normalisierung, Wortlaut-Abgleich) mit Selbsttest | neu geschrieben aus der Prototyp-Bewertungsfunktion; reproduziert die gespeicherten Ergebnisse | 4.722 |
| `ergebnisse/ergebnisse.md` | Genauigkeit der Bedingungen A bis F nach Fragetyp und Dokument | neu geschrieben aus den Prototyp-Ergebnissen | 4.580 |
| `ergebnisse/ergebnisse.json` | dieselben Werte pro Lauf | abgeleitet aus den Prototyp-Zusammenfassungen | 6.856 |
| `MANIFEST.md` | diese Liste | neu erstellt | - |

Summe der aufgeführten Dateien: 119.759 Bytes (0,12 MB). `README.md` und `assets/` werden getrennt gepflegt und sind hier nicht aufgeführt.

## Voraussetzungen

- Python 3.8+, keine externen Pakete
- Aufrufe aus `testbett/`: `python score_answers.py --selftest`, `python score_answers.py antworten.jsonl` (eine Zeile `{"qid": ..., "answer": ...}` pro Frage)

## Nicht enthalten

- Trainings- und Datenerzeugungscode
- synthetische Trainingsdaten, Lehrerausgaben und Entwicklungsfragen
- Beschreibung der Bedingungen C bis F
- Modellgewichte und Rohantworten der Bedingungen
- weitere Varianten, Messprotokolle und Entwurfsnotizen
