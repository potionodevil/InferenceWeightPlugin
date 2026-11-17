# Wissens-Kassetten

**Ein Sprachmodell beantwortet Fragen zu einem Dokument, ohne das Dokument im Kontext zu lesen.**

![Status](https://img.shields.io/badge/Status-Forschungsprototyp-orange)
![Sprache](https://img.shields.io/badge/Sprache-Deutsch-blue)
![Lizenz](https://img.shields.io/badge/Lizenz-Alle%20Rechte%20vorbehalten-lightgrey)

Forschungsprototyp, nicht veröffentlicht. Stand 17.11.2026.

## Auf einen Blick

- Mit eingesteckter Kassette beantwortet Qwen2.5-0.5B 97,2 % der direkten und 88,3 % der umformulierten Fragen. Mit dem Dokument im Kontext sind es 92,5 % und 76,7 % (gemessen).
- Der Prompt schrumpft von 1.629 auf 40 Tokens.
- Mehrschritt- und Umkehrfragen beantwortet das Kontextfenster besser: 69,2 % gegen 30,8 % und 71,4 % gegen 20,6 % (gemessen).
- Vollautomatisch erzeugte Kassetten erreichen 37,3 % gesamt, das Kontextfenster 82,4 % (gemessen).

Eine Kassette ist ein einmal erzeugtes, steckbares Wissensmodul für ein Dokument.

## Problem

- Lange Kontextfenster halten weniger, als sie versprechen. RULER: Llama 3.1 70B verspricht 128.000 Tokens und hält 64.000.
- NoLiMa: 11 von 13 Modellen fallen bei 32.000 Tokens unter die Hälfte ihrer Leistung bei kurzem Kontext.
- Studie Context Rot (2025): Ein Prompt mit etwa 300 Tokens schlägt die volle Historie mit 113.000 Tokens bei allen 18 getesteten Modellen.
- Kontext kostet Speicher. Der KV-Cache von Llama 3.1 8B belegt 131.072 Byte pro Token, also 13,1 GB für 100.000 Tokens. Bei Llama 3.1 70B sind es 32,8 GB (berechnet aus den öffentlichen Modellkonfigurationen).
- Den Kontext pflegen heute Entwickler von Hand oder Heuristiken. Anthropic Context Editing schneidet in einem Agenten-Test mit 100 Schritten 84 % der Tokens weg.

## Ergebnisse

Testbedingungen: Qwen2.5-0.5B-Instruct in bf16 auf einer RTX 3050 mit 6 GB. Zwei fiktive Dokumente: eine Firma (1.641 Tokens) und ein Planet (1.513 Tokens), je 60 geprüfte Fakten. 295 zurückgehaltene Testfragen, Greedy-Decoding. Ohne Dokument beantwortet das Modell 3,3 % der direkten Fragen, die Fakten sind ihm also unbekannt.

### Genauigkeit nach Fragetyp

Prozent richtig, Mittel über Startwerte (gemessen).

| Testbedingung | Startwerte | direkt (120) | umformuliert (120) | Mehrschritt (26) | Umkehr (21) | wörtlich (8) | gesamt (295) |
|---|---|---|---|---|---|---|---|
| ohne Dokument | 1 | 3,3 | 3,3 | 0,0 | 0,0 | 0,0 | 2,7 |
| Dokument im Kontext | 1 | 92,5 | 76,7 | 69,2 | 71,4 | 87,5 | 82,4 |
| Kassette, Variante A | 3 | 97,2 | 88,3 | 30,8 | 20,6 | 100 | 82,4 |
| Kassette, Variante B | 3 | 87,2 | 73,9 | 48,7 | 36,5 | 95,8 | 75,0 |
| Kassette, Variante C | 2 | 97,5 | 87,9 | 50,0 | 21,4 | 100 | 84,1 |
| Kassette, Variante D | 2 | 60,0 | 39,2 | 38,5 | 14,3 | 50,0 | 46,1 |
| Kassette, vollautomatisch | 1 | 45,8 | 33,3 | 30,8 | 33,3 | 0,0 | 37,3 |
| Kassette, Variante A2 | 1 | 95,0 | 85,8 | 34,6 | 95,2 | 100 | 86,1 |

- Die Varianten unterscheiden sich in der Erzeugung. Details sind nicht Teil dieses Repositorys.
- Variante A erreicht das Kontextfenster gesamt (82,4 gegen 82,4) mit anderem Profil. Sie ist besser bei umformulierten Fragen (88,3 gegen 76,7, gepaarter Test p = 0,035) und bei wörtlichen Zitaten (100 gegen 87,5).
- Variante C erreicht den höchsten Gesamtwert: 84,1 %.
- Variante A2 hebt die Umkehrfragen auf 95,2 %. Direkte und umformulierte Fragen bleiben bei 95,0 % und 85,8 %.
- Wörtliche Zitate: Die Varianten A und C geben alle 8 Sätze in jedem Startwert exakt wieder.

### Größe und Geschwindigkeit

Gemessen auf der RTX 3050, Batch 1.

| Größe | Kassette | Dokument im Kontext |
|---|---|---|
| Speicherbedarf | 8,8 bis 17,6 MB | 18,6 bis 20,2 MB |
| Prompt-Länge | 40 Tokens | 1.629 Tokens (Median) |
| Laden von der SSD | 261 ms | 10 ms (gespeicherter Kontextzustand) |
| Wechsel zwischen geladenen Kassetten | 17 ms | entfällt |
| Antwort mit 24 Tokens | 387 ms fest eingebunden, 812 ms steckbar | 394 ms zwischengespeichert, 520 ms neu eingelesen |

- Das Modell ohne Kassette und ohne Dokument braucht 384 ms für dieselbe Antwort.
- Drei Kassettengrößen: 8,8 MB ergeben 80,3 % gesamt, 17,6 MB 82,4 %, 70,4 MB 83,4 %.
- Erzeugung pro Dokument auf der RTX 3050: 93 s (A), 194 s (B), 273 s (C), 207 s (vollautomatisch). 50 kurze Dokumente vollautomatisch: 2,9 Stunden (berechnet aus Messwerten).

### Nebenwirkungen auf fremde Fragen

20 Fragen zu Allgemeinwissen und Perplexität auf WikiText-2 (gemessen).

| Modell | Allgemeinwissen richtig (von 20) | Perplexität |
|---|---|---|
| ohne Kassette | 18 | 15,7 |
| Variante A | 8 bis 12 | 41,5 bis 49,0 |
| Variante B | 16 bis 18 | 22,4 bis 24,2 |
| Variante C | 10 bis 18 | 29,9 bis 32,8 |
| Variante D | 13 bis 14 | 121 bis 164 |
| vollautomatisch | 15 bis 16 | 19,7 bis 19,9 |

- Beispiel mit eingesteckter Planeten-Kassette: Auf "What is the capital of France?" antwortet das Modell "Amberfall.".
- Prüfrunde 1: Eine Einstellung mit weniger Nebenwirkung hält Variante A bei 81,4 % gesamt. Allgemeinwissen steigt von 10 auf 15 von 20 im Mittel. Variante C: 83,1 % gesamt, Allgemeinwissen von 14 auf 16,5 von 20.

### Zwei Dokumente gleichzeitig

| Aufbau | gesamt (295 Fragen) | Art |
|---|---|---|
| zwei Kassetten zugleich eingesteckt, Variante A | 36,6 % | gemessen |
| zwei Kassetten zugleich eingesteckt, Variante B | 42,4 % | gemessen |
| eine gemeinsame Kassette für beide Dokumente | 82,4 % | gemessen |
| beide Dokumente im Kontext (3.150 Tokens) | 79,0 % | gemessen |

## Grenzen

- Ein kleines Modell mit 0,5 Mrd. Parametern und zwei kurze fiktive Dokumente. Größere Modelle und lange Dokumente sind ungetestet.
- Die besten Werte setzen vorbereitetes Begleitmaterial voraus, das jede geprüfte Tatsache abdeckt. Ein stärkeres Modell schrieb es mit Kenntnis der Testfakten. Das ist eine obere Schranke. Vollautomatisch sind es 37,3 %.
- Bei Mehrschritt- und Umkehrfragen verlieren die Kassetten klar gegen das Kontextfenster. Nur Variante A2 schließt die Lücke bei Umkehrfragen.
- Eine eingesteckte Kassette verändert Antworten auf fremde Fragen. Bei Variante A fällt das Allgemeinwissen von 18 auf 8 bis 12 von 20.
- Zwei zugleich eingesteckte Kassetten verlieren mehr als die Hälfte der Genauigkeit.
- Mit Dokument im Kontext verfehlt das 0,5B-Modell selbst 9 von 120 direkten Fragen. Der Vergleich läuft gegen einen schwachen Leser.
- Dieses Modell braucht nur 12.288 Byte Kontextspeicher pro Token. Die Kassette ist daher etwa so groß wie das Dokument im Kontext. Für Llama 3.1 8B wäre eine entsprechende Kassette (84 MB) ab etwa 640 Tokens Dokumentlänge kleiner als das Dokument im Kontext (berechnet, nicht gemessen).
- Startwerte verschieben einzelne Fragetypen um bis zu 19 Punkte. Unterschiede unter 15 Punkten bei Mehrschritt- und Umkehrfragen (26 und 21 Fragen) sind Rauschen.
- Die Zeiten stammen von einer geteilten Desktop-GPU, ohne Batching über mehrere Nutzer.

## Stand und Fahrplan

| Phase | Inhalt | Stand |
|---|---|---|
| Phase 1 | Prototyp mit 41 Kassetten, Labormessung | abgeschlossen |
| Prüfrunde 1 | Nachmessungen zu Nebenwirkungen und Kombination | abgeschlossen |
| Phase 2 | Benchmark gegen etablierte Baselines und größere Modelle | geplant |
| Phase 3 | Bibliothek aus 15 Kassetten, Schutz unbeteiligter Fragen | geplant |
| Phase 4 | Mehrschritt- und Umkehrfragen | geplant |
| Phase 5 | Vollautomatische Erzeugung ohne vorbereitetes Material | geplant |
| Phase 6 | Dokumente mit 10.000 bis 100.000 Tokens | geplant |

## Projektstruktur

```
wissens-kassetten/
  README.md
  MANIFEST.md
  requirements.txt
  testbett/      Testdaten, Generatoren, Bewertungsskripte
  ergebnisse/    Messwerte und Auswertungen
```

Das Repository enthält das Testbett und die Ergebnisse. Jede Datei steht mit Zweck und Größe in `MANIFEST.md`. Code und Methodik des Verfahrens sind nicht Teil dieses Repositorys.

## Zugehörige Arbeit

- Interner Forschungsbericht, November 2026, unveröffentlicht.
- Eigene Vorarbeit (2026): KI-Effizienz auf Consumer-Hardware. Unveröffentlicht.

## Lizenz

Alle Rechte vorbehalten. Keine Nutzung ohne Zustimmung.

Kontakt: auf Anfrage
