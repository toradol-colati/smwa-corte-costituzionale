# Il confronto con la banca dati SPARQL della Corte

Prodotto da `src/ingest/sparql_check.py` il 12/11/2026 alle 00:20 (ora UTC). Oltre ai file da scaricare, la Corte ha una banca dati che un programma può interrogare con il linguaggio SPARQL, all'indirizzo `https://dati.cortecostituzionale.it/sparql/endpoint`. È una seconda fonte ufficiale: confrontandola con i file scaricati, elencati in `data/raw/MANIFEST.csv`, si possono scoprire errori nei file. La banca dati si aggiorna di continuo, mentre i file sono quelli di un giorno preciso: negli anni più recenti qualche differenza è normale.

## In breve

Questo file confronta i file scaricati con una seconda fonte ufficiale della Corte, la sua banca dati interrogabile con il linguaggio SPARQL, per scoprire errori nei file. Il risultato principale: il relatore coincide quasi sempre, e quasi tutte le differenze sono due errori di grafia nei file ("Caianello" per Caianiello, "Capolozza" per Capalozza), poi corretti nel programma che riconosce i giudici. Il confronto non è stato rifatto dopo il 12/11/2026, perché la banca dati cambia ogni giorno.

## Che cosa contiene la banca dati

La banca dati descrive quattro tipi di oggetti: pronunce, massime, giudici e sedute della Corte. Ogni informazione è registrata come una "tripla": oggetto, proprietà, valore (per esempio: una pronuncia, "relatore", un giudice). Per ogni proprietà le tabelle dicono quante triple ci sono: è un modo per vedere quanto è completa ogni informazione. "onto:" abbrevia `https://dati.cortecostituzionale.it/ontology/`, cioè le proprietà definite dalla Corte; le altre vengono da vocabolari usati da molte banche dati.

**Pronunce**

| Proprietà (nome tecnico) | Che cosa è | Triple |
| --- | --- | --- |
| onto:massima | massime della pronuncia | 46683 |
| onto:relatorePronuncia | relatore | 22460 |
| http://dbpedia.org/ontology/number | numero | 22429 |
| http://purl.org/dc/elements/1.1/identifier | codice identificativo | 22429 |
| http://purl.org/dc/elements/1.1/type | tipo | 22429 |
| http://rdfs.org/sioc/ns#content | testo | 22429 |
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | tipo di oggetto (pronuncia, massima…) | 22429 |
| http://www.w3.org/2000/01/rdf-schema#label | nome leggibile | 22429 |
| http://www.w3.org/2006/time#year | anno | 22429 |
| onto:tipoProcedimento | tipo di procedimento | 22429 |
| onto:presidentePronuncia | presidente | 21523 |
| onto:seduta | seduta | 19417 |
| onto:tipoDispositivo | esito | 8990 |

**Massime**

| Proprietà (nome tecnico) | Che cosa è | Triple |
| --- | --- | --- |
| http://dbpedia.org/ontology/number | numero | 46683 |
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | tipo di oggetto (pronuncia, massima…) | 46683 |
| http://www.w3.org/2000/01/rdf-schema#label | nome leggibile | 46683 |
| onto:testoMassima | testo della massima | 46643 |
| onto:riferimentoCostMassima | riferimenti alla Costituzione | 14773 |
| onto:riferimentoNormMassima | riferimenti ad altre norme | 13922 |

**Giudici**

| Proprietà (nome tecnico) | Che cosa è | Triple |
| --- | --- | --- |
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | tipo di oggetto (pronuncia, massima…) | 136 |
| http://www.w3.org/2002/07/owl#sameAs | lo stesso oggetto in un'altra banca dati | 136 |
| http://xmlns.com/foaf/0.1/name | nome | 136 |
| http://xmlns.com/foaf/0.1/surname | cognome | 136 |
| http://xmlns.com/foaf/0.1/title | titolo (prof., dott.…) | 136 |
| http://www.w3.org/2000/01/rdf-schema#comment | nota | 121 |
| http://xmlns.com/foaf/0.1/depiction | immagine | 84 |

**Sedute**

| Proprietà (nome tecnico) | Che cosa è | Triple |
| --- | --- | --- |
| onto:haMembro | membri (giudici) | 12546 |
| onto:verbale | verbale | 7678 |
| http://purl.org/dc/elements/1.1/date | data | 943 |
| http://purl.org/dc/elements/1.1/type | tipo | 943 |
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | tipo di oggetto (pronuncia, massima…) | 943 |
| http://www.w3.org/2000/01/rdf-schema#label | nome leggibile | 943 |

## Le pronunce

- Pronunce diverse: nella banca dati 22.429, nei file 22.427.
- Anni in cui i due conteggi non coincidono:

| Anno | Nei file | Nella banca dati |
| --- | --- | --- |
| 2026 | 191 | 193 |

- Triple che dicono "questo oggetto è una pronuncia": 22.461, più delle 22.429 pronunce. Il motivo: nella banca dati una pronuncia con più relatori è registrata una volta per ogni relatore (controllato sulle pronunce 194/2019, 102/2016 e 119/2024). Quindi contare queste triple non dà il numero delle pronunce. Triple con il relatore: 22.461.

## Il relatore: banca dati e file a confronto

