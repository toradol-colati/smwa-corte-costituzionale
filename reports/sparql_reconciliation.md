# Endpoint SPARQL e file scaricati: verifica e riconciliazione

Generato da `src/ingest/sparql_check.py` il 2026-11-12 00:20 UTC, interrogando `https://dati.cortecostituzionale.it/sparql/endpoint` e confrontando con i file di `data/raw/MANIFEST.csv`. L'endpoint è aggiornato in continuo; i file sono quelli del download registrato nel manifest.

## Metadati esposti

**Pronuncia**

| proprietà | triple |
| --- | --- |
| onto:massima | 46683 |
| onto:relatorePronuncia | 22460 |
| http://dbpedia.org/ontology/number | 22429 |
| http://purl.org/dc/elements/1.1/identifier | 22429 |
| http://purl.org/dc/elements/1.1/type | 22429 |
| http://rdfs.org/sioc/ns#content | 22429 |
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | 22429 |
| http://www.w3.org/2000/01/rdf-schema#label | 22429 |
| http://www.w3.org/2006/time#year | 22429 |
| onto:tipoProcedimento | 22429 |
| onto:presidentePronuncia | 21523 |
| onto:seduta | 19417 |
| onto:tipoDispositivo | 8990 |

**Massima**

| proprietà | triple |
| --- | --- |
| http://dbpedia.org/ontology/number | 46683 |
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | 46683 |
| http://www.w3.org/2000/01/rdf-schema#label | 46683 |
| onto:testoMassima | 46643 |
| onto:riferimentoCostMassima | 14773 |
| onto:riferimentoNormMassima | 13922 |

**Giudice**

| proprietà | triple |
| --- | --- |
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | 136 |
| http://www.w3.org/2002/07/owl#sameAs | 136 |
| http://xmlns.com/foaf/0.1/name | 136 |
| http://xmlns.com/foaf/0.1/surname | 136 |
| http://xmlns.com/foaf/0.1/title | 136 |
| http://www.w3.org/2000/01/rdf-schema#comment | 121 |
| http://xmlns.com/foaf/0.1/depiction | 84 |

**Seduta**

| proprietà | triple |
| --- | --- |
| onto:haMembro | 12546 |
| onto:verbale | 7678 |
| http://purl.org/dc/elements/1.1/date | 943 |
| http://purl.org/dc/elements/1.1/type | 943 |
| http://www.w3.org/1999/02/22-rdf-syntax-ns#type | 943 |
| http://www.w3.org/2000/01/rdf-schema#label | 943 |

## Pronunce

- Pronunce distinte: endpoint 22,429, file 22,427.
- Anni con conteggi diversi:

| index | file | endpoint |
| --- | --- | --- |
| 2026 | 191 | 193 |

- Triple di tipo `Pronuncia`: 22,461, contro 22,429 pronunce distinte. Triple `relatorePronuncia`: 22,461. Nell'endpoint una pronuncia con più relatori riceve una tripla di tipo per ciascun relatore (verificato su 194/2019, 102/2016, 119/2024): il conteggio delle triple di tipo non è il numero delle pronunce.

## Relatore: endpoint e file a confronto

- Pronunce confrontate: 22,426. Concordanza (ogni cognome dell'endpoint compare nel relatore dei file): **97.12%** (645 discordanze).
- Discordanze raggruppate per coppia di nomi (11 coppie distinte; le prime 30):

| file | endpoint | pronunce |
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

## Massime

- Massime distinte: endpoint 46,683, file 46,658.
- Anni con conteggi diversi:

| index | file | endpoint |
| --- | --- | --- |
| 2016 | 663 | 665 |
| 2020 | 934 | 935 |
| 2021 | 954 | 955 |
| 2022 | 806 | 808 |
| 2026 | 439 | 458 |

## Giudici

- Giudici: endpoint 136, righe dell'anagrafica nei file 136 (di cui 11 righe composte da più nomi).

## Esito (`tipoDispositivo`)

| index | pronunce nei file | con esito nell'endpoint | quota |
| --- | --- | --- | --- |
| 1989 | 596 | 1 | 0.002 |
| 2005 | 482 | 310 | 0.643 |
| 2006 | 463 | 459 | 0.991 |
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
| 2026 | 191 | 193 | 1.01 |

- Tipi di esito distinti: 33.

| codice | etichetta | triple |
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
