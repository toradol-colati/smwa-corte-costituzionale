# Primo controllo dei file scaricati

Prodotto da `src/ingest/inspect_raw.py` sui file elencati in `data/raw/MANIFEST.csv`, prima di qualsiasi analisi. Descrive com'è fatto ogni file, quanto è completo anno per anno e se i dati sono coerenti tra loro; non corregge nulla. Che cosa contiene ogni campo dei file (le etichette XML, scritte `così`) è spiegato in `docs/data_schema.md`; il suo significato giuridico in `docs/context.md`.

## In breve

Questo file è il primo controllo fatto sui file scaricati dal portale, prima di qualsiasi analisi. Le cose più importanti che ne sono uscite: la numerazione delle pronunce non ha buchi né doppioni, quindi anno e numero identificano ogni pronuncia; il nome di chi ha scritto la pronuncia c'è solo dal dicembre 1986; nelle ordinanze il ragionamento della Corte sta in un posto diverso che nelle sentenze; l'elenco ufficiale dei giudici ha date mancanti o sbagliate, da completare a mano.

## Quale versione dei dati

Per ogni file scaricato: quando è stato scaricato e la sua impronta, un codice che cambia se cambia anche un solo carattere del file.

| File | Scaricato il (ora UTC) | Impronta (SHA-256) |
| --- | --- | --- |
| data/raw/pronunce/CC_OpenPronunce_1956_1980.zip | 2026-11-08T16:31:49+00:00 | 82cd2b739b5fb90fe103a3cdafb0be55c4c03b7044e816774b325964d72d4294 |
| data/raw/pronunce/CC_OpenPronunce_1981_2000.zip | 2026-11-08T16:31:57+00:00 | 41565cd8962e0cae9591a47933f4d80017c3aa1856093d5bba4b6d558d309472 |
| data/raw/pronunce/CC_OpenPronunce_2001_oggi.zip | 2026-11-08T16:32:07+00:00 | 86d39bd5ce7dd666e03e80a050327d0e3a7a5634a6b26a757624d0b075c45d58 |
| data/raw/massime/CC_OpenMassime_1956_1980.zip | 2026-11-08T16:32:08+00:00 | 62065d13269cba9f73ae552ad1f3f57b21795dbb8b67e09e82bed88fce449b57 |
| data/raw/massime/CC_OpenMassime_1981_2000.zip | 2026-11-08T16:32:10+00:00 | f17ce7551f6cfe6f756d415e3ea6e3af62cd0ee269558ffbedc6003284e65e8f |
| data/raw/massime/CC_OpenMassime_2001_oggi.zip | 2026-11-08T16:32:12+00:00 | b57aceb78827c1df4ea7651ed54335d53610385e9a6b49351d01577051b495be |
| data/raw/giudici/Cc_Opendata_AnagraficaGiudici.zip | 2026-11-08T16:32:13+00:00 | 071f0e6ea9db135bd6bcfa0dbac481c15d4b7eba293ea14ffa79ce2c748513ac |

## Le pronunce: numeri e date

- Pronunce: **22.427**, dal 1956 al 2026: 11.735 sentenze e 10.692 ordinanze (altri tipi: 0).
- Pronunce con lo stesso anno e lo stesso numero: 0. Anni con numeri mancanti: 0. Quindi ogni anno la numerazione riparte da 1 ed è unica per sentenze e ordinanze: anno e numero bastano a identificare una pronuncia.
- Pronunce con un codice europeo (ECLI) diverso da `ECLI:IT:COST:anno:numero`: 0.
- L'anno della pronuncia è quello del deposito, tranne in 1 caso (un errore di data: la 69/1982, depositata il 03/04/1980 secondo i dati). Coincide con l'anno della decisione nel 99,02% dei casi: 220 pronunce sono state decise in un anno e depositate, e quindi numerate, nell'anno dopo.
- Pronunce con un numero più alto della precedente ma una data più vecchia: 22 guardando la data di deposito, 1.134 guardando quella della decisione. Quindi il numero segue l'ordine del deposito, non quello della decisione.
- La rete arriva a 1.000 pronunce nel 1966 (a fine anno sono 1.121). Dal 1966 l'anno con meno pronunce depositate è il 1978, con 87; l'anno in corso (2026, non ancora finito) ne ha 191.
- Giorni tra la decisione e il deposito: 9 a metà della distribuzione (mediana); il 99% delle pronunce entro 72. Date di decisione mancanti: 3. Pronunce depositate prima della data di decisione, quindi con una data sbagliata: 17.

## Le pronunce: presidente, relatore e chi ha scritto

Quota di pronunce, per decennio, in cui il campo è vuoto (1 = sempre vuoto, 0 = mai). Il relatore è il giudice che segue la causa; il redattore è chi scrive la pronuncia (campo `redattore_pronuncia`).

