# Che cosa c'è nei file dei dati

I file sono stati scaricati l'8/11/2026 con `src/ingest/download.py` (le versioni sono annotate in `data/raw/MANIFEST.csv`). La loro struttura è descritta dal portale in documenti ufficiali (i [DTD](https://dati.cortecostituzionale.it/Scarica_i_dati/I_dtd/I_dtd)), confrontati qui con i file veri. I numeri vengono da `src/ingest/inspect_raw.py`; i risultati completi sono in `reports/data_inspection.md`.

Questo documento descrive i campi dal punto di vista tecnico: come si chiamano, che cosa contengono, quanto sono completi. Il significato giuridico di ogni campo è in `docs/context.md`, sezione 5. Se il significato di un campo non è chiaro, lo si segnala in entrambi i documenti.

I file sono in formato XML: testi in cui ogni informazione sta tra due etichette con il suo nome, per esempio `<anno_pronuncia>2019</anno_pronuncia>`. Qui i nomi delle etichette sono scritti `così`.

## I file

| Archivio | Come arriva | Che cosa contiene, una volta aperto |
| --- | --- | --- |
| Pronunce | 3 file compressi (1956–1980, 1981–2000, dal 2001 a oggi) | Un file per anno, `data/raw/pronunce/<archivio>/Cc_Opendata_Pronunce_AAAA.xml`: 71 file |
| Massime | 3 file compressi, per gli stessi periodi | Un file per anno, `data/raw/massime/<archivio>/Cc_OpenData_Massime_AAAA.xml`: 71 file, fino al 2026 |
| Giudici | 1 file compresso | `data/raw/giudici/Cc_Opendata_AnagraficaGiudici/Cc_Opendata_AnagraficaGiudici.xml` |

I caratteri sono codificati in UTF-8. Nei testi gli a capo sono scritti in due modi diversi; nei testi più vecchi gli spazi riproducono l'impaginazione originale, con molti spazi in fila. Per questo prima di leggere i testi spazi e a capo vengono uniformati.

## Pronunce

Il file contiene un blocco `<pronuncia>` per ogni decisione: 22.427 in tutto, 11.735 sentenze e 10.692 ordinanze.

**L'intestazione di ogni pronuncia (`pronuncia_testata`)**

