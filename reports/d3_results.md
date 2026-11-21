# D3: un giudice cita di più le pronunce decise in collegi in cui sedeva?

Prodotto da `src/analysis/d3_memoria_collegiale.py`, con i numeri salvati in `reports/d3_results.json`.

## In breve

Questo file contiene i numeri di D3, il risultato principale del lavoro: un giudice cita di più i precedenti decisi da collegi in cui sedeva, rispetto a quelli decisi mentre era in carica ma assente? La risposta è no: il numero che lo misura (l'odds ratio) vale 1, cioè nessuna differenza, e resta vicino a 1 in tutte le prove. Il giudice cita molto di più, invece, le pronunce che ha scritto lui. Le tabelle spiegano riga per riga che cosa è stato provato; la lettura completa è nella relazione, sezione 3.4.

## Che cosa misura la tabella principale

Per ogni pronuncia che cita, il programma mette a confronto i precedenti che cita con un campione di precedenti che avrebbe potuto citare e non ha citato. Guarda solo i precedenti decisi mentre il giudice che scrive la pronuncia era già alla Corte. Tra questi distingue due gruppi:

- i precedenti decisi da un collegio in cui il giudice sedeva, senza averli scritti lui;
- i precedenti decisi mentre il giudice era in carica, ma assente da quel collegio.

La colonna "Odds ratio" dice quanto è più probabile, in termini di odds, che il giudice citi un precedente del primo gruppo invece che del secondo, a parità di età del precedente, di materia e del fatto di averlo scritto lui. 1 vuol dire nessuna differenza; sopra 1 cita di più i precedenti decisi con lui presente; sotto 1, di meno. L'intervallo al 95% raccoglie i valori compatibili con i dati. Il valore p dice quanto sarebbe raro un risultato così lontano da 1 se la differenza non ci fosse. L'incertezza tiene conto che le pronunce scritte dallo stesso giudice si somigliano (errori standard raggruppati per chi scrive).

La prima riga è il risultato principale, deciso prima di vedere i dati. Le altre ripetono il calcolo cambiando una cosa alla volta, per vedere se il risultato regge.

| Prova | Pronunce che citano | Citazioni | Di cui a precedenti decisi con il giudice assente | Odds ratio | Intervallo al 95% | Valore p |
| --- | --- | --- | --- | --- | --- | --- |
| **Risultato principale** | 13.654 | 46.969 | 1.658 | 1,00 | 0,92–1,09 | 0,997 |
| con due controlli in più: tipo del precedente e citazioni già ricevute | 13.654 | 46.969 | 1.658 | 1,00 | 0,92–1,09 | 0,968 |
| senza i precedenti scritti dallo stesso giudice | 13.654 | 32.325 | 1.639 | 0,99 | 0,91–1,08 | 0,870 |
| solo pronunce dalla 287/1986 (il nome di chi scrive è nei dati) | 11.076 | 41.320 | 1.430 | 1,01 | 0,93–1,10 | 0,801 |
| solo pronunce che citano fino alla 286/1986 (al posto di chi scrive, il relatore) | 2.565 | 4.895 | 167 | 1,01 | 0,77–1,33 | 0,939 |
| senza gli anni dell'arretrato (tolte le pronunce che citano del 1987–1989) | 12.542 | 44.949 | 1.549 | 1,04 | 0,96–1,13 | 0,333 |
| senza le ordinanze che correggono errori materiali | 13.574 | 46.875 | 1.658 | 1,00 | 0,92–1,09 | 0,987 |
| solo sentenze che citano | 7.370 | 32.001 | 1.150 | 1,05 | 0,96–1,14 | 0,283 |
| solo ordinanze che citano | 6.284 | 14.968 | 508 | 0,91 | 0,78–1,05 | 0,205 |
| solo pronunce che citano fino al 2000 | 7.179 | 15.971 | 597 | 0,92 | 0,78–1,08 | 0,288 |
| solo pronunce che citano dal 2001 | 6.475 | 30.998 | 1.061 | 1,03 | 0,95–1,13 | 0,484 |
| solo giudizi in via incidentale | 10.079 | 29.470 | 982 | 1,01 | 0,91–1,12 | 0,858 |
| citazioni da tutto il testo (anche dal «Ritenuto in fatto») | 14.406 | 52.453 | 1.899 | 0,99 | 0,90–1,09 | 0,860 |
| con anche le citazioni delle note editoriali alle massime | 13.844 | 48.212 | 1.702 | 0,99 | 0,91–1,08 | 0,791 |
| con un controllo per la stessa legge impugnata (prova esplorativa) | 13.654 | 46.969 | 1.658 | 0,99 | 0,91–1,07 | 0,804 |
| materia più fine, dagli articoli della Costituzione invocati (prova esplorativa) | 13.654 | 46.969 | 1.658 | 0,99 | 0,91–1,08 | 0,788 |

## Tutti i numeri del modello principale

Ogni riga confronta i precedenti con quella caratteristica con quelli senza. Per le classi di età il confronto è con i precedenti di meno di un anno. Per la somiglianza di materia il confronto è tra i due estremi, 0 (nessun tema in comune) e 1 (gli stessi temi nelle stesse proporzioni): per questo il numero è così grande.

| Caratteristica del precedente | Odds ratio | Intervallo al 95% | Valore p |
| --- | --- | --- | --- |
| il precedente l'ha scritto lo stesso giudice (`self_drafted`) | 5,466 | 4,765–6,271 | < 0,001 |
| il giudice sedeva nel collegio del precedente, senza scriverlo (`sat_not_drafted`) | 1,000 | 0,918–1,089 | 0,997 |
| somiglianza di materia tra le due pronunce, da 0 a 1 (`topic_similarity`) | 168,424 | 139,623–203,165 | < 0,001 |
| il precedente ha tra 1 e 2 anni | 0,750 | 0,701–0,801 | < 0,001 |
| il precedente ha tra 2 e 3 anni | 0,548 | 0,501–0,599 | < 0,001 |
| il precedente ha tra 3 e 4 anni | 0,420 | 0,380–0,465 | < 0,001 |
| il precedente ha tra 4 e 5 anni | 0,354 | 0,316–0,396 | < 0,001 |
| il precedente ha tra 5 e 7 anni | 0,289 | 0,257–0,325 | < 0,001 |
| il precedente ha tra 7 e 10 anni | 0,258 | 0,217–0,308 | < 0,001 |
| il precedente ha tra 10 e 15 anni | 0,279 | 0,154–0,505 | < 0,001 |

Lo stesso calcolo, ripetuto con altri 5 campioni casuali di precedenti non citati, dà questi odds ratio per `sat_not_drafted`: 0,994; 1,009; 0,986; 0,983; 0,989.

Giudici che scrivono (i gruppi usati per l'incertezza): 122. Righe del confronto: 728.876.

## Il modello completo (secondario)

Qui entrano tutti i precedenti, anche quelli decisi prima che il giudice arrivasse alla Corte, e il confronto è con questi ultimi. Il risultato non dice solo se il giudice sedeva nel collegio, ma anche quanto il precedente è vicino nel tempo: per questo è secondario. Il controllo su questo modello è in `reports/d3_full_check.json` e nella relazione, sezione 3.4.

| Caratteristica del precedente | Odds ratio | Intervallo al 95% | Valore p |
| --- | --- | --- | --- |
| il precedente l'ha scritto lo stesso giudice (`self_drafted`) | 7,239 | 6,231–8,410 | < 0,001 |
| il giudice sedeva nel collegio del precedente, senza scriverlo (`sat_not_drafted`) | 0,875 | 0,801–0,957 | 0,003 |
| il precedente è stato deciso mentre il giudice era in carica, ma assente (`in_mandate_absent`) | 0,885 | 0,771–1,015 | 0,080 |
| somiglianza di materia tra le due pronunce, da 0 a 1 (`topic_similarity`) | 280,549 | 239,856–328,146 | < 0,001 |
| il precedente ha tra 1 e 2 anni | 0,685 | 0,631–0,744 | < 0,001 |
| il precedente ha tra 2 e 3 anni | 0,507 | 0,458–0,562 | < 0,001 |
| il precedente ha tra 3 e 4 anni | 0,390 | 0,348–0,438 | < 0,001 |
| il precedente ha tra 4 e 5 anni | 0,330 | 0,295–0,371 | < 0,001 |
| il precedente ha tra 5 e 7 anni | 0,257 | 0,228–0,289 | < 0,001 |
| il precedente ha tra 7 e 10 anni | 0,174 | 0,152–0,198 | < 0,001 |
| il precedente ha tra 10 e 15 anni | 0,108 | 0,093–0,126 | < 0,001 |
| il precedente ha tra 15 e 20 anni | 0,073 | 0,061–0,086 | < 0,001 |
| il precedente ha tra 20 e 30 anni | 0,048 | 0,039–0,058 | < 0,001 |
| il precedente ha 30 anni o più | 0,025 | 0,021–0,030 | < 0,001 |