- Pronunce confrontate: 22.426. Il relatore coincide, cioè ogni cognome della banca dati compare nel relatore dei file, nel **97,12%** dei casi; le differenze sono 645.
- Le differenze, raggruppate per coppia di nomi (11 coppie). Un nome scritto in due modi simili è di solito un errore di grafia; una casella vuota vuol dire che nei file il relatore manca.

| Nei file | Nella banca dati | Pronunce |
| --- | --- | --- |
| Vincenzo Caianello | CAIANIELLO | 471 |
| Enzo Capolozza | CAPALOZZA | 164 |
|  | SILVESTRI / FRIGO | 2 |
|  | DE STEFANO / PALADIN | 1 |
|  | FERRI / GUIZZI | 1 |
|  | FERRI / SPAGNOLI | 1 |
|  | GRECO / LA PERGOLA | 1 |
|  | GRECO / SAJA | 1 |
|  | MEZZANOTTE / CAPOTOSTI | 1 |
|  | SANTOSUOSSO / CHIEPPA | 1 |
|  | TESAURO / VACCARELLA | 1 |

## Le massime

- Massime diverse: nella banca dati 46.683, nei file 46.658.
- Anni in cui i due conteggi non coincidono:

| Anno | Nei file | Nella banca dati |
| --- | --- | --- |
| 2016 | 663 | 665 |
| 2020 | 934 | 935 |
| 2021 | 954 | 955 |
| 2022 | 806 | 808 |
| 2026 | 439 | 458 |

## I giudici

- Giudici: nella banca dati 136; righe dell'elenco dei giudici nei file 136, di cui 11 con più nomi insieme (corrispondono alle pronunce scritte da più giudici, non a persone).

## L'esito delle pronunce (`tipoDispositivo`)

La banca dati dice anche l'esito di ogni pronuncia, per esempio "non fondatezza" o "illegittimità costituzionale". La tabella dà, per ogni anno in cui c'è almeno un esito, quante pronunce lo hanno e la quota sul totale delle pronunce nei file (1 = tutte; sopra 1 se la banca dati ha più pronunce dei file).

| Anno | Pronunce nei file | Con l'esito nella banca dati | Quota |
| --- | --- | --- | --- |
| 1989 | 596 | 1 | 0,002 |
| 2005 | 482 | 310 | 0,643 |
| 2006 | 463 | 459 | 0,991 |
| 2007 | 464 | 464 | 1 |
| 2008 | 449 | 449 | 1 |
| 2009 | 342 | 342 | 1 |
| 2010 | 376 | 376 | 1 |
| 2011 | 342 | 342 | 1 |
| 2012 | 316 | 316 | 1 |
| 2013 | 326 | 326 | 1 |
| 2014 | 286 | 286 | 1 |
| 2015 | 276 | 276 | 1 |
| 2016 | 292 | 292 | 1 |
| 2017 | 281 | 281 | 1 |
| 2018 | 250 | 250 | 1 |
| 2019 | 291 | 291 | 1 |
| 2020 | 281 | 281 | 1 |
| 2021 | 263 | 263 | 1 |
| 2022 | 270 | 270 | 1 |
| 2023 | 229 | 229 | 1 |
| 2024 | 212 | 212 | 1 |
| 2025 | 219 | 219 | 1 |
| 2026 | 191 | 193 | 1,01 |

- Tipi di esito diversi: 33.

| Codice | Esito | Triple |
| --- | --- | --- |
| 3 | non fondatezza | 1778 |
| 4 | inammissibilità | 1283 |
| 6 | manifesta inammissibilità | 1279 |
| 2 | illegittimità costituzionale parziale | 1085 |
| 1 | illegittimità costituzionale | 1023 |
| 5 | manifesta infondatezza | 521 |
| 16 | estinzione del processo | 484 |
| 7 | restituzione atti - jus superveniens | 321 |
| 9 | cessata materia del contendere | 265 |
| 13 | inammissibile | 177 |
| 12 | ammissibile | 140 |
| 10 | accoglie il ricorso | 139 |
| 20 | altro | 133 |
| 17 | non fondatezza nei sensi di cui in motivazione | 105 |
| 11 | respinge il ricorso | 64 |
| 18 | correzione errore materiale | 60 |
| 14 | improcedibile | 46 |
| 23 | ill. cost. conseg. ex art. 27 legge n. 87/1953 | 29 |
| 24 | ill. cost. parziale conseg. ex art. 27 legge n. 87/1953 | 28 |
| 32 | inammissibilità intervento | 14 |
| 26 | ammissibilità intervento | 10 |
| 30 | ammissibilità referendum | 10 |
| 27 | inammissibilità interventi | 10 |
| 29 | accoglie parzialmente il ricorso | 6 |
| 31 | inammissibilità referendum | 5 |
| 25 | ordinanza istruttoria | 5 |
| 8 | solleva q.l.c. avanti a sè | 5 |
| 22 | respinge istanza di sospensione | 4 |
| 28 | restituzione atti | 3 |
| 34 | rinvio pregiudiziale CGUE | 2 |
| 21 | accoglie istanza di sospensione | 1 |
| 33 | ammissibilità interventi | 1 |
| 35 | rinvio a nuovo ruolo | 1 |
