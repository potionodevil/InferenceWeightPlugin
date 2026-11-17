# Ergebnisse: 295 Testfragen zu zwei fiktiven Dokumenten

Mit dem Dokument im Kontext (B) beantwortet das Modell 82,4 % der Testfragen, ohne Kontext (A) 2,7 %. Die Bedingungen D und F erreichen 82,4 % und 84,1 % und liegen bei direkten und umformulierten Fragen über B. Bei Zwei-Schritt-Fragen (30,8 bis 50,0 %) und Umkehrfragen (14,3 bis 36,5 %) liegen C bis F unter B (69,2 % und 71,4 %).

Modell: Qwen2.5-0.5B-Instruct, bf16, greedy decoding, höchstens 48 neue Tokens (64 bei Zwei-Schritt- und Wortlautfragen). Bewertung: `testbett/score_answers.py`. Alle Zahlen pro Lauf: `ergebnisse.json`.

## Testset

- Dokumente: `testbett/data/doc_quorvex.md` (fiktive Firma, 1.641 Tokens) und `testbett/data/doc_kethara.md` (fiktiver Planet, 1.513 Tokens). Je 60 geprüfte Fakten, 4 Wortlaut-Sätze, 13 Zwei-Schritt-Ketten und 10 bis 11 Umkehrpaare, dazu ungeprüfter Fülltext mit Ablenkernamen und -zahlen.
- Faktenliste: `testbett/data/facts.jsonl` (154 Einträge: 120 Fakten, 26 Zwei-Schritt-Ketten, 8 Wortlaut-Sätze).
- Testfragen: `testbett/data/test_questions.jsonl`, 295 Fragen: 120 direkt (Wortlaut des Dokuments), 120 umformuliert, 26 Zwei-Schritt, 21 Umkehr, 8 Wortlaut.
- Umformulierte Fragen teilen 43 bis 52 % ihrer Inhaltswörter mit dem Dokument, direkte 88 bis 94 %.
- Regel: Eine Antwort ist richtig, wenn sie nach Normalisierung einen akzeptierten Alias jedes Goldteils enthält. Wortlautfragen brauchen den ganzen normalisierten Satz.
- Prompt für A und B: System "You are a helpful assistant. Answer the question in one short sentence." B setzt "Read the document and answer the question. Document: ... Question: ..." in die Nutzerzeile.

## Bedingungen

| Bedingung | Beschreibung | Läufe |
|---|---|---|
| A | ohne Kontext: Basismodell, nur die Frage | 1 |
| B | Dokument im Kontext: Basismodell, Dokument im Prompt | 1 |
| C, D, E, F | weitere Bedingungen ohne Dokument im Prompt | 2, 3, 3, 2 |

## Genauigkeit nach Fragetyp, beide Dokumente

Prozent richtig. Mehrere Läufe: Mittelwert ± Standardabweichung.

| Bedingung | Läufe | direkt (n=120) | umformuliert (n=120) | Zwei-Schritt (n=26) | Umkehr (n=21) | Wortlaut (n=8) | gesamt (n=295) |
|---|---|---|---|---|---|---|---|
| A: ohne Kontext | 1 | 3,3 | 3,3 | 0,0 | 0,0 | 0,0 | 2,7 |
| B: Dokument im Kontext | 1 | 92,5 | 76,7 | 69,2 | 71,4 | 87,5 | 82,4 |
| C | 2 | 60,0 ± 1,2 | 39,2 ± 3,5 | 38,5 ± 0,0 | 14,3 ± 0,0 | 50,0 ± 17,7 | 46,1 ± 1,4 |
| D | 3 | 97,2 ± 0,5 | 88,3 ± 1,4 | 30,8 ± 6,7 | 20,6 ± 2,7 | 100,0 ± 0,0 | 82,4 ± 1,0 |
| E | 3 | 87,2 ± 2,9 | 73,9 ± 1,0 | 48,7 ± 4,4 | 36,5 ± 9,9 | 95,8 ± 7,2 | 75,0 ± 1,4 |
| F | 2 | 97,5 ± 0,0 | 87,9 ± 0,6 | 50,0 ± 10,9 | 21,4 ± 3,4 | 100,0 ± 0,0 | 84,1 ± 1,0 |

### Nur Quorvex

| Bedingung | direkt | umformuliert | Zwei-Schritt | Umkehr | Wortlaut | gesamt |
|---|---|---|---|---|---|---|
| A: ohne Kontext | 1,7 | 1,7 | 0,0 | 0,0 | 0,0 | 1,4 |
| B: Dokument im Kontext | 91,7 | 73,3 | 61,5 | 63,6 | 100,0 | 79,7 |
| C | 61,7 ± 4,7 | 31,7 ± 9,4 | 26,9 ± 5,4 | 4,5 ± 6,4 | 25,0 ± 0,0 | 41,2 ± 1,0 |
| D | 95,0 ± 1,7 | 90,6 ± 4,2 | 35,9 ± 8,9 | 12,1 ± 5,2 | 100,0 ± 0,0 | 82,0 ± 2,7 |
| E | 85,6 ± 3,5 | 65,6 ± 2,5 | 33,3 ± 4,4 | 36,4 ± 9,1 | 91,7 ± 14,4 | 69,4 ± 1,4 |
| F | 95,0 ± 0,0 | 88,3 ± 0,0 | 38,5 ± 10,9 | 9,1 ± 0,0 | 100,0 ± 0,0 | 81,1 ± 1,0 |

### Nur Kethara

| Bedingung | direkt | umformuliert | Zwei-Schritt | Umkehr | Wortlaut | gesamt |
|---|---|---|---|---|---|---|
| A: ohne Kontext | 5,0 | 5,0 | 0,0 | 0,0 | 0,0 | 4,1 |
| B: Dokument im Kontext | 93,3 | 80,0 | 76,9 | 80,0 | 75,0 | 85,0 |
| C | 58,3 ± 2,4 | 46,7 ± 2,4 | 50,0 ± 5,4 | 25,0 ± 7,1 | 75,0 ± 35,4 | 51,0 ± 1,9 |
| D | 99,4 ± 1,0 | 86,1 ± 1,9 | 25,6 ± 11,8 | 30,0 ± 10,0 | 100,0 ± 0,0 | 82,8 ± 1,4 |
| E | 88,9 ± 2,5 | 82,2 ± 1,0 | 64,1 ± 4,4 | 36,7 ± 15,3 | 100,0 ± 0,0 | 80,7 ± 1,4 |
| F | 100,0 ± 0,0 | 87,5 ± 1,2 | 61,5 ± 10,9 | 35,0 ± 7,1 | 100,0 ± 0,0 | 87,1 ± 1,0 |

## Befunde

- Ohne Kontext kennt das Modell 3,3 % der direkten Fakten. Die Fakten sind ihm also unbekannt.
- D und F liegen bei umformulierten Fragen 11 Punkte über B (88,3 und 87,9 gegen 76,7) und bei Wortlautfragen bei 100 % gegen 87,5 %.
- Zwei-Schritt-Fragen: B 69,2 %, C bis F 30,8 bis 50,0 %.
- Umkehrfragen: B 71,4 %, C bis F 14,3 bis 36,5 %.
- Läufe verschieben einzelne Fragetypen um bis zu 19 Punkte (E Umkehr: 28,6, 33,3, 47,6 bei n = 21). Unterschiede unter etwa 15 Punkten bei Umkehr- und Zwei-Schritt-Fragen sind bei dieser Stichprobe Rauschen. Direkte und umformulierte Werte schwanken um 1 bis 3 Punkte.