| Decennio | Presidente vuoto | Relatore vuoto | Redattore vuoto |
| --- | --- | --- | --- |
| 1950 | 0 | 0 | 1 |
| 1960 | 0 | 0 | 1 |
| 1970 | 0 | 0 | 1 |
| 1980 | 0 | 0,001 | 0,997 |
| 1990 | 0 | 0 | 0,996 |
| 2000 | 0 | 0,001 | 0,207 |
| 2010 | 0 | 0,001 | 0,001 |
| 2020 | 0 | 0 | 0 |

Il campo del redattore negli anni in cui comincia a essere compilato (quota di pronunce con il campo vuoto): 1999: 100%; 2000: 99%; 2001: 81%; 2002: 0%; 2003: 0%; 2004: 0%.

**Le firme in fondo alla pronuncia**

- Fino alla 286/1986 firmano tutti i giudici del collegio, e chi ha scritto la pronuncia non è indicato da nessuna parte. Pronunce di quel periodo che nominano un redattore nelle firme: 0.
- Dalla 287/1986 (decisa il 19/12/1986, depositata il 23/12/1986) firmano il Presidente e chi ha scritto la pronuncia ("Il redattore: …", poi "…, Redattore" o "Redattrice"). Pronunce successive senza il redattore nelle firme: 251, per lo più ordinanze lette in udienza e firmate dal solo Presidente.
- Pronunce con entrambi i campi compilati: 8.384. In 93 il relatore è diverso da chi ha scritto (per decennio: anni 1980: 12; anni 1990: 19; anni 2000: 30; anni 2010: 21; anni 2020: 11).
- Pronunce scritte da più giudici (nomi separati da " - "): 17, dal 2016 al 2026.
- Valori diversi di ogni campo: relatore 131, redattore 76, presidente 84 (il presidente è scritto con il solo cognome).

## Le pronunce: il collegio

Numero di giudici scritti nel campo `collegio`, contati in modo approssimato (il conteggio vero è fatto dopo, in `src/judges/`). I collegi con 10 giudici o meno, o con più di 15, sono da controllare.

| Decennio | 10 o meno (da controllare) | 11–12 | 13–15 | più di 15 (da controllare) |
| --- | --- | --- | --- | --- |
| 1950 | 1 | 23 | 291 | 0 |
| 1960 | 1 | 169 | 1099 | 2 |
| 1970 | 1 | 122 | 1941 | 1 |
| 1980 | 12 | 896 | 3554 | 0 |
| 1990 | 21 | 958 | 4031 | 0 |
| 2000 | 5 | 1051 | 3546 | 1 |
| 2010 | 0 | 628 | 2408 | 0 |
| 2020 | 0 | 104 | 1561 | 0 |

- Collegi con 11 o 12 giudici: 3.951 (17,6%). Sono validi, perché il numero legale è 11 (legge 87/1953, art. 16): una soglia di 13–15 giudici li scarterebbe.
- Collegi con nomi in cui ci sono cifre al posto delle lettere (errori di trascrizione, per esempio "PERASS1", "MAR10"): 6; per decennio: anni 1950: 2; anni 1960: 2; anni 1970: 2.

## Le pronunce: come è diviso il testo

- Nelle sentenze il campo `<testo>` contiene due etichette, `<fatto>` e `<diritto>`, che racchiudono solo il titolo della parte ("Ritenuto in fatto", "Considerato in diritto"): il testo della parte viene dopo l'etichetta, non dentro.
- Sentenze con entrambe le etichette: 11.693 su 11.735; ordinanze con le etichette: 0.
Lunghezza di ogni parte a metà della distribuzione (mediana, in caratteri), per tipo di pronuncia (O = ordinanza, S = sentenza) e decennio:

| Tipo | Decennio | epigrafe | testo | dispositivo |
| --- | --- | --- | --- | --- |
| O | 1950 | 2430 | 0 | 1154 |
| O | 1960 | 2654 | 0 | 1155 |
| O | 1970 | 2507 | 0 | 1326 |
| O | 1980 | 3469 | 0 | 1169 |
| O | 1990 | 5100 | 0 | 1090 |
| O | 2000 | 7952 | 0 | 835 |
| O | 2010 | 4851 | 0 | 774 |
| O | 2020 | 9590 | 0 | 669 |
| S | 1950 | 1018 | 17162 | 1454 |
| S | 1960 | 1053 | 13529 | 1323 |
| S | 1970 | 1044 | 10677 | 1402 |
| S | 1980 | 1116 | 14197 | 1326 |
| S | 1990 | 1045 | 15139 | 1166 |
| S | 2000 | 888 | 20038 | 1004 |
| S | 2010 | 892 | 28351 | 1047 |
| S | 2020 | 1002 | 38963 | 1093 |

