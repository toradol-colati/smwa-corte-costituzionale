# Schema dei dati

File scaricati l'8/11/2026 con `src/ingest/download.py` (versioni in `data/raw/MANIFEST.csv`). Struttura dichiarata dal portale nei [DTD](https://dati.cortecostituzionale.it/Scarica_i_dati/I_dtd/I_dtd), confrontata con i file. I numeri vengono da `src/ingest/inspect_raw.py`; il report completo è in `reports/data_inspection.md`.

Questo documento contiene i dettagli tecnici. Il significato giuridico di ogni campo è in `docs/context.md`, sezione 5: un campo il cui significato non è chiaro si segnala in tutti e due i documenti.

## File

| Archivio | Origine | Contenuto dopo l'estrazione |
| --- | --- | --- |
| Pronunce | 3 zip (1956–1980, 1981–2000, 2001–oggi) | `data/raw/pronunce/<zip>/Cc_Opendata_Pronunce_AAAA.xml`, un file per anno, 71 file |
| Massime | 3 zip, stessi periodi | `data/raw/massime/<zip>/Cc_OpenData_Massime_AAAA.xml`, un file per anno, 71 file, fino al 2026 |
| Giudici | 1 zip | `data/raw/giudici/Cc_Opendata_AnagraficaGiudici/Cc_Opendata_AnagraficaGiudici.xml` |

Codifica UTF-8. Nei testi gli a capo sono `\r\n`, a volte scritti come entità `&#13;`; nei testi più vecchi la spaziatura riproduce l'impaginazione originale, con molti spazi.

## Pronunce

Radice `<elenco_pronunce>`, un `<pronuncia>` per decisione: 22.427 in tutto, 11.735 sentenze e 10.692 ordinanze.

**`pronuncia_testata`**

| Campo | Tipo ed esempio | Note |
| --- | --- | --- |
| `anno_pronuncia` | intero, `2019` | Anno del deposito |
| `numero_pronuncia` | intero, `1` | Numerazione annuale, comune a sentenze e ordinanze, senza buchi |
| `ecli` | `ECLI:IT:COST:2019:1` | Non dichiarato nel DTD; sempre coerente con anno e numero |
| `tipologia_pronuncia` | `S` o `O` | — |
| `presidente` | `LATTANZI` | Solo cognome, maiuscolo |
| `relatore_pronuncia` | `Mario Rosario Morelli` | Nome e cognome; dal 2016 più nomi separati da " - "; prefissi come "prof." in alcune pronunce recenti |
| `redattore_pronuncia` | come il relatore | Vuoto fino al 2001 (99,6% negli anni Novanta, 81% nel 2001), compilato dal 2002 |
| `data_decisione` | `21/11/2018` | gg/mm/aaaa; 3 vuote |
| `data_deposito` | `09/01/2019` | gg/mm/aaaa; 17 casi precedenti alla decisione (errori) |

**`pronuncia_testo`**

| Elemento | Contenuto | Note |
| --- | --- | --- |
| `collegio` | `<titolo>LA CORTE COSTITUZIONALE</titolo>composta dai signori: …` | Testo libero. Formato vecchio: "Avv. NOME COGNOME, Presidente - Dott. … , Giudici,"; formato recente: "Presidente: Nome COGNOME; Giudici : Nome COGNOME, …". Rari errori di trascrizione ("PERASS1") |
| `epigrafe` | "ha pronunciato la seguente `<titolo>SENTENZA</titolo>` nel giudizio …" | Atti introduttivi, con i numeri di registro ("iscritta al n. 7 del registro ricorsi 2018"), il relatore udito. **Nelle ordinanze contiene anche la motivazione** ("Ritenuto che…", "Considerato che…") |
| `testo` | testo delle sentenze | Contiene i marcatori `<fatto>Ritenuto in fatto</fatto>` e `<diritto>Considerato in diritto</diritto>`: il tag racchiude solo il titolo, il testo della sezione lo segue. Presenti in 11.693 sentenze su 11.735, mai nelle ordinanze; vuoto nel 96% delle ordinanze |
| `dispositivo` | "per questi motivi LA CORTE COSTITUZIONALE dichiara …" | Finisce con luogo e data della decisione, firme e data di deposito. Firme: tutti i giudici fino a 286/1986; poi "Il Presidente: X / Il redattore: Y" fino al 2002; dal 2002–2003 "F.to: Nome COGNOME, Presidente / Nome COGNOME, Redattore (o Redattrice)" |

