# Ispezione dei dati grezzi

Generato da `src/ingest/inspect_raw.py` sui file elencati in `data/raw/MANIFEST.csv`. Solo controlli descrittivi: struttura, copertura, coerenza. Non modificare a mano.

## Versione dei dati

| file | downloaded_at | sha256 |
| --- | --- | --- |
| data/raw/pronunce/CC_OpenPronunce_1956_1980.zip | 2026-11-08T16:31:49+00:00 | 82cd2b739b5fb90fe103a3cdafb0be55c4c03b7044e816774b325964d72d4294 |
| data/raw/pronunce/CC_OpenPronunce_1981_2000.zip | 2026-11-08T16:31:57+00:00 | 41565cd8962e0cae9591a47933f4d80017c3aa1856093d5bba4b6d558d309472 |
| data/raw/pronunce/CC_OpenPronunce_2001_oggi.zip | 2026-11-08T16:32:07+00:00 | 86d39bd5ce7dd666e03e80a050327d0e3a7a5634a6b26a757624d0b075c45d58 |
| data/raw/massime/CC_OpenMassime_1956_1980.zip | 2026-11-08T16:32:08+00:00 | 62065d13269cba9f73ae552ad1f3f57b21795dbb8b67e09e82bed88fce449b57 |
| data/raw/massime/CC_OpenMassime_1981_2000.zip | 2026-11-08T16:32:10+00:00 | f17ce7551f6cfe6f756d415e3ea6e3af62cd0ee269558ffbedc6003284e65e8f |
| data/raw/massime/CC_OpenMassime_2001_oggi.zip | 2026-11-08T16:32:12+00:00 | b57aceb78827c1df4ea7651ed54335d53610385e9a6b49351d01577051b495be |
| data/raw/giudici/Cc_Opendata_AnagraficaGiudici.zip | 2026-11-08T16:32:13+00:00 | 071f0e6ea9db135bd6bcfa0dbac481c15d4b7eba293ea14ffa79ce2c748513ac |

## Pronunce: identificativi e numerazione

- Pronunce: **22,427** (1956–2026); sentenze (S) 11,735, ordinanze (O) 10,692; altri tipi: 0.
- Coppie anno + numero duplicate: 0. Anni con buchi nella numerazione: 0. La numerazione è annuale e unica per sentenze e ordinanze.
- ECLI diverso da `ECLI:IT:COST:anno:numero`: 0.
- L'anno della pronuncia coincide con l'anno del deposito in tutti i casi tranne 1 (errori di data: 69/1982 depositata il 03/04/1980); con l'anno della decisione nel 99.02% dei casi. Pronunce decise in un anno e depositate (e numerate) nell'anno dopo: 220.
- Coppie consecutive in cui il numero cresce ma la data scende: rispetto al deposito 22, rispetto alla decisione 1134. Il numero segue l'ordine del deposito.
- La rete raggiunge 1.000 pronunce nel 1966 (cumulate a fine anno: 1,121). Dal 1966 il numero minimo di pronunce depositate in un anno è 87 (1978); l'anno in corso (2026, incompleto) ne conta 191.
- Giorni tra decisione e deposito: mediana 9, 99° percentile 72; date di decisione mancanti 3; deposito prima della decisione (errori di data) 17.

## Pronunce: presidente, relatore, redattore

Quota di campi vuoti per decennio:

| decade | presidente vuoto | relatore vuoto | redattore vuoto |
| --- | --- | --- | --- |
| 1950 | 0 | 0 | 1 |
| 1960 | 0 | 0 | 1 |
| 1970 | 0 | 0 | 1 |
| 1980 | 0 | 0.001 | 0.997 |
| 1990 | 0 | 0 | 0.996 |
| 2000 | 0 | 0.001 | 0.207 |
| 2010 | 0 | 0.001 | 0.001 |
| 2020 | 0 | 0 | 0 |

Campo `redattore_pronuncia` vuoto, anni di passaggio: 1999: 100%, 2000: 99%, 2001: 81%, 2002: 0%, 2003: 0%, 2004: 0%.

Firme in fondo al dispositivo:

- Fino a 286/1986 la pronuncia è firmata da tutti i giudici del collegio; il redattore non è indicato in nessun punto. Pronunce di quel periodo che nominano un redattore nelle firme: 0.
- Da 287/1986 (decisa il 19/12/1986, depositata il 23/12/1986) firmano il Presidente e il redattore ("Il redattore: …", poi "…, Redattore" o "Redattrice"). Pronunce successive senza redattore nelle firme: 251, per lo più ordinanze lette in udienza e firmate dal solo Presidente.
- Con entrambi i campi compilati (8,384 pronunce), relatore diverso dal redattore: 93 (per decennio: {1980: 12, 1990: 19, 2000: 30, 2010: 21, 2020: 11}).
- Pronunce con più redattori (nomi separati da " - "): 17, dal 2016 al 2026.
- Stringhe distinte: relatore 131, redattore 76, presidente 84 (il presidente è indicato col solo cognome).

## Pronunce: collegio

Numero di giudici nell'elemento `collegio`, stima con un'euristica (da rifare in `src/judges/`):

| decade | ≤10 (da controllare) | 11–12 | 13–15 | >15 (da controllare) |
| --- | --- | --- | --- | --- |
| 1950 | 1 | 23 | 291 | 0 |
| 1960 | 1 | 169 | 1099 | 2 |
| 1970 | 1 | 122 | 1941 | 1 |
| 1980 | 12 | 896 | 3554 | 0 |
| 1990 | 21 | 958 | 4031 | 0 |
| 2000 | 5 | 1051 | 3546 | 1 |
| 2010 | 0 | 628 | 2408 | 0 |
| 2020 | 0 | 104 | 1561 | 0 |