- Nelle ordinanze `<testo>` è vuoto nel 95,6% dei casi: il ragionamento ("Ritenuto che…", "Considerato che…") sta dentro `<epigrafe>`. La formula "Considerato che" compare nell'epigrafe del 50% delle ordinanze (per decennio: anni 1950: 39%; anni 1960: 52%; anni 1970: 50%; anni 1980: 26%; anni 1990: 39%; anni 2000: 71%; anni 2010: 60%; anni 2020: 97%): le altre usano formule diverse, da elencare prima di scrivere il programma che legge i testi.
- Il dispositivo comincia con "per questi motivi" nel 99,9% delle pronunce e finisce con le firme e la data di deposito.

## Le massime

- Pronunce nell'archivio delle massime: 22.427, le stesse dell'archivio delle pronunce (mancanti: 0; con un tipo diverso: 0). Massime: 46.658; di solito una per pronuncia (mediana 1), al massimo 59.
Quota di pronunce con almeno una massima (1 = tutte), per decennio e tipo:

| Decennio | Ordinanze | Sentenze |
| --- | --- | --- |
| 1950 | 1 | 1 |
| 1960 | 1 | 1 |
| 1970 | 1 | 1 |
| 1980 | 1 | 1 |
| 1990 | 1 | 1 |
| 2000 | 1 | 1 |
| 2010 | 1 | 1 |
| 2020 | 0,956 | 0,971 |

Gli ultimi anni: 2023: 100%; 2024: 100%; 2025: 100%; 2026: 73%. Le massime vengono scritte qualche mese dopo la pronuncia.

Il tipo di giudizio (campo `tipologia_giudizio`) sta solo nell'archivio delle massime, ma c'è per tutte le pronunce:

| Tipo di giudizio | Pronunce |
| --- | --- |
| GIUDIZIO DI LEGITTIMITÀ COSTITUZIONALE IN VIA INCIDENTALE | 17052 |
| GIUDIZIO DI LEGITTIMITÀ COSTITUZIONALE IN VIA PRINCIPALE | 3234 |
| GIUDIZIO PER CONFLITTO DI ATTRIBUZIONE TRA ENTI | 1026 |
| GIUDIZIO SULL'AMMISSIBILITÀ DI RICORSO PER CONFLITTO DI ATTRIBUZIONE TRA POTERI DELLO STATO | 480 |
| GIUDIZIO PER CONFLITTO DI ATTRIBUZIONE TRA POTERI DELLO STATO | 305 |
| GIUDIZIO SULL'AMMISSIBILITÀ DEI REFERENDUM | 153 |
| GIUDIZIO PER LA CORREZIONE DI OMISSIONI E/O ERRORI MATERIALI | 140 |
| GIUDIZIO SU CONFLITTO DI ATTRIBUZIONE TRA ENTI + GIUDIZIO DI LEGITTIMITA' COSTITUZIONALE IN VIA PRINCIPALE | 17 |
| (vuoto) | 8 |
| GIUDIZIO DI LEGITTIMITÀ COSTITUZIONALE IN VIA PRINCIPALE + GIUDIZIO DI LEGITTIMITÀ COSTITUZIONALE IN VIA INCIDENTALE | 4 |
| GIUDIZIO PER LA SOSPENSIONE DELL'ATTO IMPUGNATO | 3 |
| GIUDIZIO DI ACCUSA | 3 |
| GIUDIZIO SU CONFLITTO DI ATTRIBUZIONE TRA ENTI  + GIUDIZIO DI LEGITTIMITA' COSTITUZIONALE  IN VIA INCIDENTALE | 2 |

- Il titolo di ogni massima è fatto di voci separate da " - "; la prima di solito è la materia. Titoli nel formato vecchio, tutto in maiuscolo e con davanti un'abbreviazione come "SENT. n/aa": 56% (l'ultimo anno in cui compaiono: 2014). Prime voci diverse: 5.363: prima di usarle come materia vanno ricondotte a un elenco più corto.
- Massime con i parametri, cioè le norme della Costituzione (o di leggi costituzionali) che si dicono violate: 86,3%; con le leggi impugnate: 85,6%. Parametri e leggi hanno un campo `codice` che i documenti ufficiali sulla struttura dei file non descrivono.
- Pronunce con massime che hanno prime voci diverse tra loro: 25,2%.

## L'elenco dei giudici

