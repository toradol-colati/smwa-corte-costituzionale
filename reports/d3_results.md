# D3 - memoria collegiale

Generato da `src/analysis/d3_memoria_collegiale.py`.

Odds ratio di `sat_not_drafted`: quanto più spesso il redattore cita un precedente deciso da un collegio in cui sedeva (senza averlo redatto) rispetto a un precedente deciso mentre era in carica ma assente. Errori standard raggruppati per redattore.

| Analisi | Pronunce che citano | Citazioni | Citazioni a precedenti con redattore assente | OR | IC 95% | p |
| --- | --- | --- | --- | --- | --- | --- |
| **Principale** | 13,654 | 46,969 | 1,658 | 1.00 | 0.92–1.09 | 1 |
| controlli aggiuntivi (tipo del precedente, citazioni ricevute) | 13,654 | 46,969 | 1,658 | 1.00 | 0.92–1.09 | 0.97 |
| senza autocitazioni del redattore | 13,654 | 32,325 | 1,639 | 0.99 | 0.91–1.08 | 0.87 |
| solo pronunce dalla 287/1986 (redattore osservato) | 11,076 | 41,320 | 1,430 | 1.01 | 0.93–1.10 | 0.8 |
| solo pronunce fino alla 286/1986 (relatore come approssimazione) | 2,565 | 4,895 | 167 | 1.01 | 0.77–1.33 | 0.94 |
| senza gli anni dell'arretrato (citanti 1987-1989 escluse) | 12,542 | 44,949 | 1,549 | 1.04 | 0.96–1.13 | 0.33 |
| senza le ordinanze di correzione | 13,574 | 46,875 | 1,658 | 1.00 | 0.92–1.09 | 0.99 |
| solo sentenze che citano | 7,370 | 32,001 | 1,150 | 1.05 | 0.96–1.14 | 0.28 |
| solo ordinanze che citano | 6,284 | 14,968 | 508 | 0.91 | 0.78–1.05 | 0.21 |
| citanti fino al 2000 | 7,179 | 15,971 | 597 | 0.92 | 0.78–1.08 | 0.29 |
| citanti dal 2001 | 6,475 | 30,998 | 1,061 | 1.03 | 0.95–1.13 | 0.48 |
| solo giudizi in via incidentale | 10,079 | 29,470 | 982 | 1.01 | 0.91–1.12 | 0.86 |
| testo intero (anche Ritenuto in fatto) | 14,406 | 52,453 | 1,899 | 0.99 | 0.90–1.09 | 0.86 |
| con le citazioni delle massime (note editoriali) | 13,844 | 48,212 | 1,702 | 0.99 | 0.91–1.08 | 0.79 |
| controllo per norma impugnata in comune (esplorativo) | 13,654 | 46,969 | 1,658 | 0.99 | 0.91–1.07 | 0.8 |

**Tutti i coefficienti del modello principale**

| Variabile | OR | IC 95% | p |
| --- | --- | --- | --- |
| self_drafted | 5.466 | 4.765–6.271 | 7.6e-130 |
| sat_not_drafted | 1.000 | 0.918–1.089 | 1 |
| topic_similarity | 168.424 | 139.623–203.165 | 0 |
| age_1_2 | 0.750 | 0.701–0.801 | 2.7e-17 |
| age_2_3 | 0.548 | 0.501–0.599 | 1.3e-39 |
| age_3_4 | 0.420 | 0.380–0.465 | 2.3e-63 |
| age_4_5 | 0.354 | 0.316–0.396 | 4.5e-73 |
| age_5_7 | 0.289 | 0.257–0.325 | 1.2e-95 |
| age_7_10 | 0.258 | 0.217–0.308 | 5.5e-52 |
| age_10_15 | 0.279 | 0.154–0.505 | 2.5e-05 |

Sensibilità al campione dei controlli (altri 5 seed), OR: 0.994, 1.009, 0.986, 0.983, 0.989.

Gruppi (redattori): 122. Righe: 728,876.

**Modello completo** (tutti i precedenti; riferimento: precedente deciso prima dell'ingresso del redattore)

| Variabile | OR | IC 95% | p |
| --- | --- | --- | --- |
| self_drafted | 7.239 | 6.231–8.410 | 1.3e-147 |
| sat_not_drafted | 0.875 | 0.801–0.957 | 0.0033 |
| in_mandate_absent | 0.885 | 0.771–1.015 | 0.08 |
| topic_similarity | 280.549 | 239.856–328.146 | 0 |
| age_1_2 | 0.685 | 0.631–0.744 | 3.5e-19 |
| age_2_3 | 0.507 | 0.458–0.562 | 1.2e-38 |
| age_3_4 | 0.390 | 0.348–0.438 | 1.3e-58 |
| age_4_5 | 0.330 | 0.295–0.371 | 2.6e-79 |
| age_5_7 | 0.257 | 0.228–0.289 | 3.1e-112 |
| age_7_10 | 0.174 | 0.152–0.198 | 2.5e-151 |
| age_10_15 | 0.108 | 0.093–0.126 | 6.5e-172 |
| age_15_20 | 0.073 | 0.061–0.086 | 5.2e-199 |
| age_20_30 | 0.048 | 0.039–0.058 | 7.1e-217 |
| age_30_200 | 0.025 | 0.021–0.030 | 0 |