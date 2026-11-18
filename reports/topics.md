# Topic sulle massime

Generato da `src/analysis/topics.py`.

- Massime usate: 46,126 (testo oltre 50 caratteri); vocabolario: 8,000 parole.
- Coerenza NPMI per numero di topic: K=10: 0.1912, K=20: 0.2031, K=30: 0.1937, K=40: 0.1845, K=50: 0.1786, K=60: 0.1598.
- K scelto con la regola fissata (il più piccolo entro il 2% del migliore): **20**.
- Stabilità su 5 seed (Jaccard medio delle prime 20 parole, miglior abbinamento): 0.309 (min 0.283).
- Pronunce con materia: 22,107; peso medio del topic dominante 0.47; pronunce con più di un topic sopra 0,2: 57.3%.
- Verifica con i titoli delle massime (dal 2015, prime voci con almeno 30 massime, 7,455 massime): informazione mutua normalizzata 0.313, contro 0.025 con topic rimescolati.
- Verifica con il primo parametro costituzionale (35,991 massime): NMI 0.177, contro 0.011 rimescolando.

| Topic | Massime | Parole più pesanti | Prima voce dei titoli più frequente (dal 2015) |
| --- | --- | --- | --- |
| 0 | 2,391 | lavoro, trattamento, rapporto, lavoratori, pensione, servizio, dipendenti, diritto, indennita, lavoratore, retribuzione, previdenziale | previdenza |
| 1 | 4,964 | tutela, regionale, attività, principio, materia, nazionale, disciplina, amministrazione, servizio, esercizio, pubblico, pubblica | sanità pubblica |
| 2 | 381 | fattispecie, straniero, territorio, descrizione, cittadini, lgs, soggiorno, arresto, stranieri, italiana, rientro, ingresso | pronunce della corte costituzionale |
| 3 | 2,210 | legislatore, principio, trattamento, disciplina, scelta, discrezionalità, rispetto, scelte, situazioni, fattispecie, ragionevolezza, irragionevole | reati e pene |
| 4 | 3,369 | ricorso, conflitto, regione, consiglio, presidente, attribuzione, regionale, giudizio, ministri, confronti, atto, ricorrente | bilancio e contabilità pubblica |
| 5 | 1,187 | reg, aree, beni, piano, impianti, governo, edilizia, territorio, regionale, opere, interventi, illegittimo | edilizia e urbanistica |
| 6 | 2,673 | diritto, imposta, civ, legittimita, pagamento, cod, puo, tutela, principio, reddito, interessi, valore | tributi |
| 7 | 2,557 | gia, legittimita, manifesta, infondatezza, red, sanzione, sanzioni, sent, inammissibilita, penale, costituzionalmente, polizia | paesaggio |
| 8 | 5,042 | giudizio, oggetto, rilevanza, motivazione, eccezione, via, principale, difetto, rimessione, incidentale, giudizi, inammissibili | prospettazione della questione incidentale |
| 9 | 4,441 | regioni, regione, competenza, materia, regionale, statuto, statale, competenze, speciale, province, provincia, legislativa | bilancio e contabilità pubblica |
| 10 | 2,813 | decreto, rilevanza, bis, convertito, atti, modificazioni, luglio, dicembre, conversione, manifesta, restituzione, legittimita | sopravvenienze nel giudizio incidentale |
| 11 | 621 | dichiarate, personale, fondate, sollevate, red, dipendenti, rev, legittimita, siciliana, economico, regionale, regione | impiego pubblico |
| 12 | 462 | mass, precedenti, diritto, tutela, precedente, rispetto, diritti, contratto, costituzionalmente, legislatore, ordinamento, garanzia | pronunce della corte costituzionale |
| 13 | 1,604 | spese, spesa, risorse, fondo, periodo, pubblica, contributo, copertura, legislatore, bilancio, anno, oneri | bilancio e contabilità pubblica |
| 14 | 1,640 | pena, cod, misura, pen, sospensione, misure, reato, persona, precedenti, reati, sociale, rispetto | reati e pene |
| 15 | 1,249 | interpretazione, citate, europea, parametri, diritto, motivazione, parametro, unione, cedu, precedenti, plurimis, violazione | interpretazione della norma censurata |
| 16 | 4,758 | cod, penale, proc, pen, processo, imputato, procedimento, giudizio, codice, diritto, pubblico, difesa | processo penale |
| 17 | 596 | camera, parlamentare, tribunale, deputati, poteri, esercizio, funzioni, espresse, opinioni, parlamento, parlamentari, evocati | parlamento |
| 18 | 1,619 | regionale, regione, finanza, materia, enti, statale, siciliana, finanziaria, pubblica, bilancio, coordinamento, spesa | bilancio e contabilità pubblica |
| 19 | 1,549 | decreto, lgs, delega, testo, legislativo, vigore, disciplina, entrata, violazione, dicembre, materia, delegato | thema decidendum |