- Righe: 136; giudici: 125. Le altre 11 righe hanno più nomi insieme ("Lattanzi - Cartabia"): corrispondono alle pronunce scritte da più giudici, non a persone.
- Chi ha eletto o nominato il giudice (campo `Eletto_da`): Presidente della Repubblica: 43; Parlamento: 41; Corte di Cassazione: 23; Corte dei Conti: 9; Consiglio di Stato: 8; Corte dei conti: 1. "Corte dei Conti" e "Corte dei conti" sono la stessa cosa scritta in due modi.
- Fine del mandato (`data_cessazione`) mancante: 33 giudici, molti dei quali hanno chiaramente finito il mandato (tabella qui sotto). Va completata prima di usarla: come, è scritto in `docs/decisions.md`.
- Mandati di più di 12 anni, quindi date sbagliate: Ugo Spagnoli (25/02/1986–25/02/2005).
- Giudici che hanno giurato prima della legge costituzionale 2/1967, che riguarda la durata del mandato: 26; durata mediana del loro mandato 11,8 anni (per quelli venuti dopo: 9,0).
- Giudici con lo stesso cognome di un altro: Aldo Sandulli, Nicola Reale, Oronzo Reale, Ettore Gallo, Annibale Marini, Franco Gallo, Maria Alessandra Sandulli, Francesco Saverio Marini. Per collegare i nomi all'elenco non basta il cognome.
- Note biografiche vuote: 4; lunghezza mediana 248 caratteri. Dicono la professione del giudice al momento dell'elezione (serve per D4).

Giudici senza la data di fine del mandato, con l'ultima decisione in cui il loro cognome compare nel collegio (è una stima: i cognomi condivisi possono confondere):

| Giudice | Giuramento | Ultimo collegio (stima) |
| --- | --- | --- |
| Luigi Mazzella | 28/06/2005 | 11/06/2014 |
| Sabino Cassese | 09/11/2005 | 22/10/2014 |
| Giuseppe Tesauro | 09/11/2005 | 03/11/2014 |
| Paolo Maria Napolitano | 10/07/2006 | 23/06/2015 |
| Giuseppe Frigo | 23/10/2008 | 21/06/2016 |
| Paolo Grossi | 23/02/2009 | 06/12/2017 |
| Giorgio Lattanzi | 09/12/2010 | 04/11/2019 |
| Aldo Carosi | 13/09/2011 | 12/08/2020 |
| Marta Cartabia | 13/09/2011 | 12/08/2020 |
| Mario Rosario Morelli | 12/12/2011 | 21/10/2020 |
| Giancarlo Coraggio | 28/01/2013 | 29/11/2021 |
| Giuliano Amato | 18/09/2013 | 06/07/2022 |
| Daria de Pretis | 11/11/2014 | 19/09/2023 |
| Nicolò Zanon | 11/11/2014 | 19/09/2023 |
| Silvana Sciarra | 11/11/2014 | 19/09/2023 |
| Franco Modugno | 21/12/2015 | 17/06/2024 |
| Augusto Antonio Barbera | 21/12/2015 | 14/11/2024 |
| Giulio Prosperetti | 21/12/2015 | 14/11/2024 |
| Giovanni Amoroso | 13/11/2017 | 05/10/2026 |
| Francesco Viganò | 08/03/2018 | 05/10/2026 |
| Luca Antonini | 26/07/2018 | 05/10/2026 |
| Stefano Petitti | 10/12/2019 | 05/10/2026 |
| Angelo Buscema | 15/09/2020 | 05/10/2026 |
| Emanuela Navarretta | 15/09/2020 | 05/10/2026 |
| Maria Rosaria San Giorgio | 17/12/2020 | 05/10/2026 |
| Filippo Patroni Griffi | 29/01/2022 | 05/10/2026 |
| Marco D'Alberti | 20/09/2022 | 05/10/2026 |
| Giovanni Pitruzzella | 14/11/2023 | 05/10/2026 |
| Antonella Sciarrone Alibrandi | 14/11/2023 | 05/10/2026 |
| Massimo Luciani | 18/02/2025 | 05/10/2026 |
| Maria Alessandra Sandulli | 18/02/2025 | 05/10/2026 |
| Roberto Nicola Cassinelli | 18/02/2025 | 05/10/2026 |
| Francesco Saverio Marini | 18/02/2025 | 05/10/2026 |

## Una prima ricerca grezza delle citazioni (non controllata)

Serve solo per orientarsi, non per le analisi. Cerca le citazioni scritte come "sentenza n. X del AAAA" e ne prende il primo numero, nel testo delle sentenze (compreso il «Ritenuto in fatto») e nell'epigrafe delle ordinanze.

- Citazioni trovate: 86.172; verso pronunce che non esistono: 1,9%.
- Verso pronunce depositate prima: 84.386; lo stesso giorno: 145; dopo: 20.
- Pronunce che contengono le parole "in pari data": 328. Quindi le citazioni tra pronunce depositate lo stesso giorno esistono davvero: non sono errori del programma.
