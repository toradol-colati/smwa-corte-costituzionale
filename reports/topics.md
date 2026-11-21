# La materia delle pronunce, ricavata dalle massime

Prodotto da `src/analysis/topics.py`. Per sapere di che cosa parla ogni pronuncia, un programma (un modello LDA) legge i testi delle massime e raggruppa in temi le parole che compaiono spesso insieme. Ogni massima riceve un peso per ogni tema; la materia di una pronuncia è la media dei pesi delle sue massime.

## In breve

Questo file descrive come è stata ricavata la materia di ogni pronuncia, con le prove fatte per scegliere il numero di temi e per controllarli. I temi vanno d'accordo con i titoli delle massime e con gli articoli della Costituzione invocati, molto più che per caso; però cambiano parecchio ripetendo il calcolo, e alcuni raccolgono formule ricorrenti di scrittura più che una materia. Per questo la materia serve come controllo nei confronti, non come classificazione precisa.

## I numeri principali

- **Che cosa è stato letto.** 46.126 massime, quelle con un testo di più di 50 caratteri. Parole considerate: 8.000, tolte quelle troppo comuni o troppo rare.
- **Quanti temi.** Il programma è stato provato con 10, 20, 30, 40, 50, 60 temi. Per ogni prova si misura quanto le parole principali di ogni tema compaiono davvero insieme nelle massime (la "coerenza", misurata con l'NPMI: più è alta, meglio è): 10 temi: 0,1912; 20 temi: 0,2031; 30 temi: 0,1937; 40 temi: 0,1845; 50 temi: 0,1786; 60 temi: 0,1598. La regola, decisa prima, sceglie il numero più piccolo con una coerenza entro il 2% della migliore: **20 temi**.
- **Quanto sono stabili i temi.** Il calcolo è stato rifatto partendo da altri 4 punti di partenza casuali (semi). Ogni tema è stato confrontato con il tema più simile del nuovo calcolo, guardando le prime 20 parole (indice di Jaccard: 1 vuol dire le stesse parole, 0 nessuna in comune). In media l'indice vale 0,309, al minimo 0,283: ripetendo il calcolo i temi cambiano parecchio.
- **Le pronunce.** Pronunce con una materia: 22.107. In media il tema principale pesa 0,47; il 57,3% delle pronunce ha più di un tema con un peso di almeno 0,2.
- **Controllo con i titoli delle massime.** Dal 2015 il titolo di ogni massima comincia con una voce di classificazione (per esempio "reati e pene"). Sulle 7.455 massime con una voce che compare almeno 30 volte, temi e voci vanno d'accordo con un valore di 0,313 (informazione mutua normalizzata: 0 nessun legame, 1 corrispondenza perfetta), contro 0,025 se i temi vengono rimescolati a caso.
- **Controllo con gli articoli della Costituzione.** Con il primo articolo della Costituzione invocato nella massima (35.991 massime): 0,177, contro 0,011 rimescolando.

## I temi

Per ogni tema: quante massime lo hanno come tema principale; le 12 parole che pesano di più, scritte come le legge il programma (a volte senza accenti, come "puo" e "gia", e con le abbreviazioni dei testi, come "lgs" per decreto legislativo e "cod" per codice); la voce dei titoli delle massime più tipica del tema. "Quota nel tema" è la parte delle massime del tema che hanno quella voce; "volte la media" dice quanto la voce è più frequente nel tema che in tutte le massime.

| Tema | Massime | Parole che pesano di più | Voce dei titoli più tipica del tema (dal 2015): quota nel tema, volte la media |
| --- | --- | --- | --- |
| 0 | 2.391 | lavoro, trattamento, rapporto, lavoratori, pensione, servizio, dipendenti, diritto, indennita, lavoratore, retribuzione, previdenziale | previdenza: 19%, 16,8 volte la media |
| 1 | 4.964 | tutela, regionale, attività, principio, materia, nazionale, disciplina, amministrazione, servizio, esercizio, pubblico, pubblica | sanità pubblica: 14%, 4,8 volte la media |
| 2 | 381 | fattispecie, straniero, territorio, descrizione, cittadini, lgs, soggiorno, arresto, stranieri, italiana, rientro, ingresso | pronunce della corte costituzionale: 33%, 24,6 volte la media |
| 3 | 2.210 | legislatore, principio, trattamento, disciplina, scelta, discrezionalità, rispetto, scelte, situazioni, fattispecie, ragionevolezza, irragionevole | reati e pene: 21%, 5,8 volte la media |
| 4 | 3.369 | ricorso, conflitto, regione, consiglio, presidente, attribuzione, regionale, giudizio, ministri, confronti, atto, ricorrente | bilancio e contabilità pubblica: 12%, 1,8 volte la media |
| 5 | 1.187 | reg, aree, beni, piano, impianti, governo, edilizia, territorio, regionale, opere, interventi, illegittimo | edilizia e urbanistica: 36%, 9,8 volte la media |
| 6 | 2.673 | diritto, imposta, civ, legittimita, pagamento, cod, puo, tutela, principio, reddito, interessi, valore | tributi: 16%, 16,9 volte la media |
| 7 | 2.557 | gia, legittimita, manifesta, infondatezza, red, sanzione, sanzioni, sent, inammissibilita, penale, costituzionalmente, polizia | nessuna voce arriva al 10% delle massime del tema |
| 8 | 5.042 | giudizio, oggetto, rilevanza, motivazione, eccezione, via, principale, difetto, rimessione, incidentale, giudizi, inammissibili | prospettazione della questione incidentale: 12%, 3,0 volte la media |
| 9 | 4.441 | regioni, regione, competenza, materia, regionale, statuto, statale, competenze, speciale, province, provincia, legislativa | bilancio e contabilità pubblica: 13%, 2,0 volte la media |
| 10 | 2.813 | decreto, rilevanza, bis, convertito, atti, modificazioni, luglio, dicembre, conversione, manifesta, restituzione, legittimita | reati e pene: 14%, 3,7 volte la media |
| 11 | 621 | dichiarate, personale, fondate, sollevate, red, dipendenti, rev, legittimita, siciliana, economico, regionale, regione | nessuna voce arriva al 10% delle massime del tema |
| 12 | 462 | mass, precedenti, diritto, tutela, precedente, rispetto, diritti, contratto, costituzionalmente, legislatore, ordinamento, garanzia | nessuna voce arriva al 10% delle massime del tema |
| 13 | 1.604 | spese, spesa, risorse, fondo, periodo, pubblica, contributo, copertura, legislatore, bilancio, anno, oneri | bilancio e contabilità pubblica: 37%, 5,6 volte la media |
| 14 | 1.640 | pena, cod, misura, pen, sospensione, misure, reato, persona, precedenti, reati, sociale, rispetto | reati e pene: 26%, 7,2 volte la media |
| 15 | 1.249 | interpretazione, citate, europea, parametri, diritto, motivazione, parametro, unione, cedu, precedenti, plurimis, violazione | nessuna voce arriva al 10% delle massime del tema |
| 16 | 4.758 | cod, penale, proc, pen, processo, imputato, procedimento, giudizio, codice, diritto, pubblico, difesa | processo penale: 39%, 15,3 volte la media |
| 17 | 596 | camera, parlamentare, tribunale, deputati, poteri, esercizio, funzioni, espresse, opinioni, parlamento, parlamentari, evocati | giudizio costituzionale per conflitto di attribuzione tra poteri dello stato: 29%, 78,4 volte la media |
| 18 | 1.619 | regionale, regione, finanza, materia, enti, statale, siciliana, finanziaria, pubblica, bilancio, coordinamento, spesa | imposte e tasse: 24%, 11,2 volte la media |
| 19 | 1.549 | decreto, lgs, delega, testo, legislativo, vigore, disciplina, entrata, violazione, dicembre, materia, delegato | thema decidendum: 27%, 4,2 volte la media |