| Campo | Che cosa contiene, con un esempio | Note |
| --- | --- | --- |
| `anno_pronuncia` | L'anno, per esempio `2019` | È l'anno del deposito, non della decisione |
| `numero_pronuncia` | Il numero, per esempio `1` | Riparte da 1 ogni anno, è unico per sentenze e ordinanze, senza buchi |
| `ecli` | Il codice europeo della decisione, per esempio `ECLI:IT:COST:2019:1` | Non è descritto nei documenti ufficiali, ma è sempre coerente con anno e numero |
| `tipologia_pronuncia` | `S` (sentenza) o `O` (ordinanza) | — |
| `presidente` | Il cognome del Presidente, per esempio `LATTANZI` | Solo il cognome, in maiuscolo |
| `relatore_pronuncia` | Nome e cognome del relatore, per esempio `Mario Rosario Morelli` | Dal 2016 a volte più nomi separati da " - "; in alcune pronunce recenti con un titolo davanti ("prof.") |
| `redattore_pronuncia` | Nome e cognome di chi ha scritto la pronuncia | Vuoto fino al 2001 (nel 99,6% delle pronunce degli anni Novanta e nell'81% di quelle del 2001), compilato dal 2002 |
| `data_decisione` | La data della decisione, per esempio `21/11/2018` | Giorno/mese/anno; 3 vuote |
| `data_deposito` | La data del deposito, per esempio `09/01/2019` | Giorno/mese/anno; in 17 casi è precedente alla decisione, quindi sbagliata |

**Il testo di ogni pronuncia (`pronuncia_testo`)**

| Parte | Che cosa contiene | Note |
| --- | --- | --- |
| `collegio` | L'elenco dei giudici: "LA CORTE COSTITUZIONALE composta dai signori: …" | Testo libero. Nel formato vecchio: "Avv. NOME COGNOME, Presidente - Dott. … , Giudici,"; in quello recente: "Presidente: Nome COGNOME; Giudici : Nome COGNOME, …". Rari errori di trascrizione nei nomi (per esempio "PERASS1") |
| `epigrafe` | "ha pronunciato la seguente SENTENZA nel giudizio …": chi ha portato la questione davanti alla Corte e su quale legge | Contiene i numeri dei registri ("iscritta al n. 7 del registro ricorsi 2018") e il nome del relatore. **Nelle ordinanze contiene anche il ragionamento della Corte** ("Ritenuto che…", "Considerato che…") |
| `testo` | Il testo delle sentenze | Contiene i titoli «Ritenuto in fatto» e «Considerato in diritto», marcati con due etichette che racchiudono solo il titolo: il testo della parte viene dopo. Ci sono in 11.693 sentenze su 11.735, mai nelle ordinanze; nelle ordinanze questa parte è vuota nel 96% dei casi |
| `dispositivo` | La decisione: "per questi motivi LA CORTE COSTITUZIONALE dichiara …" | Finisce con luogo e data della decisione, firme e data di deposito. Le firme cambiano: tutti i giudici fino alla 286/1986; poi "Il Presidente: X / Il redattore: Y" fino al 2002; dal 2002–2003 "F.to: Nome COGNOME, Presidente / Nome COGNOME, Redattore (o Redattrice)" |

## Massime

Il file contiene un blocco `<pronuncia>` per ogni decisione, con le sue massime: 22.427 pronunce, le stesse dell'archivio delle pronunce.

| Campo | Che cosa contiene, con un esempio | Note |
| --- | --- | --- |
| Anno, numero, tipo, date della pronuncia | Come nell'archivio delle pronunce | Coincidono con l'archivio delle pronunce |
| `tipologia_giudizio` | Il tipo di giudizio, per esempio `GIUDIZIO DI LEGITTIMITÀ COSTITUZIONALE IN VIA PRINCIPALE` | 13 valori diversi, alcuni uniti con "+"; 8 vuoti |
| `massima/numero` | Il numero della massima, per esempio `40214` | Identifica la massima |
| `massima/titolo` | Le voci che classificano la massima, per esempio "Demanio e patrimonio … - Norme della Regione Liguria - … - Illegittimità costituzionale …" | Voci separate da " - "; fino al 2014 spesso tutto in maiuscolo e con un'abbreviazione davanti, come "SENT. 1/60 A." (nel 56% dei titoli) |
| `massima/testo` | Il testo della massima | — |
| `massima/parametri/parametro` | Le norme della Costituzione (o di leggi costituzionali) che si dicono violate: atto, numero, data, articolo, comma | Presenti nell'86,3% delle massime. Contando solo la Costituzione (conteggio del 19/11/2026, `src/analysis/parametri.py`): almeno un articolo nel 77,9% delle massime e nel 92,9% delle pronunce con massime. Per decennio: anni '50 80%, '60 80%, '70 89%, '80 91%, '90 94%, 2000 97%, 2010 96%, 2020 97%. In tutto 139 articoli diversi, 2,6 per pronuncia in media; l'art. 3 (uguaglianza) è nel 64,7% delle pronunce |
| `massima/norme/norma` | Le leggi impugnate, cioè le norme di cui si discute se sono costituzionali (legge 87/1953, art. 23), con gli stessi campi | Presenti nell'85,6% delle massime, con l'articolo nel 77,3%. Massime con leggi impugnate, per decennio: anni '50 72,6%, '60 84,0%, '70 81,0%, '80 91,1%, '90 86,5%, 2000 88,3%, 2010 90,8%, 2020 71,0%. Pronunce con leggi impugnate in almeno una massima: 96,6%. Conteggi del 18/11/2026, da `src/analysis/d3_memoria_collegiale.py` (voce `norme_coverage` di `reports/d3_results.json`) |

Massime per pronuncia: di solito una (mediana 1), al massimo 59. Pronunce con almeno una massima: tutte fino al 2025, il 73% nel 2026 (le massime arrivano qualche mese dopo la pronuncia).

## Giudici

Il file contiene una riga (`<Giudice_costituzionale>`) per giudice: 136 righe.

| Campo | Esempio | Note |
| --- | --- | --- |
| `Titolo` | `prof.` | Vuoto in 73 righe; scritto in modi diversi ("prof.", "Prof.", "prof.ssa") |
| `Nome`, `Cognome`, `Nome_Cognome` | `Antonino`, `PAPALDO`, `Antonino Papaldo` | Alcuni cognomi hanno delle iniziali in più per distinguere giudici con lo stesso cognome ("SANDULLI M. A.", "MARINI F. S.") |
| `Eletto_da` | `Consiglio di Stato` | Chi ha nominato il giudice: 5 valori; "Corte dei Conti" e "Corte dei conti" vanno uniformati |
| `data_nomina`, `data_giuramento`, `data_cessazione` | `15/12/1955` | La data di fine mandato manca per 33 giudici, anche per molti che hanno già finito; un errore (Spagnoli) |
| `Nota_biografica` | "PAPALDO prof. Antonino, nato a … Presidente di sezione del Consiglio di Stato. Eletto …" | Breve biografia con la professione al momento della nomina; 4 vuote. Da qui si ricava in automatico la provenienza usata in D4 |

Le 11 righe con più nomi ("Giorgio Lattanzi - Marta Cartabia") e tutti gli altri campi vuoti corrispondono alle pronunce scritte da più giudici: non sono giudici, e vengono scartate.

## Che cosa non è usato

- Le versioni CSV e JSON degli stessi archivi: le massime in quei formati si fermano al 2015.
- I registri delle cause in corso (ordinanze, ricorsi, conflitti), che riguardano solo cause non ancora decise.