- Collegi con 11 o 12 giudici: 3,951 (17.6%). Sono validi: il numero legale è 11 (art. 16, legge 87/1953). Una soglia 13–15 li scarterebbe.
- Nomi con cifre al posto di lettere (errori di trascrizione, es. "PERASS1", "MAR10"): 6 collegi, per decennio {1950: 2, 1960: 2, 1970: 2}.

## Pronunce: struttura del testo

- Nelle sentenze, `<testo>` contiene il testo con due marcatori di intestazione, `<fatto>` e `<diritto>`, che racchiudono solo il titolo ("Ritenuto in fatto", "Considerato in diritto"): il testo della sezione segue il marcatore, fuori dal tag.
- Sentenze con entrambi i marcatori: 11,693 su 11,735; ordinanze con i marcatori: 0.
Lunghezza mediana (caratteri) degli elementi, per tipo e decennio:

| tipologia_pronuncia | decade | epigrafe | testo | dispositivo |
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

- Nelle ordinanze `<testo>` è vuoto nel 95.6% dei casi: la motivazione ("Ritenuto che…", "Considerato che…") sta dentro `<epigrafe>`. "Considerato che" compare nell'epigrafe del 50% delle ordinanze (per decennio {1950: 0.39, 1960: 0.52, 1970: 0.5, 1980: 0.26, 1990: 0.39, 2000: 0.71, 2010: 0.6, 2020: 0.97}): le altre usano formule diverse, da censire.
- Il dispositivo comincia con "per questi motivi" nel 99.9% delle pronunce e finisce con le firme e la data di deposito.

## Massime

- Pronunce nell'archivio delle massime: 22,427, le stesse dell'archivio delle pronunce (mancanti: 0; tipo diverso: 0). Massime: 46,658; per pronuncia mediana 1, massimo 59.
Quota di pronunce con almeno una massima:

| decade | O | S |
| --- | --- | --- |
| 1950 | 1 | 1 |
| 1960 | 1 | 1 |
| 1970 | 1 | 1 |
| 1980 | 1 | 1 |
| 1990 | 1 | 1 |
| 2000 | 1 | 1 |
| 2010 | 1 | 1 |
| 2020 | 0.956 | 0.971 |

Anni recenti: 2023: 100%, 2024: 100%, 2025: 100%, 2026: 73%. Le massime arrivano dopo la pronuncia.

Tipo di giudizio (`tipologia_giudizio`, presente solo nelle massime ma per tutte le pronunce):

| tipologia_giudizio | pronunce |
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

- Titolo della massima: voci separate da " - "; la prima è di solito la materia. Titoli nel formato vecchio, tutto maiuscolo e con prefisso "SENT. n/aa": 56% (ultimo anno: 2014). Prime voci distinte: 5,363: la materia va normalizzata prima dell'uso.
- Massime con parametri costituzionali: 86.3%; con norme impugnate: 85.6%. Parametri e norme hanno un campo `codice` non descritto nel DTD.
- Pronunce con massime su più prime voci diverse: 25.2%.

## Anagrafica dei giudici

- Righe: 136; giudici: 125; righe composte da più nomi ("Lattanzi - Cartabia"), che corrispondono alle pronunce con più redattori: 11.
- Organo di elezione o nomina (`Eletto_da`): Presidente della Repubblica: 43, Parlamento: 41, Corte di Cassazione: 23, Corte dei Conti: 9, Consiglio di Stato: 8, Corte dei conti: 1. La grafia di "Corte dei conti" va uniformata.
- `data_cessazione` vuota: 33 giudici, molti dei quali hanno chiaramente cessato dalla carica (vedi tabella sotto). Va completata in `data/manual/` con la fonte.
- Mandati più lunghi di 12 anni (errori di data): Ugo Spagnoli (25/02/1986–25/02/2005).
- Giudici che hanno giurato prima della legge cost. 2/1967: 26; durata mediana del mandato 11.8 anni (dopo: 9.0).
- Cognomi condivisi da più giudici: Aldo Sandulli, Nicola Reale, Oronzo Reale, Ettore Gallo, Annibale Marini, Franco Gallo, Maria Alessandra Sandulli, Francesco Saverio Marini. L'abbinamento non può usare il solo cognome.
- Note biografiche vuote: 4; lunghezza mediana 248 caratteri. Contengono la professione al momento dell'elezione (utile per D4).

Giudici senza data di cessazione, con l'ultima decisione in cui il cognome compare nel collegio (stima: i cognomi condivisi possono confondere):

| giudice | giuramento | ultimo collegio (stima) |
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

## Sonda grezza sulle citazioni (non validata)

Solo per orientarsi, non per l'analisi: riconosce il primo numero di ogni citazione del tipo "sentenza n. X del AAAA", nel testo delle sentenze (anche il «Ritenuto in fatto») e nell'epigrafe delle ordinanze.

- Menzioni riconosciute: 86,172; verso pronunce inesistenti: 1.9%.
- Verso pronunce depositate prima: 84,386; lo stesso giorno: 145; dopo: 20.
- Pronunce che contengono "in pari data": 328. Le citazioni tra pronunce depositate lo stesso giorno esistono davvero: non sono errori di estrazione.
