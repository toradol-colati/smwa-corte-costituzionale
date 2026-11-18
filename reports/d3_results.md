# D3 - memoria collegiale

Generato da `src/analysis/d3_memoria_collegiale.py`.

Odds ratio di `sat_not_drafted`: quanto più spesso il redattore cita un precedente deciso da un collegio in cui sedeva (senza averlo redatto) rispetto a un precedente deciso mentre era in carica ma assente. Errori standard raggruppati per redattore.

| Analisi | Pronunce che citano | Citazioni | Citazioni a precedenti con redattore assente | OR | IC 95% | p |
| --- | --- | --- | --- | --- | --- | --- |
| **Principale** | 13,654 | 46,969 | 1,658 | 1.03 | 0.96–1.10 | 0.49 |
| controlli aggiuntivi (tipo del precedente, citazioni ricevute) | 13,654 | 46,969 | 1,658 | 1.04 | 0.98–1.10 | 0.21 |
| senza autocitazioni del redattore | 13,654 | 32,325 | 1,639 | 1.00 | 0.94–1.07 | 0.97 |
| solo pronunce dalla 287/1986 (redattore osservato) | 11,076 | 41,320 | 1,430 | 1.04 | 0.97–1.11 | 0.29 |
| solo pronunce fino alla 286/1986 (relatore come approssimazione) | 2,565 | 4,895 | 167 | 1.00 | 0.78–1.27 | 0.97 |
| senza gli anni dell'arretrato (citanti 1987-1989 escluse) | 12,542 | 44,949 | 1,549 | 1.06 | 0.99–1.13 | 0.095 |
| senza le ordinanze di correzione | 13,574 | 46,875 | 1,658 | 1.03 | 0.96–1.10 | 0.48 |
| solo sentenze che citano | 7,370 | 32,001 | 1,150 | 1.05 | 0.99–1.13 | 0.12 |
| solo ordinanze che citano | 6,284 | 14,968 | 508 | 0.95 | 0.83–1.08 | 0.4 |
| citanti fino al 2000 | 7,179 | 15,971 | 597 | 0.93 | 0.80–1.07 | 0.31 |
| citanti dal 2001 | 6,475 | 30,998 | 1,061 | 1.05 | 0.99–1.12 | 0.13 |
| solo giudizi in via incidentale | 10,079 | 29,470 | 982 | 1.03 | 0.94–1.13 | 0.48 |
| testo intero (anche Ritenuto in fatto) | 14,406 | 52,453 | 1,899 | 1.02 | 0.94–1.10 | 0.67 |
| con le citazioni delle massime (note editoriali) | 13,844 | 48,212 | 1,702 | 1.01 | 0.95–1.09 | 0.69 |

**Tutti i coefficienti del modello principale**

| Variabile | OR | IC 95% | p |
| --- | --- | --- | --- |
| self_drafted | 3.011 | 2.667–3.399 | 5.8e-71 |
| sat_not_drafted | 1.025 | 0.955–1.101 | 0.49 |
| topic_similarity | 56.307 | 49.593–63.929 | 0 |
| age_1_2 | 0.826 | 0.788–0.867 | 8e-15 |
| age_2_3 | 0.678 | 0.634–0.724 | 1.1e-30 |
| age_3_4 | 0.565 | 0.522–0.611 | 2.8e-46 |
| age_4_5 | 0.500 | 0.457–0.546 | 1.6e-52 |
| age_5_7 | 0.433 | 0.395–0.474 | 3.5e-71 |
| age_7_10 | 0.388 | 0.340–0.443 | 1.7e-44 |
| age_10_15 | 0.374 | 0.248–0.565 | 2.9e-06 |

Sensibilità al campione dei controlli (altri 5 seed), OR: 1.020, 1.032, 1.020, 1.014, 1.019.

Gruppi (redattori): 122. Righe: 728,876.

**Modello completo** (tutti i precedenti; riferimento: precedente deciso prima dell'ingresso del redattore)

| Variabile | OR | IC 95% | p |
| --- | --- | --- | --- |
| self_drafted | 1.778 | 1.572–2.011 | 6e-20 |
| sat_not_drafted | 0.962 | 0.918–1.008 | 0.1 |
| in_mandate_absent | 0.973 | 0.910–1.042 | 0.44 |
| topic_similarity | 31.705 | 27.620–36.394 | 0 |
| age_1_2 | 0.879 | 0.843–0.916 | 1.4e-09 |
| age_2_3 | 0.790 | 0.751–0.832 | 3.3e-19 |
| age_3_4 | 0.719 | 0.672–0.770 | 2.8e-21 |
| age_4_5 | 0.676 | 0.628–0.727 | 1.7e-25 |
| age_5_7 | 0.593 | 0.546–0.643 | 3.8e-36 |
| age_7_10 | 0.474 | 0.432–0.521 | 1.4e-55 |
| age_10_15 | 0.349 | 0.316–0.387 | 8.9e-92 |
| age_15_20 | 0.265 | 0.241–0.291 | 2.3e-166 |
| age_20_30 | 0.201 | 0.179–0.225 | 1.3e-171 |
| age_30_200 | 0.133 | 0.119–0.148 | 2e-296 |