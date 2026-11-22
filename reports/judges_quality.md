# Giudici: quanto bene sono stati riconosciuti

Prodotto da `src/judges/build_judges.py`. Per ogni pronuncia il programma cerca chi l'ha scritta (il redattore), chi l'ha seguita come relatore e chi sedeva nel collegio, e collega ogni nome all'elenco ufficiale dei giudici pubblicato dalla Corte.

## In breve

Questo file dice quanto bene il programma ha riconosciuto i giudici: chi ha scritto ciascuna pronuncia e chi sedeva nel collegio, collegando i nomi all'elenco ufficiale dei giudici. Le due soglie decise prima (98% per entrambe le cose) sono superate. Per le pronunce fino alla 286/1986 il nome di chi ha scritto non c'è: al suo posto si usa il relatore.

## Le misure principali

- Pronunce in cui il nome di chi ha scritto è stato collegato all'elenco dei giudici: **99,84%** (soglia decisa prima: 98%).
- Da dove viene il nome di chi ha scritto: dal campo dei dati in 8.384 pronunce; dalla firma in fondo al testo in 8.349; dal relatore, usato al suo posto fino alla 286/1986, in 5.678; in 16 non c'è.
- Pronunce con il collegio riconosciuto per intero, cioè con un numero di giudici tra 11 e 15, tutti collegati all'elenco e non meno dei nomi scritti nel testo: **98,85%** (soglia decisa prima: 98%). Senza il confronto con i nomi scritti nel testo: 99,79%.
  Le 257 pronunce con il collegio non riconosciuto per intero sono elencate in `data/interim/collegio_errors.csv`, con il motivo (meno di 11 giudici, più di 15, oppure meno giudici dei nomi scritti nel testo) e il testo del collegio, per il controllo a mano.
- Pronunce scritte da più giudici insieme: 19.
- Pronunce in cui il nome del relatore è stato collegato all'elenco: 99,95%.

## Per decennio

| Decennio | Chi ha scritto: nome collegato | Collegio riconosciuto per intero | Giudici per collegio, in media |
| --- | --- | --- | --- |
| anni 1950 | 100,0% | 96,2% | 13,73 |
| anni 1960 | 100,0% | 96,1% | 13,97 |
| anni 1970 | 100,0% | 95,0% | 14,04 |
| anni 1980 | 99,6% | 98,9% | 13,72 |
| anni 1990 | 99,9% | 99,9% | 13,48 |
| anni 2000 | 99,8% | 99,2% | 13,43 |
| anni 2010 | 99,9% | 100,0% | 13,59 |
| anni 2020 | 100,0% | 100,0% | 14,17 |

## Quanti giudici sono stati riconosciuti in ogni collegio

Il collegio decide con almeno 11 giudici (il numero legale): un numero più basso vuol dire che il programma non ha riconosciuto tutti i nomi.

| Giudici riconosciuti nel collegio | Pronunce |
| --- | --- |
| 0 | 1 |
| 9 | 1 |
| 10 | 45 |
| 11 | 1.112 |
| 12 | 2.733 |
| 13 | 5.085 |
| 14 | 6.822 |
| 15 | 6.628 |

## Giudici da controllare

Giudici che non compaiono in nessun collegio, o la cui ultima presenza in un collegio è più di 400 giorni prima della fine del mandato. Per i giudici ancora in carica è normale: il mandato non è finito. Quando l'elenco ufficiale non dà la fine del mandato, la data è calcolata come giuramento più 9 anni, la durata fissata dalla Costituzione (art. 135).

- Giuseppe Lampis: non compare in nessun collegio.
- Giuseppe Capograssi: non compare in nessun collegio.
- Nicola Reale: giuramento 18/07/1968; fine del mandato 02/08/1979 (dall'elenco ufficiale); ultima presenza in un collegio 04/07/1977.
- Giuseppe Frigo: giuramento 23/10/2008; fine del mandato 23/10/2017 (calcolata: giuramento più 9 anni); ultima presenza in un collegio 22/06/2016.
- Stefano Petitti: giuramento 10/12/2019; fine del mandato 10/12/2028 (calcolata: giuramento più 9 anni); ultima presenza in un collegio 02/11/2026.
- Angelo Buscema: giuramento 15/09/2020; fine del mandato 15/09/2029 (calcolata: giuramento più 9 anni); ultima presenza in un collegio 02/11/2026.
- Emanuela Navarretta: giuramento 15/09/2020; fine del mandato 15/09/2029 (calcolata: giuramento più 9 anni); ultima presenza in un collegio 02/11/2026.
- Maria Rosaria San Giorgio: giuramento 17/12/2020; fine del mandato 17/12/2029 (calcolata: giuramento più 9 anni); ultima presenza in un collegio 02/11/2026.
- Filippo Patroni Griffi: giuramento 29/01/2022; fine del mandato 29/01/2031 (calcolata: giuramento più 9 anni); ultima presenza in un collegio 02/11/2026.
- Marco D'Alberti: giuramento 20/09/2022; fine del mandato 20/09/2031 (calcolata: giuramento più 9 anni); ultima presenza in un collegio 21/10/2026.
- Giovanni Pitruzzella: giuramento 14/11/2023; fine del mandato 14/11/2032 (calcolata: giuramento più 9 anni); ultima presenza in un collegio 02/11/2026.
- Antonella Sciarrone Alibrandi: giuramento 14/11/2023; fine del mandato 14/11/2032 (calcolata: giuramento più 9 anni); ultima presenza in un collegio 02/11/2026.
- Massimo Luciani: giuramento 18/02/2025; fine del mandato 18/02/2034 (calcolata: giuramento più 9 anni); ultima presenza in un collegio 02/11/2026.
- Maria Alessandra Sandulli: giuramento 18/02/2025; fine del mandato 18/02/2034 (calcolata: giuramento più 9 anni); ultima presenza in un collegio 02/11/2026.
- Roberto Nicola Cassinelli: giuramento 18/02/2025; fine del mandato 18/02/2034 (calcolata: giuramento più 9 anni); ultima presenza in un collegio 02/11/2026.
- Francesco Saverio Marini: giuramento 18/02/2025; fine del mandato 18/02/2034 (calcolata: giuramento più 9 anni); ultima presenza in un collegio 02/11/2026.