## Massime

Radice `<corte_costituzionale_archiviomassime>`, un `<pronuncia>` per decisione: 22.427, le stesse dell'archivio delle pronunce.

| Campo | Tipo ed esempio | Note |
| --- | --- | --- |
| `pronuncia_testata/anno_pronuncia`, `numero_pronuncia`, `tipologia_pronuncia`, `data_decisione`, `data_deposito` | come nelle pronunce | Coerenti con l'archivio delle pronunce |
| `pronuncia_testata/tipologia_giudizio` | `GIUDIZIO DI LEGITTIMITÀ COSTITUZIONALE IN VIA PRINCIPALE` | 13 valori, compresi alcuni combinati con "+"; 8 vuoti |
| `massime/massima/numero` | `40214` | Identificativo unico della massima |
| `massime/massima/titolo` | "Demanio e patrimonio … - Norme della Regione Liguria - … - Illegittimità costituzionale …" | Voci separate da " - "; fino al 2014 spesso tutto maiuscolo e con prefisso "SENT. 1/60 A." (56% dei titoli) |
| `massime/massima/testo` | testo della massima | CDATA |
| `massime/massima/parametri/parametro` | `codice`, `descrizione`, `numero`, `data`, `articolo`, `specificazione_articolo`, `comma`, `specificazione_comma` | Parametri costituzionali invocati; nell'86,3% delle massime. `codice` non è nel DTD Voci della Costituzione (`descrizione` = "Costituzione"), conteggio del 19/11/2026 da `src/analysis/parametri.py`: almeno un articolo nel 77,9% delle massime e nel 92,9% delle pronunce con massime (1950: 80%, 1960: 80%, 1970: 89%, 1980: 91%, 1990: 94%, 2000: 97%, 2010: 96%, 2020: 97%); 139 articoli distinti, 2,6 per pronuncia in media; l'art. 3 è nel 64,7% delle pronunce |
| `massime/massima/norme/norma` | stessi campi | Norme oggetto del giudizio (legge 87/1953, art. 23); nell'85,6% delle massime, con l'articolo nel 77,3%. Per decennio, massime con norme: 1950 72,6%, 1960 84,0%, 1970 81,0%, 1980 91,1%, 1990 86,5%, 2000 88,3%, 2010 90,8%, 2020 71,0%. Pronunce con norme in almeno una massima: 96,6%. Conteggi del 18/11/2026, da `src/analysis/d3_memoria_collegiale.py` (`norme_coverage` in `reports/d3_results.json`) |

Massime per pronuncia: mediana 1, massimo 59. Pronunce con almeno una massima: tutte fino al 2025, 73% nel 2026.

## Giudici

Radice `<Anagrafica_giudici_costituzionali>`, un `<Giudice_costituzionale>` per riga: 136 righe.

| Campo | Esempio | Note |
| --- | --- | --- |
| `Titolo` | `prof.` | Vuoto in 73 righe; grafie diverse ("prof.", "Prof.", "prof.ssa") |
| `Nome`, `Cognome`, `Nome_Cognome` | `Antonino`, `PAPALDO`, `Antonino Papaldo` | Alcuni cognomi hanno un suffisso per distinguere gli omonimi ("SANDULLI M. A.", "MARINI F. S.") |
| `Eletto_da` | `Consiglio di Stato` | 5 valori; "Corte dei Conti" e "Corte dei conti" da uniformare |
| `data_nomina`, `data_giuramento`, `data_cessazione` | `15/12/1955` | `data_cessazione` vuota per 33 giudici, compresi molti già cessati; un errore (Spagnoli) |
| `Nota_biografica` | "PAPALDO prof. Antonino, nato a … Presidente di sezione del Consiglio di Stato. Eletto …" | Professione al momento dell'elezione; 4 vuote |

Le 11 righe con più nomi ("Giorgio Lattanzi - Marta Cartabia"), con tutti gli altri campi vuoti, corrispondono alle pronunce con più redattori: non sono giudici.

## Non usati per ora

- Le versioni CSV e JSON degli stessi archivi. Le massime CSV e JSON si fermano al 2015.
- I registri delle norme pendenti (ordinanze, ricorsi, conflitti), che riguardano solo le cause in corso.
