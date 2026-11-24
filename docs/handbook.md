# Il progetto in un unico documento

## 0. Come usare questo documento

**Che cos'è.** Questo documento descrive tutto il progetto in un solo posto: il contesto giuridico, i dati di partenza, il piano scritto prima dei risultati, ogni passaggio fatto dai programmi, ogni controllo di qualità, ogni risultato, le scelte cambiate dopo, i limiti, i problemi noti, il lavoro che resta, il modo di correggere il lavoro, il significato delle parole tecniche, l'elenco di tutti i file e, alla fine, da quali file è presa ogni sezione.

**A che data si riferisce.** Il documento descrive il repository al 24/11/2026, dopo la costruzione della rete dei collegi tra giudici.

**Chi vince in caso di conflitto.** Il documento è scritto a mano e nessun controllo automatico ne verifica i numeri. Se un numero di questo documento è diverso da quello di un altro file, vale l'altro file, in quest'ordine:

1. i file dei risultati in `reports/` (`*.json`), scritti dai programmi;
2. la relazione (`reports/relazione_for_dummies.md`), i cui numeri principali sono confrontati con i file dei risultati da un controllo automatico (`tests/test_report_numbers.py`);
3. per le scelte e le loro date, il registro delle decisioni (`docs/decisions.md`).

**Come sono scritti i numeri.** Formato italiano: la virgola separa i decimali (0,95), il punto separa le migliaia (22.427). Ogni numero è dato, dove serve, con il suo totale ("257 pronunce su 22.427") e con il file da cui viene.

**Come sono indicati i file.** Ogni file è indicato con il suo percorso nel repository, per esempio `src/judges/build_judges.py`. Nella sezione 17 ogni file è segnato in uno di due modi:

- *scritto a mano*: si corregge aprendo il file;
- *scritto dal programma X*: non si corregge a mano, perché la volta successiva che X gira la correzione sparisce; si corregge il programma X.

**Le etichette dei risultati.** Ogni risultato porta una delle tre etichette usate nella relazione:

- *principale*: fissato prima di vedere i dati; è l'unico da cui si traggono conclusioni formali;
- *esplorativo*: trovato, aggiunto o cambiato dopo aver visto i dati; è un'indicazione da verificare, non una prova;
- *descrittivo*: una descrizione dei dati, senza un'ipotesi da provare.

**Due parole da non confondere.** In questo documento:

- un giudice è **in carica** nel periodo scritto nell'elenco ufficiale dei giudici, dal giuramento alla fine del mandato;
- un giudice è **in attività** dalla prima all'ultima pronuncia in cui siede nel collegio.

Le analisi usano sempre il periodo "in attività", perché le date di fine mandato dell'elenco ufficiale hanno errori (sezione 11.5). La relazione chiama a volte "in carica" anche il periodo "in attività": dove la relazione dice "un giudice in carica manca dal 6,3% delle pronunce", il periodo è quello "in attività".

**Come è scritto.** In forma impersonale. Le parole tecniche sono spiegate la prima volta che compaiono e raccolte nel glossario (sezione 16).

## 1. Il progetto in breve

**Che cos'è.** È il progetto d'esame di Umberto Toraldo per il corso Social Media and Web Analytics (EM1421, Università Ca' Foscari Venezia, anno accademico 2026/27, docente Pierluigi Zama Ramirez). Il progetto vale il 70% del voto. Il tema non è ancora stato approvato dal docente.

**La domanda di ricerca**, nella sua formulazione unica, da usare identica nel riassunto e nella presentazione: "In un ordinamento in cui il precedente non vincola, la Corte costituzionale costruisce comunque una gerarchia di precedenti? E quanto di quell'autorità passa attraverso i giudici che redigono e decidono le pronunce?"

**La stessa domanda in parole semplici.** In Italia una decisione della Corte costituzionale non obbliga la Corte a decidere allo stesso modo in futuro (il precedente "non vincola"). Eppure la Corte cita di continuo le proprie decisioni passate. Il progetto chiede due cose:

1. alcune decisioni vengono citate moltissimo e altre quasi mai, più di quanto succederebbe per caso?
2. conta chi ha partecipato alla decisione? In particolare: un giudice che scrive una nuova decisione cita di più le decisioni prese da collegi in cui sedeva, o quelle che ha scritto lui?

**Le quattro domande con il loro nome breve**, usato in tutti i file:

| Nome | Domanda | Etichetta |
| --- | --- | --- |
| D1 | Le citazioni sono concentrate su poche pronunce? Le pronunce "più autorevoli" secondo l'algoritmo HITS sono le più citate? | Secondario; parti esplorative |
| D1b | Quanto dura un precedente, cioè per quanti anni viene citato? | Secondario |
| D2 | Le pronunce scritte da un certo giudice sono citate più di quanto ci si aspetta? Anche dopo la fine del suo mandato? | Esplorativo (il confronto con il caso è cambiato dopo i risultati) |
| D3 | A parità di età e materia del precedente, un giudice che scrive una pronuncia cita di più i precedenti decisi da collegi in cui sedeva senza averli scritti? | **Principale** |
| D4 | I giudici con la stessa provenienza professionale o nominati dallo stesso organo si citano di più tra loro? | Estensione, fatta perché la potenza statistica bastava |

**Che cosa si è fatto, in cinque passaggi.**

1. Sono stati scaricati i file aperti della Corte (8/11/2026): 22.427 pronunce dal 1956 al 2026, le loro massime, l'elenco dei giudici.
2. Dal testo di ogni pronuncia un programma ha estratto le citazioni di pronunce precedenti: 93.467 legami "A cita B".
3. Ogni pronuncia è stata collegata al giudice che l'ha scritta (il redattore) e ai giudici che sedevano nel collegio.
4. Ogni risultato è stato confrontato con ciò che succederebbe se le citazioni andassero a caso, rifacendo il calcolo su molte versioni dei dati rimescolate.
5. Le regole principali sono state scritte prima di vedere i risultati; ciò che è stato cambiato o aggiunto dopo porta l'etichetta *esplorativo*.

**Che cosa si è trovato, in tre frasi.**

- Le citazioni sono concentrate: l'1% delle pronunce più citate raccoglie il 10,3% delle citazioni, contro il 3,4% che darebbe il caso; ma un precedente è citato soprattutto nei primi anni (il picco è a un anno dal deposito) e poi viene in parte sostituito dalle pronunce che lo hanno citato (esplorativo).
- **Risultato principale:** aver partecipato a una decisione non la rende più citata da chi c'era. L'odds ratio è 1,00, con intervallo di confidenza al 95% da 0,92 a 1,09: i dati escludono un effetto superiore al 9% circa in più o all'8% in meno.
- Averla scritta, invece, conta: un giudice cita circa 5,5 volte di più i precedenti scritti da lui (odds ratio 5,47; esplorativo), e circa 3,3 volte a parità di legge impugnata (3,27): gran parte dell'effetto viene dal fatto che le questioni ripetute vanno allo stesso giudice.

I numeri vengono da `reports/d1_results.json`, `reports/d3_results.json` e `reports/precedent_succession.json`; i dettagli sono nella sezione 9.

## 2. Il contesto: la Corte e come nasce una pronuncia

Questa sezione riassume `docs/context.md`, che riporta per ogni affermazione la fonte (leggi, regole della Corte, studi) e uno stato: *Fonte* (verificato sulla fonte), *Dati* (verificato sui file), *Da verificare*.

### 2.1 La Corte

- **Quanti giudici e chi li nomina.** I giudici sono 15: 5 nominati dal Presidente della Repubblica, 5 eletti dal Parlamento in seduta comune, 5 dalle supreme magistrature (3 dalla Corte di cassazione, 1 dal Consiglio di Stato, 1 dalla Corte dei conti).
- **Quanto dura il mandato.** 9 anni dal giuramento. Fino al 1967 durava 12 anni (legge costituzionale 2/1967, trovata ma non ancora letta). Nei dati i 26 giudici che hanno giurato prima del 1967 sono rimasti in carica 11,8 anni in mediana.
- **Il Presidente della Corte.** È eletto dai giudici tra di loro. Decide l'ordine dei lavori, nomina i relatori e, se i voti sono pari, il suo voto decide.
- **Che cosa fa la Corte.** Giudica se le leggi dello Stato e delle Regioni rispettano la Costituzione; risolve i conflitti tra poteri dello Stato e tra Stato e Regioni; decide se un referendum per abrogare una legge si può fare; giudica le accuse contro il Presidente della Repubblica.

### 2.2 Chi fa che cosa in una pronuncia

- **Pronuncia.** Ogni decisione della Corte. Nei file ci sono due tipi: la **sentenza**, che decide in via definitiva, e l'**ordinanza**, che ha una motivazione breve (legge 87/1953, art. 18). Nei file ci sono 11.735 sentenze e 10.692 ordinanze.
- **Collegio.** Il gruppo di giudici che decide una pronuncia: i giudici presenti all'udienza o alla camera di consiglio (la riunione riservata dei giudici) in cui la causa è trattata. Servono almeno 11 giudici (legge 87/1953, art. 16), quindi un collegio ha da 11 a 15 giudici. Decide la maggioranza; il voto non è pubblico e la Corte non pubblica opinioni dissenzienti. Far parte del collegio non vuol dire aver votato a favore.
- **Relatore.** Il giudice nominato dal Presidente per studiare la causa e presentarla al collegio. Vota per primo.
- **Redattore.** Il giudice che scrive il testo della pronuncia dopo il voto. Di regola è il relatore; il Presidente può affidare la scrittura a un altro giudice o a più giudici. Il testo è approvato dal collegio. Per questo nei risultati si scrive sempre "pronunce redatte da X", mai "decisioni di X": la decisione è del collegio.
- **Assistenti di studio.** Aiutano i giudici a studiare le cause e a scrivere; non firmano, quindi non compaiono nei dati.
- **Legge impugnata e parametro.** Chi porta una questione alla Corte indica la legge che ritiene incostituzionale (la legge impugnata, o norma oggetto) e le norme della Costituzione che ritiene violate (il parametro) (legge 87/1953, art. 23). Nei dati sono i campi `norme/norma` e `parametri/parametro` delle massime.
- **Massima.** Il riassunto del principio stabilito da una pronuncia. Lo scrive un ufficio della Corte (l'Ufficio del massimario), non i giudici.

### 2.3 La vita di una pronuncia

1. **Si apre il giudizio**, con un atto scritto in un registro della cancelleria. Per esempio l'ordinanza con cui un giudice, durante una causa, porta una questione alla Corte (ordinanza di rimessione, registro "R.O."). Per questo nei testi "ordinanza n. X del AAAA" può indicare un atto di un registro e non una pronuncia della Corte.
2. **Il Presidente nomina il relatore** e fissa l'udienza o la camera di consiglio.
3. **Il collegio decide**: è la data della decisione.
4. **Il redattore scrive il testo** e il collegio lo approva.
5. **La pronuncia si deposita** in cancelleria: da quel giorno chiunque può conoscerla e citarla. L'anno e il numero della pronuncia seguono il deposito, non la decisione. Per metà delle pronunce passano 9 giorni o meno tra decisione e deposito.
6. **La pronuncia si pubblica** sulla Gazzetta Ufficiale (la data non è nei file).
7. **L'Ufficio del massimario scrive le massime**, qualche mese dopo: del 2026 il 73% delle pronunce ha già le massime; fino al 2025 tutte.

**Due tipi di giudizio da conoscere.** Nel giudizio **in via incidentale** la questione è sollevata da un giudice durante una causa (legge 87/1953, art. 23). Nel giudizio **in via principale** lo Stato impugna una legge regionale, oppure una Regione impugna una legge dello Stato o di un'altra Regione (Costituzione, art. 127). Nei dati, secondo le massime, 17.052 pronunce sono in via incidentale e 3.234 in via principale.

### 2.4 Che cosa registrano i dati, e da quando

**Il nome di chi ha scritto la pronuncia non c'è sempre.** È la scoperta che più ha cambiato il lavoro.

| Periodo | Che cosa registrano i dati | Che cosa usa il progetto |
| --- | --- | --- |
| Dalla pronuncia 1/1956 alla 286/1986 (5.678 pronunce) | Solo il relatore. Firmano tutti i giudici del collegio: chi ha scritto non è indicato da nessuna parte | Il relatore al posto del redattore: un'approssimazione dichiarata (`redattore_source = relatore_proxy`) |
| Dalla 287/1986 (depositata il 23/12/1986) al 2001 | Il relatore nel campo; il redattore solo nelle firme in fondo al testo ("Il redattore: COGNOME") | Il nome ricavato dalle firme (`redattore_source = signature`) |
| Dal 2002 a oggi | Relatore e redattore nei campi dei dati; dal 2016 anche più redattori ("A - B") | Il nome del campo (`redattore_source = field`) |

Il cambio delle firme si vede nei testi il 23/12/1986, tra la pronuncia 286 e la 287; la dottrina lo data a una modifica delle regole della Corte del luglio 1987 (Caravita 2021). Dove sono compilati sia il relatore sia il redattore (8.384 pronunce, quasi tutte dal 2002), i due sono diversi in 93 casi: per questo l'approssimazione del periodo fino al 1986 è considerata piccola.

**Altre cose che i dati dicono o non dicono.**

- Anno e numero identificano una pronuncia: la numerazione riparte ogni anno, è unica per sentenze e ordinanze, senza doppioni né buchi (controllato su 22.427 pronunce, `reports/data_inspection.md`).
- Il collegio è un testo libero ("composta dai signori: …"), da cui il programma ricava i nomi.
- Il motivo delle assenze dal collegio (malattia, astensione, altri impegni) non è registrato.
- L'esito della pronuncia non è un campo dei file: si prende dalla banca dati SPARQL della Corte, solo dal 2005.
- Pronunce depositate lo stesso giorno possono citarsi a vicenda: per esempio la 135/1970 cita la 134/1970. Queste citazioni sono vere, ma si tengono da parte, fuori dalla rete.

### 2.5 Che cosa misura davvero il progetto

| Si potrebbe credere di misurare | In realtà si misura |
| --- | --- |
| L'influenza di un giudice | L'influenza delle pronunce che ha scritto, decise e approvate dal collegio |
| Chi ha scritto, in tutto il periodo | Prima del 23/12/1986 solo il relatore |
| Che chi scrive condividesse un precedente (D3) | Che sedesse nel collegio che lo ha deciso: l'esposizione al precedente, non l'adesione |
| Collegi quasi sempre completi | Il 70,4% delle pronunce ha meno di 15 giudici; in media 14,6 giudici in attività, 13,7 nel collegio, 0,9 assenti (`reports/d3_absences.json`) |
| La scelta personale di citare un precedente | Una scelta del collegio, scritta dal redattore con i suoi assistenti |
| Relatori assegnati a caso | Il Presidente nomina i relatori con criteri non pubblici, forse per competenza |
| La materia della pronuncia | Una classificazione ricavata dai testi delle massime, scritte da un ufficio |

## 3. I dati di partenza

### 3.1 Da dove vengono

Tutti i dati vengono dal portale open data della Corte costituzionale (dati.cortecostituzionale.it), con licenza CC BY-SA 3.0: si possono usare citando la fonte, e i dati derivati vanno pubblicati con la stessa licenza.

I file sono stati scaricati l'8/11/2026 dal programma `src/ingest/download.py`. Per ogni file il programma scrive in `data/raw/MANIFEST.csv` l'indirizzo, l'ora del download e un'impronta del contenuto (un codice SHA-256, che cambia se cambia anche un solo carattere). Il portale si aggiorna ogni giorno o ogni settimana: il manifest è l'unico modo per sapere quale versione dei dati ha prodotto i risultati.

| Archivio | Come arriva | Che cosa contiene |
| --- | --- | --- |
| Pronunce | 3 file compressi (1956–1980, 1981–2000, dal 2001), un file XML per anno (71 file) | 22.427 pronunce: 11.735 sentenze e 10.692 ordinanze. Per ognuna: anno, numero, tipo, presidente, relatore, redattore (dal 2002), data della decisione, data del deposito, collegio, testo |
| Massime | 3 file compressi, un file XML per anno (71 file) | 46.658 massime. Per ognuna: titolo, testo, tipo di giudizio della pronuncia, leggi impugnate, parametri |
| Giudici | 1 file XML | 136 righe: 125 giudici e 11 righe che uniscono più nomi ("Giorgio Lattanzi - Marta Cartabia"), scartate. Per ogni giudice: nome, chi l'ha nominato (`Eletto_da`), date di nomina, giuramento e fine mandato, breve biografia |

I file sono in formato XML: testi in cui ogni informazione sta tra due etichette con il suo nome, per esempio `<anno_pronuncia>2019</anno_pronuncia>`. La struttura dei campi, con la loro completezza, è descritta in `docs/data_schema.md`.

**Due servizi interrogati da un programma (API).**

- La banca dati della Corte interrogabile con il linguaggio SPARQL (`src/ingest/sparql_check.py`, `src/ingest/fetch_api.py`). Serve per: l'esito delle pronunce dal 2005 (6.741 pronunce, 33 tipi di esito); il controllo del relatore; i giudici presenti alle sedute dal 2004, come controllo del collegio. Non contiene il redattore, le date di decisione e deposito, il collegio.
- Wikipedia in italiano, per sapere quali pronunce sono citate in una voce dell'enciclopedia (283 pronunce).

**Che cosa non è usato.** Le versioni CSV e JSON degli stessi archivi (le massime in quei formati si fermano al 2015); i registri delle cause in corso.

### 3.2 Com'è fatta una pronuncia nel file

Ogni pronuncia ha un'intestazione (`pronuncia_testata`) con i campi principali e un testo (`pronuncia_testo`) diviso in parti:

- `collegio`: l'elenco dei giudici che hanno deciso;
- `epigrafe`: chi ha portato la questione davanti alla Corte e su quale legge. **Nelle ordinanze contiene anche il ragionamento della Corte** ("Ritenuto che…", "Considerato che…");
- `testo`: nelle sentenze contiene il **«Ritenuto in fatto»**, che riassume gli argomenti delle parti, e il **«Considerato in diritto»**, che è il ragionamento della Corte. Le due etichette `<fatto>` e `<diritto>` racchiudono solo il titolo: il testo della parte viene dopo l'etichetta. Nelle ordinanze `testo` è vuoto nel 96% dei casi;
- `dispositivo`: la decisione vera e propria, seguita dalle firme.

### 3.3 Le stranezze dei file, trovate prima di qualsiasi analisi

Tutte vengono da `reports/data_inspection.md` (scritto da `src/ingest/inspect_raw.py`).

- **Date.** 3 date di decisione mancanti; 17 pronunce depositate prima della data di decisione, quindi con una data sbagliata; un errore di data (la 69/1982, depositata il 03/04/1980 secondo i dati). 220 pronunce sono decise in un anno e depositate, quindi numerate, nell'anno dopo.
- **Collegi.** Il 17,6% dei collegi (3.951) ha 11 o 12 giudici: sono validi, perché il numero legale è 11. In 6 collegi dei testi più vecchi ci sono cifre al posto delle lettere ("PERASS1", "MAR10").
- **Spazi.** Nei testi gli a capo sono scritti in due modi e i testi più vecchi hanno molti spazi in fila. Senza uniformarli, la formula «Considerato che» sembrava presente solo nel 50% delle ordinanze; dopo, risulta nel 96%.
- **Elenco dei giudici.** 33 date di fine mandato mancanti; la fine del mandato di Spagnoli è scritta "2005" invece di 1995; altre date sbagliate (Granata, Chiarelli, Mezzanotte); due cognomi scritti male nel campo del nome ("Caianello", "Capolozza"). L'organo "Corte dei Conti" e "Corte dei conti" va uniformato.
- **Massime.** Tutte le pronunce fino al 2025 hanno almeno una massima; del 2026 il 73%. Le materie scritte nei titoli delle massime non sono uniformi (5.363 prime voci diverse): per questo la materia si ricava con un modello di temi (sezione 5.9).
- **L'ultimo anno è incompleto.** Del 2026 ci sono le pronunce fino alla numero 191, depositata il 6/11/2026.
- **Una prima ricerca grezza** delle citazioni, non controllata, trova circa 86.000 menzioni e 328 testi con l'espressione "in pari data": le citazioni tra pronunce depositate lo stesso giorno esistono davvero.

## 4. Il piano scritto prima e come si legge un risultato

### 4.1 Il piano

Il piano del progetto è in `docs/spec.md`. È stato scritto l'8/11/2026, prima di qualsiasi risultato, e aggiornato fino al 18/11/2026. Contiene: la domanda, i dati, come si costruiscono le reti, il significato dei concetti di rete in questo caso, il piano delle analisi, come si controlla ogni risultato, i limiti, il legame con il corso, gli strumenti. Le scelte fatte dopo, con le date, sono nel registro `docs/decisions.md`.

**Le scelte principali fissate prima dei risultati** (registro, righe dell'8/11, 11/11, 12/11 e 16/11/2026):

- il risultato principale: in D3, l'odds ratio di "sedeva nel collegio senza scriverlo", con l'intervallo al 95%, stimato sulle assenze dal collegio, con l'incertezza calcolata raggruppando le pronunce dello stesso redattore;
- le soglie di qualità: estrazione delle citazioni con precisione di almeno 0,95 e richiamo di almeno 0,90, su almeno 460 coppie; nome del redattore collegato all'elenco dei giudici in almeno il 98% delle pronunce; collegio riconosciuto per intero in almeno il 98%;
- ogni risultato con la stima, l'intervallo al 95% e il valore atteso per caso (almeno 1.000 versioni casuali, con un seme fisso); una differenza è reale se il valore p è sotto 0,05, guardando in tutte e due le direzioni;
- il testo in cui si cercano le citazioni (il testo di base, sezione 5.4);
- l'ordine nel tempo delle pronunce: la data del deposito;
- per D3: 50 precedenti non citati per ogni pronuncia che cita (seme 20261116); classi di età 0–1, 1–2, 2–3, 3–4, 4–5, 5–7, 7–10, 10–15, 15–20, 20–30 e oltre 30 anni; la materia come somiglianza dei temi tra la pronuncia che cita e il precedente;
- per D2: solo i giudici con almeno 30 pronunce scritte; citazioni contate entro 10 anni dal deposito; 10 anni dopo il mandato, solo per i giudici usciti entro il 2015; correzione di Holm;
- per D4: effetto minimo d'interesse del 20%; il test si fa solo se la potenza è almeno 0,80;
- i temi: il numero più piccolo, tra 10 e 60 a passi di 10, con una coerenza entro il 2% della migliore.

**Come si verifica che una regola è venuta prima dei risultati.** Il repository (l'archivio del codice con la storia di ogni modifica) è nato il 18/11/2026: per le regole scritte da quel giorno lo dice l'ordine delle modifiche registrate (i commit). Per le regole precedenti, comprese le soglie di qualità e il disegno di D3, la prova sta solo nel registro della sessione di lavoro con l'assistente, che non fa parte del repository: le righe sul disegno di D3 risultano scritte il 16/11/2026 alle 10:48 (ora italiana), e il programma di D3 risulta avviato la prima volta alle 17:21 dello stesso giorno. Le regole sono state scritte dallo stesso assistente che poi ha fatto le analisi, su delega di Umberto.

### 4.2 Come si legge un risultato

Ogni risultato del progetto ha tre parti.

1. **La stima**, per esempio un odds ratio di 1,00.
2. **L'intervallo di confidenza al 95%**, per esempio da 0,92 a 1,09: l'insieme dei valori compatibili con i dati. Se l'intervallo di un rapporto non comprende 1, la differenza si considera reale.
3. **Il confronto con il caso**: che cosa ci si aspetterebbe se non ci fosse nulla oltre il caso (sezione 8).

Il **valore p** è la probabilità di vedere una differenza almeno così grande se in realtà non ci fosse nessuna differenza. Sotto 0,05 la differenza si considera reale. Parole come "forte", "alto" o "concentrato" si usano solo con un test o un confronto dietro.

## 5. Dai file alle tabelle e alle reti: i passaggi, uno per uno

Tutti i programmi sono in Python, nella cartella `src/`, e si lanciano dalla cartella del progetto con `.venv/bin/python <programma>`. Tutto ciò che è casuale parte da un seme fisso (un numero che fa ripartire il generatore casuale sempre dallo stesso punto), quindi rifacendo un calcolo si ottengono gli stessi numeri. Scrivere `REPS=100` davanti ai comandi di analisi riduce le ripetizioni dei confronti con il caso, per una prova veloce.

### 5.0 L'ordine in cui girano i programmi

L'ordine è quello del README e della relazione (sezione 6). Ogni programma usa i file scritti da quelli prima.

| Passo | Programma | Che cosa scrive (i file principali) |
| --- | --- | --- |
| 1 | `src/ingest/download.py` | `data/raw/` (i file del portale) e `data/raw/MANIFEST.csv` |
| 2 | `src/ingest/inspect_raw.py` | `reports/data_inspection.md` |
| 3 | `src/ingest/build_pronunce.py` | `data/interim/pronunce.pkl` (con i testi), `data/processed/pronunce.csv` (senza testi) |
| 4 | `src/extract/citations.py` | `data/processed/citations.csv`, `edges_citations.csv`, `edges_citations_fulltext.csv`; i registri `data/interim/citation_*.csv` |
| 5 | `src/extract/citations_massime.py` | `data/processed/edges_citations_with_notes.csv`, `reports/massime_citations.json` |
| 6 | `src/validation/evaluate.py test` e `test2` | `reports/validation_test.md`, `reports/validation_test2.md` |
| 7 | `src/judges/build_judges.py` | `data/processed/judges.csv`, `pronunce_judges.csv`, `collegio.csv`; `data/interim/collegio_errors.csv`; `reports/judges_quality.md` |
| 8 | `src/analysis/topics.py` | `data/processed/topics_theta.npz`, `topics_pronunce.csv`; `reports/topics.md`, `reports/topics.json` |
| 9 | `src/analysis/parametri.py` | `data/processed/parametri_pronunce.csv`, `reports/parametri.json` |
| 10 | `src/networks/build.py` | `data/processed/nodes.csv`, `edges_redazione.csv`, `edges_judges.csv`; `reports/network_basic.json` |
| 11 | `src/networks/cositting.py` | `data/processed/edges_cositting.csv`, `judges_cositting.csv`, `cositting_network.graphml`; `reports/cositting_network.json` |
| 12 | `src/ingest/fetch_api.py` | `data/processed/esiti.csv`, `wikipedia_links.csv`; `data/interim/sedute_membri.csv`; `reports/api_fetch.json` |
| 13 | `src/analysis/d1_pronunce.py` | `reports/d1_results.json`; `data/interim/d1_yearly.pkl` e `d1_panel_<anno>.pkl` |
| 14 | `src/analysis/d2_d4_giudici.py` | `reports/d2_results.json`, `reports/d4_results.json`, `data/processed/judges_attributes.csv` |
| 15 | `src/analysis/d2_strata_check.py` | `reports/d2_strata_check.json` |
| 16 | `src/analysis/d3_memoria_collegiale.py` | `reports/d3_results.json`, `reports/d3_results.md`; `data/interim/d3_mandate.pkl` |
| 17 | `src/analysis/d3_absences.py` | `reports/d3_absences.json` |
| 18 | `src/analysis/d3_full_check.py` | `reports/d3_full_check.json`; `data/interim/d3_full.pkl` |
| 19 | `src/analysis/precedent_succession.py` | `reports/precedent_succession.json` |
| 20 | `src/analysis/extras.py` | `reports/extras.json`, `data/processed/communities.csv` |
| 21 | `src/analysis/course_measures.py` | `reports/course_measures.json` |
| 22 | `src/analysis/figures.py` | `reports/figures/fig1_…png` … `fig10_…png` |
| 23 | `src/analysis/interactive.py` | `reports/rete_interattiva.html` |
| 24 | `src/report/report_numbers.py` | `reports/numbers.json` |
| 25 | `src/report/plain_intros.py` | il paragrafo "In breve" in testa a 9 report |
| 26 | `src/courts/sizing.py` | `reports/courts_sizing.json`, `data/interim/courts_split.csv` |
| 27 | `src/polarity/contexts.py` | `data/interim/polarity_contexts.pkl` |
| 28 | `src/polarity/evaluate.py claude` | `reports/polarity_validation_claude.md` e `.json` |
| 29 | `.venv/bin/python -m pytest` | nessun file: i controlli automatici (sezione 5.19) |

**Programmi che non sono nell'elenco, e perché.**

- `src/ingest/sparql_check.py` (il confronto con la banca dati SPARQL): interroga una banca dati che cambia nel tempo; si rifà solo con un nuovo download.
- `src/validation/sample_passages.py` e `src/validation/human_sheet.py`: preparano i campioni e il foglio per i controlli a mano; i campioni sono già estratti.
- `src/polarity/draw_sample.py`: ha estratto il campione di prova della polarità e si rifiuta di sovrascriverlo.
- `src/polarity/lexicon.py`: contiene le regole della polarità, usate dagli altri programmi della polarità; non si lancia da solo.
- `src/courts/mentions.py`: il lavoro sulle altre corti è solo impostato (sezione 5.21).

### 5.1 Scaricare i dati

- **Programma:** `src/ingest/download.py` (per un solo archivio: `python3 -I src/ingest/download.py giudici`).
- **Che cosa fa:** scarica dal portale i file compressi delle pronunce, delle massime e dei giudici; li apre ciascuno nella sua cartella, rifiutando i file il cui percorso uscirebbe dalla cartella; annota ogni file in `data/raw/MANIFEST.csv` (file, indirizzo, ora del download in UTC, impronta SHA-256).
- **Regola:** i file in `data/raw/` non si modificano mai a mano; `.claude/settings.json` blocca le modifiche dirette dell'assistente. `data/raw/` resta fuori dal repository, tranne `MANIFEST.csv`.

### 5.2 Il primo controllo dei file

- **Programma:** `src/ingest/inspect_raw.py`, che scrive `reports/data_inspection.md`.
- **Che cosa fa:** solo controlli descrittivi, nessuna analisi: quante pronunce, se la numerazione ha buchi o doppioni, quali date mancano o sono incoerenti, come cambia nel tempo il campo del redattore, quanti giudici ha ogni collegio (contati in modo approssimato), come è diviso il testo, quante massime ci sono, che cosa manca nell'elenco dei giudici, e una prima ricerca grezza delle citazioni.
- **Perché conta:** tutti i numeri di `docs/context.md` e `docs/data_schema.md` vengono da qui. Le stranezze trovate sono elencate nella sezione 3.3.

### 5.3 Il confronto con la banca dati SPARQL

- **Programma:** `src/ingest/sparql_check.py`, che scrive `reports/sparql_reconciliation.md`. Ultima esecuzione: 12/11/2026. Modificato il 21/11/2026 nella parte che scrive il testo, e non più fatto girare (sezione 11.2).
- **Che cosa fa:** chiede alla banca dati SPARQL della Corte (un servizio che risponde a domande scritte nel linguaggio SPARQL) che cosa contiene e confronta i suoi conteggi con i file scaricati: pronunce, massime, giudici, esiti.
- **Il risultato principale:** il relatore dei file coincide con quello della banca dati nel 97,12% di 22.426 pronunce. Delle 645 differenze, 635 sono due errori di grafia nei file ("Caianello" per Caianiello, 471 pronunce; "Capolozza" per Capalozza, 164), corretti nel programma dei giudici; le altre 10 sono pronunce con il relatore vuoto nei file e due relatori nella banca dati.

### 5.4 Preparare i testi

- **Programma:** `src/ingest/build_pronunce.py`.
- **Legge:** i file XML delle pronunce.
- **Che cosa fa:**
  1. uniforma spazi e a capo;
  2. divide il testo di ogni pronuncia nelle sue parti. Nelle sentenze: il «Ritenuto in fatto» è il testo tra le etichette `<fatto>` e `<diritto>`; il «Considerato in diritto» è il testo dopo `<diritto>`. Nelle ordinanze il ragionamento sta nell'epigrafe e viene diviso alla prima formula «Considerato che» (o a una formula equivalente). Il dispositivo è preso senza il blocco delle firme;
  3. corregge gli errori di dati documentati in `reports/data_inspection.md`.
- **Scrive:** `data/interim/pronunce.pkl` (una riga per pronuncia, con i testi; fuori dal repository) e `data/processed/pronunce.csv` (gli stessi dati senza i testi).
- **Il testo di base.** È il testo in cui si cercano le citazioni: il «Considerato in diritto» con il dispositivo nelle sentenze, il «Considerato che» con il dispositivo nelle ordinanze. Il «Ritenuto in fatto» è escluso perché riassume gli argomenti del giudice che ha sollevato la questione e delle parti, con le loro citazioni: non sono citazioni della Corte. Entra solo nella variante "testo intero".
- **I testi non divisi:** in 322 testi (1,4% delle pronunce: 305 ordinanze e 17 sentenze) la divisione non è riuscita, e si usa il testo intero (`reports/numbers.json`).

### 5.5 Estrarre le citazioni

- **Programma:** `src/extract/citations.py` (l'estrattore).
- **Legge:** `data/interim/pronunce.pkl`.
- **Che cosa fa.** Cerca nel testo le forme con cui la Corte cita una propria pronuncia: una parola come sentenza, ordinanza, sent., ord., sentt., ordd., seguita da un numero e da un anno. Riconosce:
  - la forma semplice: "sentenza n. 120 del 2019";
  - gli elenchi con l'anno detto una volta sola: "sentenze n. 26 e n. 320 del 2007", "nn. 26 e 320 del 2007";
  - gli elenchi con anni o tipi diversi: "sentenze n. 10 del 2015 e n. 20 del 2016";
  - la barra e gli spazi mancanti: "n. 26/2007", "n.4/2008", "sent. 174/1972";
  - le forme antiche con la data: "sentenza 19 giugno 1956, n. 9";
  - "in pari data", per le pronunce depositate lo stesso giorno.
- **Che cosa scarta**, guardando le parole prima della citazione:
  - le ordinanze con cui un giudice porta una questione alla Corte, riconosciute dal numero di registro ("reg. ord.", "r.o.");
  - le decisioni di altre corti (Corte di cassazione, Consiglio di Stato, tribunali amministrativi, Corte dei conti, Corte europea dei diritti dell'uomo, Corte di giustizia);
  - gli atti amministrativi scritti allo stesso modo;
  - le citazioni senza anno.
- **Due parole da distinguere.** Una **menzione** è ogni volta che un numero di pronuncia compare nel testo. Un **legame** (o citazione, nella rete) è la coppia "A cita B", contata una sola volta anche se A nomina B più volte.
- **Che cosa ne è uscito:**

| Voce | Numero |
| --- | --- |
| Menzioni valide in tutto il testo | 155.982 |
| Menzioni scartate dal filtro (altre corti, ordinanze di rimessione, senza anno) | 9.174 |
| Menzioni di pronunce che non esistono o depositate dopo la pronuncia che cita (errori) | 1.950 |
| Menzioni tra pronunce depositate lo stesso giorno, tenute da parte | 268 |
| **Legami distinti nel testo di base** | **93.467**, da 16.944 pronunce |

- **Il controllo del tipo.** Nell'1,3% delle menzioni il tipo scritto (sentenza o ordinanza) non corrisponde al tipo vero della pronuncia citata. Queste citazioni restano nella rete: conta il numero con l'anno, che identifica la pronuncia.
- **Scrive:**
  - `data/processed/citations.csv`: una riga per menzione trovata (pronuncia che cita, pronuncia citata, testo trovato, parte del testo, posizione di inizio e fine);
  - `data/processed/edges_citations.csv`: una riga per legame nel testo di base, con il numero di menzioni;
  - `data/processed/edges_citations_fulltext.csv`: i legami nel testo intero (variante);
  - in `data/interim/`: `citation_errors.csv` (citazioni verso pronunce inesistenti o successive), `citation_excluded.csv` (le menzioni scartate, con il motivo), `citation_same_date.csv` (citazioni tra pronunce dello stesso giorno), `citation_type_mismatch.csv` (tipo scritto diverso dal tipo vero).
- **Controllo automatico:** `tests/test_citations.py` contiene frasi di prova, ognuna con le citazioni che l'estrattore deve trovare o scartare (per esempio "Cass., sez. un., sentenza n. 120 del 2019" va scartata come decisione di un'altra corte).

### 5.6 Controllare l'estrazione

- **Programmi:** `src/validation/sample_passages.py` (sceglie i campioni e mostra i passi da leggere), `src/validation/evaluate.py` (confronta l'estrattore con la lettura di riferimento), `src/validation/human_sheet.py` (prepara il foglio per il controllo di una persona).
- **Che cosa fa.** Si sceglie un campione di pronunce diviso per decennio e tipo; qualcuno legge i testi e scrive quali citazioni ci sono (la lettura di riferimento); il programma confronta l'estrattore con questa lettura e calcola precisione e richiamo. I risultati sono nella sezione 6.1.
- **File:**
  - le letture di riferimento: `data/validation/gold_test.txt` (primo campione) e `gold_test2.txt` (secondo campione), scritte dall'assistente; `gold_human.txt` (da scrivere da una persona);
  - i report: `reports/validation_round1.md` (la prima misura, con l'estrattore prima della correzione: non si può rifare con il codice attuale), `reports/validation_test.md` (il primo campione ricalcolato dopo la correzione), `reports/validation_test2.md` (il secondo campione);
  - il foglio per una persona: `data/validation/human_check.md` (36 pronunce, seme 20261119). Dopo la lettura: `.venv/bin/python src/validation/evaluate.py human`, che scrive `reports/validation_human.md` (oggi non esiste).

### 5.7 Le citazioni scritte nelle massime

- **Programma:** `src/extract/citations_massime.py`.
- **Che cosa fa:** passa allo stesso estrattore i testi delle massime, comprese le note "Precedenti citati: …" scritte dall'Ufficio del massimario.
- **Risultato:** 46.737 coppie; il 95,4% è già nella rete ricavata dal testo di base; le 2.129 coppie in più (il 2,3% della rete) formano la variante "con le citazioni delle massime" (`data/processed/edges_citations_with_notes.csv`, `reports/massime_citations.json`). Le note delle massime non le scrivono i giudici: per questo non entrano nella rete principale.

### 5.8 I giudici, i redattori e i collegi

- **Programma:** `src/judges/build_judges.py`.
- **Legge:** `data/interim/pronunce.pkl` e l'elenco ufficiale dei giudici (`data/raw/giudici/…/Cc_Opendata_AnagraficaGiudici.xml`).
- **Che cosa fa con l'elenco dei giudici:**
  - scarta le 11 righe con più nomi;
  - rende uniformi i nomi (tutto maiuscolo, senza accenti e senza titoli come "prof." o "avv.");
  - corregge due grafie con `NAME_FIX` ("CAIANELLO" diventa "CAIANIELLO", "CAPOLOZZA" diventa "CAPALOZZA"), ma solo per riconoscere i nomi (sezione 11.6);
  - corregge la fine del mandato di Spagnoli al 25/02/1995;
  - per i 33 giudici senza data di fine mandato, la calcola come giuramento più 9 anni (la durata fissata dalla Costituzione, art. 135).
- **Come riconosce un nome** (relatore, redattore): cerca tra i giudici che in quella data potevano essere in carica (dal giuramento, meno 5 giorni, fino a 13 anni dopo, perché i mandati più lunghi sono durati 12 anni) quello il cui cognome corrisponde; se ci sono due giudici con lo stesso cognome (per esempio i due Reale nel 1977), usa anche il nome. Non usa mai la fine del mandato dell'elenco, perché non è affidabile.
- **Da dove prende il nome del redattore:** dal campo `redattore_pronuncia` (dal 2002); altrimenti, dalla 287/1986 in poi, dalle firme in fondo al testo; fino alla 286/1986, dal relatore. La colonna `redattore_source` dice quale delle tre: `field`, `signature`, `relatore_proxy` (oppure `none`, se il nome non c'è).
- **Come ricava il collegio:** tra i giudici che potevano essere in carica in quella data, prende quelli il cui cognome compare nel testo del collegio. Conta anche quanti nomi sono scritti nel testo (`n_listed`), per accorgersi dei nomi non riconosciuti.
- **Quando un collegio è "riconosciuto per intero":** ha tra 11 e 15 giudici riconosciuti, e non meno dei nomi scritti nel testo.
- **Scrive:**
  - `data/processed/judges.csv`: una riga per giudice (identificativo, nome, cognome, organo che l'ha nominato, date, fonte della data di fine, biografia);
  - `data/processed/pronunce_judges.csv`: per ogni pronuncia, il relatore, il redattore o i redattori, la fonte del nome del redattore, quanti giudici ha il collegio riconosciuto, quanti nomi sono scritti nel testo;
  - `data/processed/collegio.csv`: una riga per ogni coppia (pronuncia, giudice che sedeva nel collegio);
  - `data/interim/collegio_errors.csv`: le 257 pronunce con il collegio non riconosciuto per intero, con il motivo e il testo del collegio;
  - `reports/judges_quality.md`: il controllo di qualità (sezione 6.2).
- **Numeri:** il nome del redattore viene dal campo in 8.384 pronunce, dalle firme in 8.349, dal relatore in 5.678; in 16 non c'è. Il programma conta 19 pronunce con più redattori; il campo dei dati ne ha 17, dal 2016: la differenza non è stata controllata.

### 5.9 La materia di ogni pronuncia

- **Programma:** `src/analysis/topics.py` (lento: richiede un calcolo lungo). Con `--labels-only` ricalcola solo i nomi dei temi dal modello salvato.
- **Che cosa fa.** Un modello di temi (LDA, un programma che raggruppa in "temi" le parole che compaiono spesso insieme) legge i testi delle massime:
  - sono lette 46.126 massime, quelle con più di 50 caratteri; le più corte sono rimandi ad altre massime ("Ved. ord. 84/57 B.");
  - il vocabolario ha 8.000 parole, tolte le più comuni e le più rare;
  - il numero di temi è stato scelto con la regola decisa prima: tra 10, 20, 30, 40, 50 e 60, il più piccolo con una coerenza (NPMI, quanto le parole principali di ogni tema compaiono davvero insieme) entro il 2% della migliore. La coerenza è più alta con 20 temi (0,2031), quindi sono **20 temi**;
  - ogni massima riceve un peso per ogni tema; i temi di una pronuncia sono la media dei pesi delle sue massime; la materia principale è il tema con il peso più alto.
- **Controlli:**
  - con i titoli delle massime (dal 2015): accordo 0,313 (informazione mutua normalizzata, da 0 a 1), contro 0,025 con i temi rimescolati a caso;
  - con il primo articolo della Costituzione invocato: 0,177 contro 0,011;
  - stabilità: rifacendo il calcolo da altri 4 semi, i temi più simili hanno in media 0,309 di parole in comune (indice di Jaccard sulle prime 20 parole, da 0 a 1). Ripetendo il calcolo i temi cambiano parecchio: è un limite dichiarato.
- **Pronunce con una materia:** 22.107. Le 320 pronunce senza materia (271 ordinanze e 49 sentenze) sono di due tipi: 266 hanno solo massime di rinvio di 50 caratteri o meno, tutte tra il 1957 e il 2009; 54 non hanno ancora massime, e 51 di queste sono del 2026 (`reports/numbers.json`). Restano fuori da D3.
- **I nomi dei temi:** per ogni tema, la voce dei titoli delle massime (dal 2015) più tipica del tema, solo se copre almeno 15 massime e il 10% del tema; altrimenti il tema resta senza nome (4 temi su 20).
- **Scrive:** `data/processed/topics_theta.npz` (i pesi dei temi per ogni pronuncia), `data/processed/topics_pronunce.csv`, `reports/topics.md`, `reports/topics.json`.
- **Nota:** modificato il 21/11/2026 nella parte che scrive il testo, e non più fatto girare (sezione 11.2).

### 5.10 Gli articoli della Costituzione invocati

- **Programma:** `src/analysis/parametri.py`.
- **Che cosa fa:** per ogni pronuncia raccoglie gli articoli della Costituzione che le sue massime indicano come violati (il parametro, solo la Costituzione, non le leggi costituzionali né gli statuti regionali). Ogni articolo pesa tanto più quanto è raro (peso = logaritmo di N diviso n, con N pronunce con almeno un articolo e n quelle che invocano l'articolo): l'art. 3 (uguaglianza) è invocato nel 64,7% delle pronunce e senza peso renderebbe simili quasi tutte le coppie. L'articolo principale di una pronuncia è quello invocato nel maggior numero delle sue massime.
- **Numeri:** almeno un articolo nel 92,9% delle pronunce con massime; 139 articoli diversi; 2,6 articoli per pronuncia in media.
- **A che cosa serve:** una materia più fine dei 20 temi, usata nelle prove esplorative di D2 e D3 (sezione 9).
- **Scrive:** `data/processed/parametri_pronunce.csv`, `reports/parametri.json`.

### 5.11 Le reti

- **Programma:** `src/networks/build.py`.
- **Che cosa fa:**
  - costruisce la tabella delle pronunce (`data/processed/nodes.csv`): i dati di ogni pronuncia, il redattore, il tipo di giudizio preso dalle massime (incidentale, principale, conflitto tra enti, conflitto tra poteri, referendum, correzione, misto, altro), quante citazioni riceve (`in_deg`) e quante ne fa (`out_deg`);
  - scrive il legame giudice → pronuncia scritta (`data/processed/edges_redazione.csv`);
  - scrive la rete tra giudici (`data/processed/edges_judges.csv`): giudice A → giudice B, con un peso pari al numero di citazioni dalle pronunce scritte da A a quelle scritte da B;
  - calcola le misure di base della rete delle citazioni (`reports/network_basic.json`): numero di nodi e legami, se ci sono cicli, densità, componenti, citazioni fatte e ricevute, età delle citazioni, catena più lunga.
- **Nota:** l'intestazione del programma nomina anche un file `reports/network_basic.md`, che non esiste: il programma scrive solo il file JSON.

### 5.12 La rete dei collegi tra giudici

- **Programma:** `src/networks/cositting.py` (aggiunto il 24/11/2026, su richiesta di Umberto).
- **Legge:** `data/processed/collegio.csv`, `data/processed/nodes.csv`, `data/processed/judges.csv`.
- **Che cosa fa:**
  - due giudici sono collegati se hanno deciso insieme almeno una pronuncia, cioè se sedevano tutti e due nel suo collegio; il **peso** del legame è il numero di pronunce decise insieme. Contano tutte le pronunce dell'archivio, perché sono tutte decisioni pubblicate;
  - la data di una pronuncia è quella della decisione (quella del deposito se la decisione manca);
  - per ogni giudice: la prima e l'ultima presenza in un collegio (il periodo "in attività"), quante pronunce ha deciso, con quanti colleghi, e la sua **forza** (la somma dei pesi dei suoi legami);
  - per ogni coppia: la prima e l'ultima pronuncia decisa insieme; quante pronunce dell'archivio sono state decise mentre erano tutti e due in attività (`n_both_active`); la **quota** = pronunce decise insieme diviso `n_both_active`;
  - un controllo dell'elenco ufficiale: i giudici che compaiono in un collegio dopo la fine del mandato scritta nell'elenco.
- **Scrive:** `data/processed/edges_cositting.csv` (i legami), `data/processed/judges_cositting.csv` (i giudici), `data/processed/cositting_network.graphml` (la stessa rete in un formato che si apre con Gephi o networkx), `reports/cositting_network.json` (descrizione e controlli).
- **Controllo interno:** la somma dei pesi (1.956.971) è uguale al numero di coppie di giudici dentro ogni collegio, sommato su tutte le pronunce.
- **Risultati:** sezione 7.3.

### 5.13 I dati presi con le API

- **Programma:** `src/ingest/fetch_api.py`.
- **Che cosa fa:**
  - dalla banca dati SPARQL della Corte: l'esito di ogni pronuncia dal 2005 (`data/processed/esiti.csv`) e i giudici presenti alle sedute collegate a ogni pronuncia dal 2004 (`data/interim/sedute_membri.csv`);
  - dall'interfaccia di Wikipedia in italiano (MediaWiki): le voci che rimandano a una pronuncia sul sito della Corte o su Consulta Online (`data/processed/wikipedia_links.csv`);
  - la data delle interrogazioni è annotata in `reports/api_fetch.json`.
- **L'esito.** Una pronuncia può decidere più questioni e quindi avere più esiti (6.728 pronunce con esito hanno 8.990 esiti). Si conservano tutte le etichette; nelle analisi conta solo se c'è almeno una dichiarazione di incostituzionalità, sì o no.

### 5.14 D1: le pronunce

- **Programma:** `src/analysis/d1_pronunce.py`, che scrive `reports/d1_results.json` e, in `data/interim/`, le tabelle anno per anno (`d1_yearly.pkl`, `d1_panel_<anno>.pkl`).
- **Che cosa calcola:**
  - quanto sono concentrate le citazioni ricevute (quota dell'1% più citato, indice di Gini, quota di pronunce mai citate, massimo), confrontate con le versioni casuali (sezione 8);
  - la forma della distribuzione delle citazioni: legge di potenza contro lognormale, con il metodo di Clauset, Shalizi e Newman (pacchetto `powerlaw`);
  - l'autorevolezza secondo HITS e PageRank, anno per anno dal 1966 (quando la rete ha 1.000 pronunce), e il confronto con le citazioni; prima sull'insieme di Agnoloni e Pagallo (sentenze in via incidentale fino al 2014), poi sulla rete completa, poi sulle sole sentenze;
  - la previsione delle citazioni dell'anno dopo, con e senza autorevolezza, stimata fino al 2010 e provata sul 2011–2025;
  - D1b: la frequenza di citazione per età del precedente e il tempo fino all'ultima citazione (curva di sopravvivenza di Kaplan–Meier).

### 5.15 D2 e D4: i giudici

- **Programmi:** `src/analysis/d2_d4_giudici.py`, che scrive `reports/d2_results.json`, `reports/d4_results.json` e `data/processed/judges_attributes.csv` (provenienza e organo di nomina di ogni giudice); `src/analysis/d2_strata_check.py`, che scrive `reports/d2_strata_check.json`.
- **D2, che cosa calcola:** per ogni giudice con almeno 30 pronunce scritte, le citazioni ricevute dalle sue pronunce entro 10 anni dal deposito, senza le citazioni da pronunce scritte da lui stesso, divise per le citazioni attese. L'atteso viene da 10.000 rimescolamenti: le pronunce di ogni anno sono riassegnate a caso tra i giudici di quell'anno, e ogni pronuncia porta con sé le citazioni che ha davvero ricevuto. Varianti: stesso anno e tipo; anno, tipo e materia; anno, tipo e articolo principale della Costituzione; solo pronunce dalla 287/1986. Il confronto fissato prima (ogni citazione mandata a caso tra le pronunce dello stesso anno) è ancora calcolato e salvato (voce `nullo_preregistrato`), ma non interpretato. Poi la correzione di Holm sui 113 confronti, e l'accordo tra le classifiche durante e dopo il mandato.
- **D2, il controllo `d2_strata_check.py`:** quanta parte delle pronunce dei giudici studiati sta in gruppi con almeno due redattori diversi (l'86,1%). Una pronuncia sola con il suo redattore nel suo gruppo non si può riassegnare, e avvicina a 1 il rapporto del giudice.
- **D4, che cosa calcola:** la quota di citazioni tra giudici dello stesso gruppo (stessa provenienza, oppure stesso organo di nomina), confrontata con versioni in cui i gruppi sono riassegnati a caso tra giudici entrati nello stesso decennio. Prima, una simulazione della potenza (la probabilità di accorgersi di un effetto del 20%). Il generatore casuale di D4 ha un suo seme (20261120), perché le modifiche a D2 non cambino D4.
- **Come è ricavata la provenienza:** in automatico dalla biografia ufficiale: "professore", "docente" o "ordinario di" → professore; "magistrato", "consigliere", "presidente di sezione" o "procuratore" → magistrato; "avvocato" → avvocato. Nessuno l'ha controllata riga per riga. L'organo di nomina viene dal campo ufficiale `Eletto_da`.

### 5.16 D3: la memoria del collegio (il risultato principale)

- **Programma:** `src/analysis/d3_memoria_collegiale.py`, che scrive `reports/d3_results.json`, `reports/d3_results.md` e `data/interim/d3_mandate.pkl`. Con `--md-only` riscrive `reports/d3_results.md` dai numeri salvati, senza rifare le stime.
- **Il disegno, fissato prima delle stime:**
  1. per ogni pronuncia che cita, scritta da un solo redattore R (le pronunce scritte da più giudici sono escluse), si prendono i precedenti decisi mentre R era in attività (tra la sua prima e la sua ultima presenza in un collegio) e depositati prima della pronuncia che cita;
  2. tra questi: tutti quelli citati nel testo di base, più 50 non citati estratti a caso (seme 20261116);
  3. per ogni precedente si annota: R l'ha scritto (`self_drafted`)? R sedeva nel collegio senza scriverlo (`sat_not_drafted`)? Oppure R era assente (il gruppo di riferimento)? La classe di età del precedente; la somiglianza di materia (somiglianza del coseno tra i temi della pronuncia che cita e quelli del precedente);
  4. il modello (regressione logistica condizionata) confronta, solo dentro la stessa pronuncia che cita, i precedenti citati con quelli non citati, e stima quanto ogni caratteristica cambia la probabilità di essere citato;
  5. l'incertezza tiene conto che le pronunce scritte dallo stesso giudice si somigliano (errori standard raggruppati per redattore).
- **Il calcolo è esatto:** considera tutti i modi in cui la pronuncia poteva scegliere i precedenti che cita tra quelli del suo gruppo. Fino al 17/11/2026 si usava un'approssimazione (di Breslow) che, quando una pronuncia cita molti precedenti, avvicina a 1 gli effetti forti; ora serve solo come punto di partenza e come confronto (voce `or_breslow`). Il risultato coincide con quello di un secondo programma indipendente (statsmodels) sugli stessi dati.
- **Il modello completo (secondario):** usa tutti i precedenti depositati prima, e il gruppo di riferimento è "precedente deciso prima che R arrivasse alla Corte".
- **Le varianti** (sezione 9.4): senza le citazioni di R a pronunce scritte da lui; solo dal 1987; senza gli anni dell'arretrato; testo intero; con le citazioni delle massime; a parità di legge impugnata; a parità di articoli della Costituzione; altri cinque campioni di non citati; sottogruppi (sentenze, ordinanze, fino al 2000, dal 2001).
- **Programmi di controllo:**
  - `src/analysis/d3_absences.py` (scrive `reports/d3_absences.json`): descrive le assenze dal collegio, su cui si regge il risultato principale (sezione 9.4);
  - `src/analysis/d3_full_check.py` (scrive `reports/d3_full_check.json`): spiega il numero 0,88 del modello completo, con prove e regola di lettura decise prima (sezione 9.4).

### 5.17 Le analisi in più

- **`src/analysis/precedent_succession.py`** (scrive `reports/precedent_succession.json`): un precedente dimenticato viene sostituito dalle pronunce che lo hanno citato? Regole decise prima di eseguirlo (registro, 21/11/2026). Esplorativo. Risultati nella sezione 9.3.
- **`src/analysis/extras.py`** (scrive `reports/extras.json` e `data/processed/communities.csv`): i filoni della rete (metodo di Leiden, confrontato con i temi e con un secondo metodo, Infomap); l'esito e le citazioni ricevute; Wikipedia; le quote grezze di autocitazione e di memoria del collegio; il controllo di dove sta l'autorevolezza di HITS (voce `hits_communities`).
- **`src/analysis/course_measures.py`** (scrive `reports/course_measures.json`): le misure dei libri di testo del corso, ognuna con il suo confronto (attaccamento preferenziale, chiusura dei triangoli, correlazioni di grado, piccolo mondo, pronunce ponte, robustezza). Esplorativo, aggiunto il 18/11/2026. Risultati nella sezione 9.7.

### 5.18 Le figure e la rete interattiva

- **`src/analysis/figures.py`** scrive le 10 figure della relazione in `reports/figures/`, seguendo le regole di `docs/project_guide.md`, sezione 3 (un messaggio per figura, assi dei valori dei grafici a barre che partono da zero, colore solo dove porta informazione):

| Figura | Che cosa mostra |
| --- | --- |
| `fig1_pronunce_per_anno.png` | Pronunce depositate ogni anno, per tipo; il picco del 1987–1989 è lo smaltimento delle cause arretrate |
| `fig2_fonte_redattore.png` | Da dove si ricava il nome del redattore, anno per anno |
| `fig3_distribuzione_citazioni.png` | La distribuzione delle citazioni ricevute |
| `fig4_concentrazione_vs_nullo.png` | Concentrazione delle citazioni: dato vero e valore atteso per caso |
| `fig5_invecchiamento.png` | Frequenza di citazione per età del precedente, rispetto a una scelta a caso |
| `fig6_authority_vs_citazioni.png` | Autorevolezza (HITS) contro citazioni |
| `fig7_d3_memoria_collegiale.png` | D3: l'effetto di "sedeva nel collegio senza scriverlo" nel calcolo principale e nelle varianti |
| `fig8_d3_redatto_vs_collegio.png` | D3: "l'ha scritto lui" contro "sedeva nel collegio", con la variante a parità di legge impugnata |
| `fig9_d2_giudici.png` | D2: citazioni ricevute diviso attese, per giudice, con l'intervallo al 95% |
| `fig10_d2_dopo_mandato.png` | D2: il rapporto durante il mandato e nei dieci anni dopo |

- **`src/analysis/interactive.py`** scrive `reports/rete_interattiva.html`: le 400 pronunce più citate e le 2.170 citazioni tra loro, da esplorare in un browser, senza installare nulla (disposizione dei nodi di Fruchterman–Reingold, con seme fisso). La legenda non è stata ricontrollata dopo la riscrittura dei testi (sezione 11.3).

### 5.19 I numeri della relazione e i controlli automatici

- **`src/report/report_numbers.py`** scrive `reports/numbers.json`: i numeri della relazione che nessun programma di analisi salvava (testi non divisi, conteggi delle menzioni, pronunce senza materia, l'ultimo anno, la riduzione dell'effetto "l'ha scritto lui" a parità di legge impugnata).
- **`src/report/plain_intros.py`** aggiunge, o aggiorna, il paragrafo "In breve" in testa a 9 report scritti dai programmi. Per correggere quei paragrafi si corregge questo programma, non i report.
- **`tests/test_report_numbers.py`** confronta i numeri principali della relazione con i file dei risultati: per ogni frase controllata, i numeri devono comparire nella relazione nello stesso ordine e vicini, nella Parte I o nella Parte II. Se un'analisi cambia, il controllo fallisce finché il testo della relazione non viene aggiornato.
- **`tests/test_citations.py`** controlla l'estrattore su frasi di prova (sezione 5.5).
- **Come si lanciano:** `.venv/bin/python -m pytest` (il file `pytest.ini` limita i controlli alla cartella `tests/`). Al 24/11/2026 passano tutti e tre.

### 5.20 La polarità delle citazioni

- **Programmi:** `src/polarity/contexts.py` (per ogni menzione, la frase che la contiene; scrive `data/interim/polarity_contexts.pkl`), `src/polarity/lexicon.py` (le regole), `src/polarity/draw_sample.py` (il campione di prova, già estratto), `src/polarity/evaluate.py` (il confronto con la lettura di riferimento; scrive `reports/polarity_validation_claude.md` e `.json`).
- **Che cosa cerca:** la "distinzione o distacco", cioè le citazioni in cui la Corte dice che il precedente non è pertinente, riguarda un caso diverso, non è un vero precedente, oppure è superato. Il sostegno al precedente è il caso normale e non si cerca.
- **File del campione:** `data/validation/polarity_test_sample.csv` (i passi, senza le decisioni delle regole), `polarity_test_labels.csv` (le decisioni delle regole), `gold_polarity_claude.txt` (la lettura dell'assistente), `polarity_human_check.md` e `gold_polarity_human.txt` (il foglio e il file per una persona).
- **Risultato:** sezione 9.8.

### 5.21 Le altre corti (solo impostato)

- **Documento:** `docs/context_corti.md`: che cosa fanno la Corte di cassazione, il Consiglio di Stato, la Corte europea dei diritti dell'uomo e la Corte di giustizia dell'Unione europea, chi decide, come si riconosce una decisione, che dati pubblicano e se si possono riusare.
- **`src/courts/sizing.py`** (scrive `reports/courts_sizing.json` e `data/interim/courts_split.csv`): conta quante pronunce nominano ciascuna corte e divide le pronunce a caso in due metà (seme 20261123): una per scrivere le regole (sviluppo), una per il controllo finale (prova).
- **`src/courts/mentions.py`**: registra ogni volta che la Corte nomina un'altra corte, con il ruolo (citazione, corte che ha sollevato la questione, domanda alla Corte di giustizia, altro). Le regole sono alla versione 2, non definitive; finché non lo sono, il programma si rifiuta di leggere la metà di prova. Scrive `data/interim/courts_mentions_<metà>.csv` e, con `--sheet`, `data/interim/courts_dev_sheet.md`.
- **Pronunce che nominano ciascuna corte nel testo di base:** Corte di cassazione 3.175; Consiglio di Stato 1.058; Corte di giustizia 472; Corte europea dei diritti dell'uomo 408 (`reports/courts_sizing.json`). Nominare una corte non vuol dire citare una sua decisione: molte volte il riferimento è generico, oppure la corte nominata è quella che ha sollevato la questione.
- **Che cosa si potrà costruire:** con dati aperti solo il verso "la Corte costituzionale cita le altre corti"; il verso opposto, in principio, solo per la Corte di giustizia.

## 6. I controlli di qualità

Il quadro completo, scritto a mano, è in `reports/validation.md`. Le soglie sono state fissate prima dei risultati (sezione 4.1).

### 6.1 Le citazioni estratte dai testi

**Che cosa si misura.**

- La **precisione**: delle citazioni trovate dall'estrattore, quante sono vere. Se ne trova 100 e 95 sono vere, la precisione è 0,95.
- Il **richiamo**: delle citazioni vere, quante ne trova. Se nel testo ce ne sono 100 e ne trova 90, il richiamo è 0,90.
- L'unità contata è la coppia "pronuncia che cita – pronuncia citata" nel testo di base. Tra parentesi c'è l'intervallo di confidenza al 95% (metodo di Wilson).

**Chi ha deciso quali citazioni sono vere.** L'assistente (Claude), non una persona. Ha letto i testi prima di far girare l'estrattore su quei campioni, ma solo i passi con una parola chiave (come "sentenza" o "ordinanza") o un rimando, non i testi interi. È il punto debole di tutta la misura: le parole chiave somigliano a quelle dell'estrattore, quindi una forma di citazione che nessuno dei due riconosce sfuggirebbe a entrambi, e il richiamo risulterebbe più alto del vero.

| Passo | Campione | Pronunce | Citazioni vere | Precisione | Richiamo | File |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Primo campione, tutti i decenni (seme 20261117) | 64 | 270 | 1,000 (0,985–1,000) | 0,941 (0,906–0,963) | `reports/validation_round1.md` |
| 1 | di cui fino alla pronuncia 286/1986 | 27 | 40 | 1,000 (0,886–1,000) | **0,750** (0,598–0,858): sotto la soglia | `reports/validation_round1.md` |
| 1 | di cui dal 1987 | 37 | 230 | 1,000 (0,983–1,000) | 0,974 (0,944–0,988) | `reports/validation_round1.md` |
| 2 | L'estrattore è stato corretto per le forme antiche di citazione ("12/1957" senza "n.", elenchi con più date, "in pari data", i due punti come separatore) | | | | | `src/extract/citations.py` |
| 3 | Secondo campione, mai visto prima, solo fino alla 286/1986 | 48 | 72 | 0,985 (0,920–0,997) | 0,917 (0,830–0,961) | `reports/validation_test2.md` |

**Come si legge.**

- Le stime da usare sono due: dal 1987, richiamo 0,974 (passo 1); fino al 1986, richiamo 0,917 (passo 3). La precisione è almeno 0,985 in tutti e due i periodi.
- Come previsto dalle regole, dopo il primo campione il lavoro si è fermato: l'estrattore è stato corretto e poi verificato su un secondo campione mai visto.
- Per i testi fino al 1986 il valore stimato supera la soglia di 0,90, ma il limite inferiore dell'intervallo (0,830) no: con 72 citazioni non si può escludere che il richiamo vero sia sotto la soglia.
- Le citazioni controllate sono 342 (270 + 72), meno delle 460 previste: gli intervalli sono più larghi del previsto.
- `reports/validation_test.md` ricalcola il primo campione dopo la correzione (richiamo 0,978). Non è una stima indipendente, perché la correzione è stata scritta guardando proprio quel campione: serve solo a controllare che la correzione non abbia rotto altro.

**Il controllo di una persona, ancora da fare.** `data/validation/human_check.md` contiene 36 pronunce mai usate (seme 20261119), con tutto il testo di base e senza il risultato dell'estrattore: circa 100 citazioni attese. Una persona scrive le citazioni che trova in `data/validation/gold_human.txt` (istruzioni in testa al foglio); poi `.venv/bin/python src/validation/evaluate.py human` calcola precisione e richiamo. Secondo la regola del 19/11/2026, questa lettura diventa il riferimento per le soglie. Con circa 100 citazioni il controllo può smentire le soglie, ma non confermarle con sicurezza: il limite inferiore dell'intervallo supera 0,95 solo con 100 citazioni giuste su 100, e 0,90 solo con almeno 97 su 100. Se una soglia non è raggiunta: i risultati che dipendono dalla rete delle citazioni si dichiarano provvisori, l'estrattore si corregge, e si ricontrolla una sola volta su un nuovo campione.

### 6.2 I giudici: chi ha scritto e chi sedeva nel collegio

Da `reports/judges_quality.md` (scritto da `src/judges/build_judges.py`).

| Controllo | Risultato | Soglia decisa prima |
| --- | --- | --- |
| Pronunce con il nome del redattore collegato all'elenco dei giudici | 99,84% | 98% |
| Pronunce con il collegio riconosciuto per intero (da 11 a 15 giudici, tutti collegati all'elenco, non meno dei nomi scritti nel testo) | 98,85% | 98% |
| Pronunce con il nome del relatore collegato all'elenco | 99,95% | — |

- Le 257 pronunce con il collegio non riconosciuto per intero sono in `data/interim/collegio_errors.csv` (sezione 11.7).
- Per decennio, il collegio è riconosciuto per intero dal 95,0% (anni 1970) al 100,0% (anni 2010 e 2020).
- Giudici da controllare: Giuseppe Lampis e Giuseppe Capograssi non compaiono in nessun collegio; per Nicola Reale e Giuseppe Frigo l'ultima presenza in un collegio è più di 400 giorni prima della fine del mandato; gli altri della lista sono ancora in carica.

### 6.3 Il confronto con la banca dati SPARQL della Corte

| Controllo | Risultato | File |
| --- | --- | --- |
| Relatore: file contro banca dati, 22.426 pronunce | Coincide nel 97,12%; 635 delle 645 differenze sono i due errori di grafia, corretti nel programma | `reports/sparql_reconciliation.md` |
| Collegio ricavato dal testo contro giudici presenti alla seduta, 3.684 pronunce dal 2004 | Il 97,8% dei giudici del collegio risulta presente alla seduta; il 99,1% dei presenti alla seduta risulta nel collegio; i due elenchi sono identici nel 73,5% delle pronunce | `reports/collegio_vs_sedute.json` (nessun programma lo scrive: sezione 11.1) |

Collegio e seduta non devono coincidere sempre: in una seduta si discutono più cause, e un giudice può non partecipare a tutte. Per questo conta la quota di giudici in comune, non la quota di elenchi identici. `reports/validation.md` attribuisce il file `collegio_vs_sedute.json` al programma `src/ingest/fetch_api.py`, ma quel programma scrive solo `data/interim/sedute_membri.csv`, cioè i dati da cui il confronto si calcola.

### 6.4 La polarità delle citazioni

La soglia era una precisione di almeno 0,80; il risultato è 0,76 (28 su 37), sotto la soglia. Dettagli nella sezione 9.8.

## 7. Le reti

### 7.1 Che cosa è una rete, e le reti del progetto

Una rete è fatta di **nodi** (le cose) e **legami** (le relazioni tra le cose). Un legame può avere un **verso** (da A a B) e un **peso** (un numero, per esempio quante volte succede).

| Rete | Nodi | Legame | Verso | Peso | File |
| --- | --- | --- | --- | --- | --- |
| Citazioni | Pronunce | A cita B nel testo di base | Da chi cita a chi è citato, sempre verso il passato | Nessuno: una coppia conta una volta | `data/processed/edges_citations.csv` |
| Redazione | Giudici e pronunce | Il giudice ha scritto la pronuncia | — | — | `data/processed/edges_redazione.csv` |
| Collegio | Giudici e pronunce | Il giudice sedeva nel collegio | — | — | `data/processed/collegio.csv` |
| Influenza tra giudici | Giudici | Le pronunce scritte da A citano pronunce scritte da B | Da A a B | Numero di citazioni | `data/processed/edges_judges.csv` |
| Collegio tra giudici | Giudici | A e B hanno deciso insieme almeno una pronuncia | Nessuno | Numero di pronunce decise insieme | `data/processed/edges_cositting.csv` |

Le reti "Redazione" e "Collegio" hanno due tipi di nodi (giudici e pronunce): in questi casi un legame va sempre da un nodo di un tipo a un nodo dell'altro tipo. Le due reti tra giudici si ricavano da queste: la rete "Collegio tra giudici" è la **proiezione** della rete "Collegio" sui giudici (due giudici sono collegati se hanno una pronuncia in comune). In termini dei libri di testo, i collegi sono una **rete di affiliazione**: persone legate agli eventi a cui partecipano (Easley e Kleinberg, capitolo 4).

### 7.2 La rete delle citazioni in numeri

Da `reports/network_basic.json` (scritto da `src/networks/build.py`).

- **22.427 pronunce, 93.467 citazioni, nessun ciclo.** "Nessun ciclo" vuol dire che seguendo le citazioni non si torna mai al punto di partenza: una pronuncia cita solo pronunce più vecchie.
- **La rete è rada.** Ogni pronuncia cita in media 4,2 precedenti. La densità (legami presenti diviso legami possibili verso il passato) è 0,00037, cioè lo 0,037%.
- **Quasi tutto è collegato.** L'86% delle pronunce forma un unico blocco (in cui da ogni pronuncia si arriva a ogni altra seguendo le citazioni in un senso o nell'altro); 2.629 pronunce (12%) non citano nulla e non sono mai citate.
- **Sentenze e ordinanze sono citate in modo molto diverso.** Una sentenza riceve in media 6,4 citazioni, un'ordinanza 1,7.
- **Si cita sempre di più.** Negli anni Cinquanta una pronuncia citava in media 1 precedente; negli anni Venti di questo secolo 14,7.
- **Si cita il recente.** Metà delle citazioni va a precedenti con meno di 3,5 anni; il 9% a precedenti con più di 20 anni.
- **La catena più lunga** di pronunce che si citano una dopo l'altra ha 148 anelli.
- **Le misure che su questa rete non hanno senso** (`.claude/rules/network-analysis.md`): la reciprocità (quante citazioni vanno nei due sensi), che è zero per costruzione; i gruppi che si raggiungono a vicenda seguendo il verso, perché senza cicli ogni pronuncia fa gruppo a sé; la chiusura dei triangoli sulla rete con il verso, che si calcola invece sulla rete senza verso.

### 7.3 La rete dei collegi tra giudici in numeri

Da `reports/cositting_network.json` (scritto da `src/networks/cositting.py`). Etichetta: descrittivo.

- **Nodi e legami.** 123 giudici (i 125 dell'elenco meno Lampis e Capograssi, che non compaiono in nessun collegio) e 1.541 legami, su 7.503 coppie possibili.
- **Sull'intero periodo la rete è poco fitta:** esiste il 20,5% dei legami possibili, perché un giudice degli anni Cinquanta non ha mai incontrato un giudice di oggi.
- **Negli stessi anni è quasi completa.** Le coppie di giudici in attività negli stessi anni sono 1.548; di queste, 1.541 hanno deciso insieme almeno una pronuncia. Le altre 7 si sono sovrapposte per poco (da 14 a 52 pronunce decise nel periodo comune).
- **Il peso** (pronunce decise insieme) va da 1 a 5.081; la mediana è 999. Il peso dice soprattutto per quanto tempo due giudici sono stati in attività insieme. La coppia con il peso più alto è Enzo Cheli e Luigi Mengoni: 5.081 pronunce insieme su 5.476 decise mentre erano tutti e due in attività.
- **La quota** (pronunce decise insieme diviso pronunce decise mentre erano tutti e due in attività) ha mediana 89,3%: in una coppia tipica i due giudici siedono insieme quasi 9 volte su 10. È il rovescio delle assenze, su cui si regge D3.
- **Ogni giudice** ha da 14 a 34 colleghi, 26 in mediana.
- **Perché la rete serve solo a descrivere.** Negli stessi anni tutti siedono con quasi tutti: un test su questa rete direbbe soprattutto chi era in attività insieme. La regola di metodo vieta quindi i test su questa rete. La rete serve a descrivere, a controllare i dati (sezioni 11.5 e 11.7) e a controllare le occasioni di citare.
- **Come aprirla.** `data/processed/cositting_network.graphml` si apre con Gephi o con networkx (`networkx.read_graphml`); in alternativa, `edges_cositting.csv` (i legami) e `judges_cositting.csv` (i giudici).

## 8. Come si decide che un risultato non è dovuto al caso

### 8.1 Il principio

Un numero da solo non dice se qualcosa è tanto o poco. Per esempio: l'1% delle pronunce più citate raccoglie il 10% delle citazioni. È tanto? Dipende da quanto ne raccoglierebbe se le citazioni andassero a caso. Per saperlo si costruiscono molte versioni rimescolate dei dati (i **modelli nulli**). Ogni versione conserva ciò che è ovvio (per esempio quante citazioni fa ogni pronuncia e quanto sono vecchi i precedenti che cita) e mescola a caso il resto. Se il dato vero sta fuori dall'intervallo delle versioni rimescolate, c'è qualcosa che il caso non spiega.

Le versioni rimescolate sono 1.000 (10.000 per i giudici di D2, 100 per alcune misure secondarie), sempre con lo stesso seme. Il tempo va sempre rispettato: una pronuncia può citare solo pronunce già depositate. Un rimescolamento che ignorasse il tempo darebbe confronti falsi.

### 8.2 Un confronto per ogni domanda

| Domanda | Che cosa si misura | Con che cosa si confronta |
| --- | --- | --- |
| D1: le citazioni sono concentrate? | Quota delle citazioni che va all'1% più citato; quota di pronunce mai citate; indice di Gini (da 0, tutte uguali, a 1, tutto a una sola) | Ogni citazione resta alla pronuncia che cita, ma va a una pronuncia presa a caso tra quelle depositate nello stesso anno del precedente vero (variante aggiunta dopo: stesso anno e stesso tipo). Le citazioni ricevute non si conservano, perché sono proprio ciò che si misura |
| D1: che forma ha la distribuzione? | Legge di potenza contro lognormale, metodo di Clauset, Shalizi e Newman | Un test statistico tra le due forme (rapporto di verosimiglianza) |
| D1: le pronunce "autorevoli" sono le più citate? | HITS e PageRank; quante pronunce stanno nell'1% più alto di entrambe le classifiche | Citazioni scambiate tra coppie con gli stessi anni (alla Uzzi): conservano quante citazioni fa e riceve ogni pronuncia e l'età delle citazioni. Uno scambio è ammesso solo se ogni pronuncia citata resta depositata prima, o lo stesso giorno, della pronuncia che la cita |
| D1: l'autorevolezza aiuta a prevedere? | Previsione delle citazioni dell'anno dopo, stimata fino al 2010 e provata sul 2011–2025 | Lo stesso modello senza autorevolezza; criterio fissato prima: almeno il 2% di errore in meno, con un intervallo al 95% che esclude lo zero |
| D1b: quanto dura un precedente? | Frequenza di citazione per età del precedente; tempo fino all'ultima citazione | Una scelta a caso tra tutti i precedenti disponibili, senza badare all'età |
| D2: le pronunce di un giudice sono più citate? | Citazioni ricevute diviso citazioni attese, senza le citazioni del giudice a sé stesso | Le pronunce di ogni anno riassegnate a caso tra i giudici di quell'anno (10.000 volte); correzione di Holm sui 113 confronti |
| D3: conta aver partecipato o aver scritto? | Regressione logistica condizionata | Dentro ogni pronuncia che cita: i precedenti citati contro 50 non citati estratti a caso |
| D4: ci si cita tra giudici simili? | Quota di citazioni tra giudici dello stesso gruppo | I gruppi riassegnati a caso tra giudici entrati nello stesso decennio |

### 8.3 Molti confronti insieme: la correzione di Holm

Quando si fanno molti confronti insieme (in D2, uno per ognuno dei 113 giudici), alcuni risultano "diversi" per puro caso. La correzione di Holm alza l'asticella in modo che la probabilità anche di un solo falso allarme resti sotto il 5%.

### 8.4 La potenza

La potenza è la probabilità di accorgersi di un effetto della grandezza cercata, se l'effetto esiste. Per D4 si è calcolata prima del test, con una simulazione: si inserisce l'effetto minimo d'interesse (20%) nei dati rimescolati e si conta quante volte il test lo trova. Il test si fa solo se la potenza è almeno 0,80.

## 9. I risultati, uno per uno

### 9.1 D1: le citazioni sono concentrate (secondario)

Da `reports/d1_results.json`. Tra parentesi l'intervallo in cui cadono 95 versioni casuali su 100.

| Misura | Dato vero | A caso, stesso anno (deciso prima) | A caso, stesso anno e tipo (aggiunto dopo) |
| --- | --- | --- | --- |
| Quota delle citazioni che va all'1% delle pronunce più citate | 10,3% | 3,4% (3,4–3,5) | 4,2% (4,1–4,2) |
| Indice di Gini | 0,66 | 0,37 (0,37–0,37) | 0,48 (0,48–0,48) |
| Pronunce mai citate | 29,5% | 4,3% (4,1–4,5) | 12,8% (12,5–13,0) |
| Citazioni ricevute dalla pronuncia più citata | 113 | 21 (18–23) | 25 (22–28) |

- **Come si legge.** In ogni riga il dato vero è molto lontano da tutte e due le versioni casuali. Una parte della differenza viene dal tipo di pronuncia: non è mai citato il 45,7% delle ordinanze e il 14,8% delle sentenze. Con il secondo confronto il divario si riduce, ma resta grande.
- **Avvertenza.** Quasi tutte le reti di citazioni battono un confronto di questo tipo: la concentrazione in sé è un fatto atteso. Chiamarla "gerarchia" è un'interpretazione, non una prova.
- **Le pronunce più citate** sono la 303/2003, la 401/2007 e la 383/2005: tutte di giudizi in via principale, dopo la riforma costituzionale del 2001.
- **Non è una legge di potenza** (esplorativo). Una legge di potenza è una forma matematica in cui pochissimi casi sono enormi e gli altri piccolissimi, con una regola precisa che lega le due cose. Il test dice che un'altra forma, la lognormale, descrive meglio le pronunce molto citate (rapporto di verosimiglianza −7,5, p < 0,001; esponente stimato 2,92 da 10 citazioni in su). Agnoloni e Pagallo (2016, pp. 142–143) avevano proposto una legge di potenza (esponente 2,414) guardando un grafico, senza test, su una rete diversa (le sole pronunce in via incidentale, 16.320 nodi).
- **Le pronunce "più autorevoli" non sono le più citate** (esplorativo). HITS dà a ogni pronuncia un punteggio di autorevolezza (authority), alto se la pronuncia è citata da pronunce che citano molti precedenti autorevoli. Sulla rete completa l'1% più autorevole e l'1% più citato hanno in comune il 41,5% delle pronunce, contro il 55,7% (53,1–58,0) atteso con le citazioni scambiate. Ma il motivo non è che "conta chi ti cita": HITS concentra l'autorevolezza in un solo gruppo di pronunce molto collegate (il 95,1% dell'1% più autorevole sta in un gruppo di 2.045 pronunce, anno mediano 2013, che raccoglie il 91,6% dell'autorevolezza totale), mentre l'1% più citato è sparso in 22 gruppi (`reports/extras.json`). Le versioni scambiate cancellano i gruppi: il confronto misura soprattutto che i gruppi esistono. PageRank fa l'opposto e premia le pronunce antiche (anno mediano 1970 nel suo 1% più alto). Un terzo delle pronunce ha autorevolezza zero.
- **La verifica del lavoro di Agnoloni e Pagallo non riesce.** Loro scrivono che le prime 30 pronunce per citazioni sono le stesse prime 30 per autorevolezza. Sul loro insieme (sentenze in via incidentale fino al 2014: 6.561 pronunce) qui solo 4 delle prime 30 per autorevolezza sono tra le prime 30 per citazioni. Il loro insieme non è identico e il loro calcolo non è descritto; nella loro tabella 5 (p. 144) pronunce con lo stesso numero di citazioni hanno la stessa autorevolezza, segno che la loro misura coincideva con il numero di citazioni.
- **L'autorevolezza non aiuta a prevedere.** Aggiungerla al modello che prevede le citazioni dell'anno dopo aumenta l'errore di previsione dello 0,27% (0,10–0,42), invece di ridurlo di almeno il 2% come chiedeva il criterio deciso prima.
- **I filoni** (esplorativo, `reports/extras.json`). Il metodo di Leiden (che cerca gruppi di pronunce collegate più tra loro che con il resto) trova 34 gruppi con almeno 50 pronunce, che coprono l'86% dei nodi. La modularità (quanto la divisione è netta) è 0,68, contro 0,29 (0,287–0,292) in 100 reti rimescolate. I gruppi seguono in parte la materia: accordo con i temi 0,22, contro 0,006 del caso. Con un secondo metodo (Infomap) i gruppi sono 63 con almeno 50 pronunce e coprono il 28% dei nodi; l'accordo tra i due metodi è 0,71.

### 9.2 D1b: quanto dura un precedente (secondario)

- **Il picco è a un anno.** La frequenza di citazione è massima a un anno dal deposito (5,8 volte quella di una scelta a caso tra tutti i precedenti disponibili), si dimezza in 3 anni e scende sotto la scelta a caso dopo 9.
- **La vita di una pronuncia.** Per metà delle pronunce, l'ultima citazione arriva entro 6 anni dal deposito: 19 anni per le sentenze, 1 per le ordinanze. Una pronuncia si considera "uscita di scena" se passano 10 anni dall'ultima citazione senza che ne arrivino altre (curva di sopravvivenza di Kaplan–Meier, che tiene conto delle pronunce troppo recenti per saperlo).
- **Un nucleo che resta.** Il 13,4% delle pronunce con almeno trent'anni è citato ancora dopo trent'anni.

### 9.3 Dimenticato o sostituito? (esplorativo)

Da `reports/precedent_succession.json` (`src/analysis/precedent_succession.py`); regole decise prima di eseguire il programma.

- **Che cosa si è fatto.** Si sono presi 1.606 precedenti depositati tra il 1970 e il 2010 e citati almeno 5 volte entro 4 anni dal deposito. Per ognuno: le pronunce che lo hanno citato entro 4 anni (i "successori", 13.340 in tutto) e, per ciascuna, una pronuncia simile (stesso anno, stesso tipo, stesso tema principale) che non lo ha citato. Poi si contano le citazioni ricevute quando il precedente ha tra 4 e 15 anni, solo da pronunce che non citano il precedente.
- **Risultato.** I successori ricevono 1,43 volte le citazioni delle pronunce simili (intervallo 1,37–1,49): il 43% in più. Secondo la regola decisa prima, la sostituzione è "sostenuta".
- **Cautele.** Il risultato è coerente con un passaggio di testimone, ma anche con un'altra spiegazione: le pronunce che citano precedenti importanti sono importanti di loro. I dati non distinguono le due letture. La seconda condizione della regola (i successori, tutti insieme, più citati del precedente: 36,7 contro 4,7 in media) vale anche per le pronunce simili (25,7), quindi non distingue nulla.

### 9.4 D3: il risultato principale

Da `reports/d3_results.json` e `reports/d3_results.md`.

**La misura: l'odds ratio.** Gli odds di essere citato sono la probabilità di essere citato divisa per quella di non esserlo (20% diventa 0,25). L'odds ratio dice quante volte gli odds sono più alti in un gruppo che nell'altro: vale 1 se non c'è differenza, 2 se sono doppi, 0,5 se sono la metà.

| Precedente, rispetto a uno deciso mentre il giudice era assente | Odds ratio | Intervallo al 95% | Valore p | Etichetta |
| --- | --- | --- | --- | --- |
| Deciso da un collegio in cui il giudice sedeva, senza scriverlo | **1,00** | 0,92–1,09 | 1,00 | **Principale** |
| Scritto dal giudice stesso | 5,47 | 4,76–6,27 | < 0,001 | Esplorativo |

- **Su che cosa si regge.** 13.654 pronunce che citano, 46.969 citazioni, di cui 1.658 a precedenti decisi in assenza del giudice che scrive; 122 giudici. Restano fuori le 320 pronunce senza materia.
- **Come si legge.** Aver partecipato alla decisione di un precedente non lo rende più citato da quel giudice: la differenza misurata è zero, e i dati escludono effetti superiori al 9% circa in più o all'8% in meno. Non dimostrano che l'effetto sia esattamente zero. L'idea di partenza ("un precedente circola attraverso le persone che lo hanno deciso") non trova sostegno; ne resta una più stretta: un precedente circola attraverso chi lo ha scritto.

**Le assenze, su cui si regge il risultato** (descrittivo, `reports/d3_absences.json`).

- Su 327.252 coppie giudice–pronuncia decisa mentre il giudice era in attività, il giudice manca nel 6,3% dei casi.
- La quota cambia poco con il tipo di giudizio (dal 3,9% dei referendum al 6,6% dei giudizi in via incidentale), con l'articolo della Costituzione più invocato (dal 5,0% al 7,0% tra i dieci più frequenti) e con la materia (dal 3,9% al 7,3%); di più con il decennio (dal 3,4% degli anni 2020 al 7,2% degli anni 1980 e 1990). La V di Cramér (quanto la presenza dipende da queste categorie, da 0 a 1) vale al massimo 0,049: pochissimo.
- I precedenti non citati decisi con il giudice presente e quelli decisi in sua assenza si somigliano: la differenza più grande, in unità di variabilità, è 0,097, per l'età (2,35 anni in media contro 2,54).
- Le assenze non sono collegi letti male: solo lo 0,6% dei precedenti decisi in assenza del giudice ha un collegio con meno di 11 giudici riconosciuti.
- Non dipendono da pochi giudici: 106 dei 122 giudici citano almeno un precedente deciso in loro assenza; i cinque che ne citano di più raccolgono il 21% di queste citazioni.
- Dal confronto con i presenti alle sedute (dal 2004), al massimo il 13,5% delle assenze potrebbe essere una presenza non riconosciuta: un effetto vero del +10% apparirebbe come +8,5%. Non basta a spiegare un risultato pari a zero.
- Il motivo delle singole assenze non è registrato: non si può escludere un legame tra il motivo di un'assenza e la tendenza a citare quel precedente.

**Le varianti: il risultato principale non si muove** (Figura 7).

| Variante | "Sedeva nel collegio" |
| --- | --- |
| Senza le citazioni del giudice a pronunce scritte da lui | 0,99 (0,91–1,08) |
| Solo dal 1987, dove il redattore è noto davvero | 1,01 (0,93–1,10) |
| Senza gli anni dell'arretrato (pronunce che citano del 1987–1989 escluse) | 1,04 (0,96–1,13) |
| Testo intero, anche il «Ritenuto in fatto» | 0,99 (0,90–1,09) |
| Con le citazioni delle massime | 0,99 (0,91–1,08) |
| A parità di legge impugnata (esplorativo) | 0,99 (0,91–1,07) |
| A parità di articoli della Costituzione invocati (esplorativo) | 0,99 (0,91–1,08) |
| Altri cinque campioni di precedenti non citati | tra 0,98 e 1,01 |

**Perché chi scrive conta tanto: la cautela sul 5,47** (esplorativo).

- I relatori li sceglie il Presidente, con criteri non pubblici. Due spiegazioni non si escludono: un giudice che segue sempre la stessa materia cita i propri precedenti perché sono quelli pertinenti; le questioni ripetute (la stessa legge portata alla Corte da più giudici) possono andare allo stesso relatore, che poi richiama la propria decisione.
- L'effetto è più forte nelle ordinanze (9,83) che nelle sentenze (3,53), e prima del 2001 (8,74) che dopo (3,64): è l'andamento atteso dalle questioni ripetute, spesso chiuse con un'ordinanza.
- **La prova delle questioni ripetute.** Il 40,0% dei precedenti scritti dallo stesso giudice e citati riguarda la stessa legge impugnata della pronuncia che cita, contro il 7,8% dei precedenti decisi in collegi in cui sedeva e il 9,8% di quelli decisi in sua assenza. A parità di legge e articolo impugnati, "l'ha scritto lui" scende da 5,47 a 3,27 (2,95–3,63), mentre "sedeva nel collegio" resta 0,99 (0,91–1,07). La parte che supera 1 passa da 4,47 a 2,27 (si riduce del 49%); sulla scala dei logaritmi, quella del modello, si riduce del 30%. Il 3,27 che resta può essere preferenza personale, specializzazione per materia o legami tra questioni che le massime non registrano: è il valore massimo possibile dell'effetto "personale".
- **La materia più fine.** A parità di articoli della Costituzione invocati, "l'ha scritto lui" scende a 4,78 (4,18–5,47): la materia ne spiega una piccola parte.

**Il secondo confronto, con la data di arrivo del giudice** (secondario, `reports/d3_full_check.json`).

- Qui i precedenti decisi mentre il giudice era in attività si confrontano con quelli della stessa età decisi prima che arrivasse alla Corte. I primi sono citati meno, sia quando il giudice sedeva nel collegio (0,88; 0,80–0,96) sia quando era assente (0,88; 0,77–1,01). Il rapporto tra presenza e assenza è 0,99 (0,88–1,11): presenza e assenza, di nuovo, non differiscono.
- **Da dove viene lo 0,88** (esplorativo, con prove e regola di lettura decise prima). Non dipende da come si misura l'età (con classi di tre mesi: 0,87). È più marcato nelle pronunce che citano fino al 2000 (0,80) e nelle ordinanze (0,78), ma la differenza tra gruppi non è stata provata. Tenendo conto della stessa legge impugnata e degli articoli invocati sale a 0,98 (0,89–1,07): secondo la regola decisa prima, lo 0,88 si attribuisce alle questioni in comune. Con altri due campioni di non citati: 0,86 e 0,90. Lo 0,88 non tocca il risultato principale.

### 9.5 D2: i singoli giudici (esplorativo)

Da `reports/d2_results.json`.

- **Pochi giudici si distinguono.** Su 113 giudici con almeno 30 pronunce scritte, dopo la correzione di Holm le pronunce di 6 sono citate più dell'atteso e quelle di 7 meno (Figura 9).
- **Ma le differenze ci sono.** Nel complesso i giudici differiscono tra loro più di quanto farebbero per caso: la variabilità dei rapporti è 3,0 volte quella attesa (p < 0,001).
- **I primi tre:** Baldassarre (1,88; intervallo 1,60–2,17), Onida (1,61; 1,28–1,99), De Siervo (1,48; 1,21–1,80).
- **Tenendo conto di altro, i giudici che si distinguono diminuiscono:** con anche il tipo di pronuncia, 2 sopra e 4 sotto; con anche la materia, 1 e 3; con anche l'articolo principale della Costituzione, 0 e 3. Con le sole pronunce dalla 287/1986, 7 e 7 su 74 giudici.
- **Dopo il mandato** (87 giudici usciti entro il 2015): l'accordo tra la classifica durante il mandato e quella dei dieci anni dopo (correlazione tra ranghi, da −1 a 1) è 0,66, contro 0,37 (0,16–0,55) con pronunce prese a caso dello stesso anno; tenendo conto anche di tipo e materia, 0,62 contro 0,32 (0,12–0,51). Con l'articolo della Costituzione, invece, 0,42, dentro l'atteso (0,32; 0,11–0,51). Se il peso di un giudice duri dopo il mandato resta incerto.
- **Perché è esplorativo.** Il confronto deciso prima (ogni citazione mandata a caso tra le pronunce dello stesso anno) ignora quanto diversamente sono citate le singole pronunce: con quel confronto i giudici fuori dall'atteso erano 22 e 26, con una variabilità 15 volte quella del caso, un risultato gonfiato. Cambiare confronto dopo aver visto i risultati rende D2 esplorativo. Tutti e due i confronti restano nel file dei risultati.

### 9.6 D4: ci si cita tra giudici simili? Poco

Da `reports/d4_results.json`. La potenza calcolata prima è 1,00 per tutti e due i confronti, quindi il test si poteva fare.

- **Organo di nomina** (Presidente della Repubblica, Parlamento, magistrature): le citazioni tra giudici nominati dallo stesso organo sono il 32,4%, contro il 31,6% atteso (30,7–32,7); p = 0,074, anche dopo la correzione di Holm. Nessun effetto.
- **Provenienza** (professori, magistrati; gli avvocati sono solo 3): 48,4% contro 46,1% (44,4–48,0); p = 0,011, 0,022 con la correzione di Holm. L'eccesso è del 4,9%: reale ma piccolo, molto sotto il 20% fissato come soglia d'interesse.

### 9.7 Gli altri risultati

**Con le API** (`reports/extras.json`):

- **Esito.** Tra le pronunce del 2006–2015, quelle che dichiarano incostituzionale una legge ricevono in dieci anni 10,9 citazioni in media, le altre 4,0: 2,7 volte tanto (2,5–2,9). Tra le sole sentenze, 1,6 volte (1,4–1,7).
- **Wikipedia** (descrittivo). L'1,3% delle pronunce è citato in una voce di Wikipedia; tra l'1% più autorevole secondo HITS l'8,5%, tra l'1% più citato il 10,7%.

**Le misure dei libri di testo del corso** (esplorative, `reports/course_measures.json`):

- **Chi è ricco diventa più ricco** (attaccamento preferenziale): confrontando ogni pronuncia con quelle dello stesso anno, le citazioni nuove crescono con quelle già ricevute come (1 + citazioni)^a, con a = 1,12 (1,11–1,14): un po' più che in proporzione. È un valore massimo, perché una pronuncia può essere molto citata perché è importante di suo.
- **Chiusura dei triangoli** (transitività, sulla rete senza verso): 0,151, contro 0,009 (0,008–0,009) nelle reti rimescolate; clustering locale medio 0,241 contro 0,005.
- **Correlazioni di grado:** le pronunce molto citate citano pronunce molto citate (0,201 contro 0,076); le pronunce che citano molto citano precedenti molto citati (0,173 contro 0,105).
- **Piccolo mondo:** nel blocco principale (86,2% delle pronunce) due pronunce distano in media 5,30 passi, contro 4,96 in una rete a caso con gli stessi nodi e legami; i triangoli chiusi sono molti di più (0,151 contro 0,0003). Le distanze ignorano il verso delle citazioni.
- **Pronunce ponte** (betweenness, quante volte una pronuncia sta sul cammino più breve tra altre due): l'1% più alto ha il 37,9% dei vicini in altri gruppi, contro il 22,5% dell'1% più citato e il 16,0% di tutte le pronunce collegate.
- **Robustezza:** togliendo il 20% delle pronunce più citate il blocco principale scende al 50,9% delle pronunce, contro il 65,5% togliendone a caso: la rete si spezza più in fretta, ma senza crolli.

### 9.8 La polarità delle citazioni: lo strumento non supera la soglia

Da `reports/polarity_validation_claude.md`.

- **Che cosa si voleva misurare.** La voce "sentiment analysis" del corso (capire se un testo esprime un giudizio positivo o negativo) adattata a una corte: se una pronuncia segue il precedente che cita o se ne distingue. Si è cercato il caso raro, la distinzione o distacco.
- **Come.** Regole scritte a mano (`src/polarity/lexicon.py`) leggendo metà delle pronunce che citano (la metà di sviluppo, seme 20261121). Ogni regola deve riferirsi al precedente: entro 120 caratteri dalla citazione, nella stessa frase, senza negazioni né forme ipotetiche, non nelle parole del giudice che ha sollevato la questione o delle parti. Prima della prova: soglia di precisione 0,80, campione, e che cosa fare se la soglia non fosse superata.
- **Esito.** Sull'altra metà, i 37 passi segnalati dalle regole sono stati letti dall'assistente senza sapere che cosa avevano deciso le regole, mescolati a 30 passi non segnalati: 28 su 37 sono vere distinzioni, precisione 0,76 (0,60–0,87), **sotto la soglia**. Come stabilito, nessuna analisi con questo strumento.
- **Per regola** (numeri piccoli): "non pertinente" 19 su 21; "caso diverso" 7 su 8; "superamento" 2 su 7; "non affermato" 0 su 1. Tra i 30 passi non segnalati, 5 sono vere distinzioni.
- **Quanto è solido il verdetto.** Poco: mancano due passi per arrivare a 0,80, l'intervallo comprende la soglia, e chi ha letto i passi (l'assistente) aveva anche scritto le regole. Il controllo di una persona servirà solo come verifica: per una regola decisa prima non cambia l'esito.

## 10. Che cosa è cambiato dopo i risultati, e perché

Il registro completo, con le date, è in `docs/decisions.md`. Qui ci sono i cambiamenti che toccano i risultati.

| Parte | Deciso prima | Cambiato o aggiunto dopo, e perché | Come si legge |
| --- | --- | --- | --- |
| D3, risultato principale | Confronto tra precedenti decisi con il giudice presente o assente, a parità di "l'ha scritto lui", età e materia; 50 non citati per pronuncia; incertezza raggruppata per giudice | Il calcolo: esatto al posto dell'approssimazione di Breslow, che avvicina a 1 gli effetti forti (da 1,03 a 1,00; "l'ha scritto lui" da 3,01 a 5,47). La domanda non è cambiata | Principale |
| D3, altre stime | Sei prove di robustezza; il secondo confronto con la data di arrivo | Aggiunte: la stessa legge impugnata, gli articoli della Costituzione, la descrizione delle assenze, il controllo dello 0,88 | Esplorative o descrittive |
| D1 | Confronto con citazioni mandate a caso tra pronunce dello stesso anno; HITS contro citazioni scambiate; criterio di previsione | Aggiunto il confronto con stesso anno e tipo; ritirata la lettura "conta chi ti cita" | Il primo confronto resta il riferimento |
| D2 | Giudici con almeno 30 pronunce; citazioni entro 10 anni; citazioni mandate a caso | Il confronto è diventato il rimescolamento dei giudici; la finestra di 10 anni, decisa ma non applicata nel primo calcolo, è stata applicata; aggiunta la prova dal 1987 | Esplorativo |
| D4 | Effetto minimo 20%; potenza almeno 0,80; Holm sui due confronti | Nessun cambiamento (un generatore casuale suo, perché le modifiche a D2 non spostassero D4) | Come deciso |
| Misure del corso | Non previste | Aggiunte per coprire gli argomenti dei libri di testo | Esplorative |
| Sostituzione dei precedenti | Non prevista | Aggiunta su domanda di Umberto, con regole decise prima del calcolo | Esplorativa |
| Polarità | Soglia 0,80, campione estratto a caso, regola d'arresto | Nessuno: la soglia non è stata superata e non si sono fatte analisi | Come deciso |
| Qualità dell'estrazione | Precisione 0,95 e richiamo 0,90 su almeno 460 citazioni | 342 citazioni invece di 460; dopo il primo campione l'estrattore è stato corretto e riverificato; la lettura di una persona diventerà il riferimento | Da completare |
| Rete dei collegi tra giudici | Nel piano: "misure sulla sola rete dei collegi" senza senso | Costruita il 24/11/2026 su richiesta di Umberto, solo per descrivere e controllare; la regola ora vieta solo i test | Descrittivo |

**Le date principali del lavoro.**

- 7–8/11/2026: il tema, il metodo di lavoro, i dati, le soglie di qualità, il risultato principale.
- 11–12/11/2026: le regole di D1, l'allargamento al corso (temi, API, Wikipedia), il primo confronto con la banca dati SPARQL.
- 16/11/2026: le scelte aperte fissate prima dei risultati; le analisi partono prima dell'approvazione del docente, su richiesta di Umberto.
- 17/11/2026: la fotografia del lavoro prima delle correzioni (etichetta git `versione-17-11`) e un controllo critico.
- 18/11/2026: le correzioni dopo il controllo (D3 esatto, D2 esplorativo, D1 per tipo, test dei numeri); la polarità; le misure del corso; il repository.
- 19–20/11/2026: la materia più fine, le altre corti, le verifiche chieste da una revisione esterna (assenze, 0,88, relazione in due livelli).
- 21/11/2026: la sostituzione dei precedenti; tutto riscritto in linguaggio semplice.
- 22/11/2026: il file dei collegi non riconosciuti per intero.
- 24/11/2026: la rete dei collegi tra giudici.


## 11. Problemi noti e punti non verificati

Questa sezione elenca, uno per uno, i punti del lavoro che hanno un difetto noto o che nessuno ha ancora controllato. Per ogni punto: che cosa succede, perché conta, dove si trova.

### 11.1 Un risultato senza il programma che lo produce

- **Che cosa succede.** Il file `reports/collegio_vs_sedute.json` contiene il confronto tra il collegio ricavato dal testo delle pronunce e i giudici presenti alle sedute secondo la banca dati SPARQL della Corte (dal 2004, 3.684 pronunce). Nessun programma del repository scrive questo file. È stato prodotto il 17/11/2026 da un programma usato una sola volta e non salvato.
- **Perché conta.** La regola del progetto dice che ogni numero della relazione viene da un programma salvato. Da questo file vengono due numeri citati nella relazione (sezione 2.5) e in `CLAUDE.md`: il 97,8% dei giudici del collegio risulta presente alla seduta; il 99,1% dei giudici presenti alla seduta risulta nel collegio.
- **Che cosa serve.** Un programma che ricalcoli i quattro numeri del file partendo da `data/interim/sedute_membri.csv` (scritto da `src/ingest/fetch_api.py`) e da `data/processed/collegio.csv`, e che ottenga gli stessi valori.

### 11.2 Programmi modificati e non rifatti girare

- `src/analysis/topics.py` (le materie) e `src/ingest/sparql_check.py` (il confronto con la banca dati SPARQL) sono stati modificati il 21/11/2026, solo nella parte che scrive il testo dei report. Dopo la modifica non sono stati rifatti girare.
- Il motivo: `topics.py` richiede un calcolo lungo; `sparql_check.py` interroga una banca dati che cambia nel tempo, quindi rifarlo cambierebbe i numeri del 12/11/2026.
- I report `reports/topics.md` e `reports/sparql_reconciliation.md` sono stati convertiti a mano nel nuovo testo, con gli stessi numeri. Un controllo automatico del codice (pyflakes) non segnala errori, ma solo farli girare dimostra che funzionano.

### 11.3 La legenda della rete interattiva

La pagina `reports/rete_interattiva.html` (scritta da `src/analysis/interactive.py`) non è stata ricontrollata dopo la riscrittura dei testi in linguaggio semplice. Le sue etichette possono essere ancora quelle tecniche.

### 11.4 I controlli di qualità sono stati letti dall'assistente, non da una persona

- Le letture di riferimento con cui si misura la qualità dell'estrazione delle citazioni (`data/validation/gold_test.txt`, `data/validation/gold_test2.txt`) e della polarità (`data/validation/gold_polarity_claude.txt`) le ha fatte l'assistente (Claude), non una persona.
- Mancano due controlli a mano, preparati e non ancora fatti:
  - 36 pronunce da leggere per intero, per le citazioni: `data/validation/human_check.md`, da scrivere in `data/validation/gold_human.txt`;
  - 67 passi, per la polarità: `data/validation/polarity_human_check.md`, da scrivere in `data/validation/gold_polarity_human.txt`.

### 11.5 Le date dell'elenco ufficiale dei giudici

- La rete dei collegi tra giudici (`reports/cositting_network.json`) ha mostrato che 13 giudici siedono in un collegio dopo la fine del mandato scritta nell'elenco ufficiale. I casi più grandi: Carlo Mezzanotte (3.271 giorni dopo la fine scritta nell'elenco, che per lui riporta un mandato iniziato e finito nel 1996), Renato Granata (1.084 giorni), Giuseppe Chiarelli (729), Romano Vaccarella (220). Gli altri nove casi vanno da 6 a 120 giorni.
- Le cause possibili: una data sbagliata nell'elenco ufficiale, oppure una pronuncia con la data di decisione sbagliata. Va verificato con una fonte, caso per caso.
- Conseguenze: le date sbagliate restano in `data/processed/judges.csv`. Nessuna analisi usa la fine del mandato scritta nell'elenco: per le analisi un giudice è "in attività" dalla prima all'ultima pronuncia in cui siede nel collegio. Il controllo in `reports/judges_quality.md` non trovava questi casi, perché cerca solo i giudici che smettono di comparire molto prima della fine del mandato, non quelli che compaiono dopo.

### 11.6 Due nomi scritti male nell'elenco dei giudici

Nel campo del nome dell'elenco ufficiale restano due grafie sbagliate: "Vincenzo Caianello" (il cognome giusto è Caianiello) ed "Enzo Capolozza" (il cognome giusto è Capalozza). Il programma le corregge per riconoscere i nomi (`NAME_FIX` in `src/judges/build_judges.py`), ma nelle tabelle (`data/processed/judges.csv` e le tabelle che ne derivano) il nome mostrato resta quello sbagliato.

### 11.7 I collegi non riconosciuti per intero

- 257 pronunce su 22.427 (l'1,15%) hanno il collegio non riconosciuto per intero. Sono elencate in `data/interim/collegio_errors.csv`, con il motivo: 210 hanno meno giudici riconosciuti dei nomi scritti nel testo; 47 hanno meno di 11 giudici. Quasi tutte sono degli anni 1960–1980.
- Cause viste guardando alcune righe: nei testi più vecchi gli errori di trascrizione ("PERASS1", "CASTELL1", con la cifra 1 al posto della lettera I) impediscono di riconoscere un nome; in una pronuncia (la 24/2000) il testo del collegio manca del tutto.
- Conseguenza: i giudici non riconosciuti mancano dalle analisi che usano il collegio (D3, la rete dei collegi tra giudici).
- Nella rete dei collegi tra giudici alcune coppie hanno una quota di pronunce decise insieme molto bassa: per esempio Renato Dell'Andro e Renato Granata hanno deciso insieme 1 pronuncia su 163 decise mentre erano tutti e due in attività (elenco in `reports/cositting_network.json`, voce `bottom10_share_pairs_100`). Possono nascere da un nome riconosciuto male o da una data sbagliata: vanno guardate a mano.

### 11.8 L'installazione da zero

Il README spiega come installare l'ambiente e rifare tutto da zero. Questa procedura non è mai stata provata su un computer nuovo.

## 12. I limiti

Ogni riga dice qual è il problema, quale risultato tocca e in che direzione può spostarlo. La tabella riprende la sezione 4 della relazione.

| Limite | Che cosa tocca | Che effetto può avere |
| --- | --- | --- |
| La lettura di riferimento per giudicare l'estrattore l'ha fatta l'assistente, non una persona, e solo sui passi con parole chiave; le citazioni controllate sono 342 invece di 460 | Tutta la rete delle citazioni | Se assistente ed estrattore sbagliano allo stesso modo, precisione e richiamo risultano più alti del vero |
| L'estrattore trova meno citazioni nei testi fino al 1986 (richiamo 0,917, limite inferiore 0,830) | La durata dei precedenti; D2 per i giudici più antichi | Citazioni ai precedenti antichi contate un po' meno del vero |
| Prima del 23/12/1986 il nome del redattore non c'è e si usa il relatore | D2, D3 | Attenua le differenze tra giudici; la prova dal 1987 dà lo stesso risultato per D3 |
| I relatori non sono assegnati a caso | Il 5,47 di D3 (3,27 a parità di legge impugnata); le classifiche di D2 | Gonfia l'effetto di chi scrive |
| Le assenze dal collegio possono non essere casuali, e il loro motivo non è nei dati | Il risultato principale di D3 | Direzione incerta; le assenze variano poco per tipo di giudizio, articolo e materia, e i precedenti con e senza il giudice sono simili |
| I temi sono 20, alcuni sono formule di scrittura, e cambiano ripetendo il calcolo | Il controllo per materia in D2 e D3 | Controllo imperfetto; con gli articoli della Costituzione il risultato principale non cambia |
| Citare non vuol dire approvare | Tutto | Un precedente può essere citato per prenderne le distanze; lo strumento per misurarlo non ha superato la soglia |
| Le pronunce recenti hanno avuto meno tempo per essere citate | D1, D2 | Gestito confrontando pronunce dello stesso anno e con finestre di tempo fisse; le pronunce dal 2020 dicono ancora poco |
| HITS dà autorevolezza zero a un terzo delle pronunce e concentra il resto in un gruppo | Autorevolezza contro citazioni | La differenza dal caso misura soprattutto l'esistenza dei gruppi |
| In D2 il confronto con il caso è cambiato dopo aver visto i risultati | D2 | Esplorativo: nessuna conclusione certa |
| Provenienza dei giudici ricavata in automatico dalle biografie | D4 | Eventuali errori nascondono un effetto, non lo creano |
| La verifica della sostituzione non distingue tra passaggio di testimone e importanza propria di chi cita | Sezione 9.3 | Il 43% in più può venire in parte dall'una e in parte dall'altra |
| 257 collegi non riconosciuti per intero; date sbagliate nell'elenco dei giudici | D3, la rete dei collegi tra giudici | Pochi casi (1,15% delle pronunce); da controllare a mano (sezione 11) |
| Il tema non è di social media | L'esame | Da concordare con il docente; il progetto è allargato a temi, API e Wikipedia |

## 13. Che cosa resta da fare

### 13.1 Da fare da Umberto (nessun altro può farlo)

1. **Il controllo a mano delle citazioni**: leggere le 36 pronunce di `data/validation/human_check.md` e scrivere le citazioni in `data/validation/gold_human.txt`. È la priorità, prima di qualsiasi estensione.
2. **Il controllo a mano della polarità**: i 67 passi di `data/validation/polarity_human_check.md`, da scrivere in `data/validation/gold_polarity_human.txt`. Serve solo come verifica.
3. **La mail al docente**: la bozza è tenuta fuori dal repository; va letta e inviata da Umberto. Chiede: se il tema rientra nel corso; il perimetro (le tre reti, con o senza D4); progetto individuale o in coppia; forma, scadenze, lingua e lunghezza della consegna; le regole sull'uso dell'intelligenza artificiale.
4. **Confermare il piano di controllo della rete tra corti** (registro, 20/11/2026: "da confermare da Umberto prima di leggere").
5. **Le scelte ancora aperte** (`docs/decisions.md`, "Ancora da decidere"): la licenza del codice; la seconda versione delle regole di polarità; come costruire la rete tra corti (riferimenti alla corte o singole decisioni).
6. **Confrontare la mappa del programma d'esame** (`docs/course_mapping.md`) con l'elenco delle lezioni su Moodle.
7. **Leggere gli articoli a pagamento** non ancora letti (Black e Spriggs 2013; Agnoloni e Pagallo 2015): finché non sono letti non si citano.
8. **Una copia di sicurezza della storia del repository fuori da iCloud** (per esempio un file `git bundle`): la cartella del progetto è sincronizzata con iCloud e alcuni file vengono tolti dal disco.

### 13.2 Prima di rendere pubblico il repository

Dalla lista in `docs/decisions.md`:

- togliere da `docs/spec.md` le note personali di pianificazione (il punto 1 dei "Prossimi passi", con il nome di un collega; il link alla scheda privata su Claude Docs; la sezione "Prossimi passi" e i punti "Da concordare con il docente");
- rileggere `docs/decisions.md` e togliere le note personali;
- decidere se `docs/project_guide.md`, un documento personale di metodo, resta nel repository pubblico; la stessa domanda vale per questo documento;
- aggiungere la licenza del codice al README e un file `LICENSE` (CC BY-SA 3.0 per i dati derivati);
- ripulire la storia del repository dall'indirizzo email e dai file personali, **senza fondere le modifiche tra loro**: le date e l'ordine delle modifiche sono la prova che le regole dal 18/11/2026 in poi sono venute prima dei risultati.

### 13.3 Difetti tecnici da sistemare

Tutti descritti nella sezione 11:

- scrivere il programma che produce `reports/collegio_vs_sedute.json` (11.1);
- far girare `src/analysis/topics.py` e `src/ingest/sparql_check.py` dopo le modifiche al testo (11.2);
- controllare la legenda della rete interattiva (11.3);
- verificare con una fonte le date dei 13 giudici che compaiono in un collegio dopo la fine del mandato scritta nell'elenco (11.5);
- decidere se correggere nel codice anche il nome mostrato di Caianiello e Capalozza (11.6);
- guardare a mano le 257 pronunce di `data/interim/collegio_errors.csv` e le coppie con la quota più bassa nella rete dei collegi tra giudici (11.7);
- capire perché il programma conta 19 pronunce con più redattori e il campo dei dati 17 (sezione 5.8);
- provare l'installazione da zero (11.8).

### 13.4 Più avanti

- **La migrazione a R.** L'analisi andava fatta in R. Si rifà in R solo dopo aver finito tutto in Python; per ora non si cambia nulla.
- **Estensioni possibili** (relazione, sezione 5): una seconda versione delle regole di polarità, decisa prima e provata su dati mai visti con la lettura di una persona; lo studio dei 93 casi in cui il relatore è stato sostituito nella scrittura; la rete tra la Corte costituzionale e le altre quattro corti; l'effetto del Presidente, che sceglie i relatori; un confronto con il Tribunale costituzionale tedesco.
- **Previsti e non fatti** (relazione, sezione 5): il confronto con il modello di Karrer e Newman, che su una rete che cita solo il passato andrebbe ricostruito rispettando le date; l'autorevolezza su finestre di più anni; gli scambi di citazioni anno per anno (circa 60 volte il tempo di calcolo attuale).

## 14. Come si corregge il lavoro

### 14.1 Prima di tutto: che tipo di file è

Ogni file è di uno di due tipi (inventario, sezione 17):

- **scritto a mano** (documenti, relazione, regole, programmi, letture di riferimento): si corregge aprendolo;
- **scritto da un programma** (tabelle in `data/processed/` e `data/interim/`, file in `reports/` tranne la relazione e `validation.md`, le figure): si corregge il programma che lo scrive, poi lo si rifà girare. Una correzione fatta a mano su questi file sparisce la volta successiva che il programma gira.

### 14.2 Correggere un programma

1. Correggere il programma.
2. Rifare girare quel programma e tutti quelli che vengono dopo nell'ordine della sezione 5.0, perché ognuno usa i file di quelli prima.
3. Lanciare i controlli automatici: `.venv/bin/python -m pytest`. Se un numero della relazione non coincide più con i file dei risultati, il controllo indica la frase.
4. Aggiornare a mano il testo della relazione finché il controllo passa.
5. Scrivere una riga nel registro `docs/decisions.md`: la data, la decisione, il motivo, chi l'ha presa.
6. Salvare la modifica con un commit a sé. Non fondere mai i commit tra loro: il loro ordine è la prova che le regole sono venute prima dei risultati.

### 14.3 Casi particolari

- **Un errore nei dati del portale** (un nome scritto male, una data sbagliata): non si tocca mai `data/raw/`. La correzione si scrive nel codice, con la fonte: per i giudici in `src/judges/build_judges.py` (per esempio `NAME_FIX` per i nomi, la riga di Spagnoli per le date); per le pronunce in `src/ingest/build_pronunce.py`.
- **Un errore dell'estrattore delle citazioni:** si corregge `src/extract/citations.py` e si aggiunge la frase che lo mostra a `tests/test_citations.py`. La lettura di riferimento non si ricava mai con il programma che si sta controllando; dopo una correzione, la qualità si misura su un campione nuovo, mai usato per scrivere la correzione.
- **Il testo di un report scritto da un programma:** si corregge la funzione che scrive il testo dentro il programma (per esempio `render_md` in `src/analysis/d3_memoria_collegiale.py` e in `src/analysis/topics.py`). Il paragrafo "In breve" si corregge in `src/report/plain_intros.py`. Per non rifare calcoli lunghi: `src/analysis/d3_memoria_collegiale.py --md-only` riscrive il report di D3 dai numeri salvati; `src/analysis/topics.py --labels-only` ricalcola solo i nomi dei temi.
- **Una regola di metodo:** si cambia in `.claude/rules/` o in `CLAUDE.md`, e il cambiamento si registra in `docs/decisions.md`. Un risultato già visto non si cambia cambiando la regola: un cambiamento fatto dopo aver visto i dati rende il risultato esplorativo.
- **Un file che non si apre o un programma che si blocca leggendo `data/`:** la cartella è sincronizzata con iCloud e alcuni file restano sul cloud; il comando `brctl download <file>` li riporta sul computer.

### 14.4 Come verificare che una correzione non abbia cambiato altro

- Prima di rifare girare un programma, salvare l'impronta dei suoi file: `shasum <file>`. Dopo, confrontarla: se l'impronta è uguale, il file non è cambiato.
- Lanciare `.venv/bin/python -m pytest`.
- Guardare le differenze con `git diff` prima di salvare.

## 15. Chi ha fatto che cosa: l'uso dell'assistente

- Il lavoro è stato svolto con Claude Code, un assistente di programmazione basato su un modello linguistico. L'assistente ha scritto il codice, eseguito le analisi e redatto i testi, compresi la relazione e questo documento, su richiesta e sotto la direzione di Umberto Toraldo.
- Umberto ha scelto il tema, la domanda e le estensioni, e ha preso o delegato le scelte di metodo.
- Il registro `docs/decisions.md` dice per ogni scelta chi l'ha presa, nella colonna "Chi o fonte":
  - "Umberto": la scelta è sua;
  - "Claude, su delega di Umberto": l'ha presa l'assistente, a cui Umberto l'aveva affidata;
  - "Claude": l'assistente l'ha presa mentre faceva il lavoro;
  - "dal check" o "revisione": viene da un controllo del lavoro.
- **Tre conseguenze per chi legge i risultati:**
  1. le letture di riferimento per la qualità dell'estrazione e della polarità sono dell'assistente, non di una persona;
  2. le regole decise prima dei risultati sono state scritte dallo stesso assistente che poi ha fatto le analisi;
  3. le regole del corso sull'uso dell'intelligenza artificiale non sono ancora note.
- **Le istruzioni che l'assistente segue** sono in `CLAUDE.md` e in `.claude/rules/` (`data.md` per i dati e l'estrazione, `network-analysis.md` per le reti e le analisi). Cambiarle cambia il modo di lavorare d'ora in poi, non i risultati già prodotti.

## 16. Glossario

Una parola per ogni concetto. Le parole sono in ordine alfabetico.

- **API.** Un servizio che risponde a domande fatte da un programma invece che da una persona. Qui: la banca dati SPARQL della Corte e l'interfaccia di Wikipedia.
- **Assente.** Un giudice in attività che non siede nel collegio di una pronuncia.
- **Attività, in.** Il periodo dalla prima all'ultima pronuncia in cui un giudice siede nel collegio. Lo usano tutte le analisi. Da non confondere con "in carica".
- **Autorevolezza (authority) e HITS.** HITS è un algoritmo che dà a ogni pronuncia un punteggio di autorevolezza: alto se la pronuncia è citata da pronunce che citano molti precedenti autorevoli.
- **Betweenness.** Quante volte un nodo sta sul cammino più breve tra altri due nodi: misura chi fa da ponte.
- **Blocco principale (componente).** Il gruppo più grande di pronunce collegate tra loro, seguendo le citazioni in un senso o nell'altro.
- **Carica, in.** Il periodo scritto nell'elenco ufficiale dei giudici, dal giuramento alla fine del mandato. Le analisi non lo usano, perché le date di fine hanno errori.
- **Ciclo.** Una sequenza di citazioni che torna al punto di partenza. Nella rete delle citazioni non ce ne sono: si cita solo il passato.
- **Citazione (o legame, nella rete).** La coppia "la pronuncia A cita la pronuncia B", contata una sola volta anche se A nomina B più volte.
- **Collegio.** Il gruppo di giudici (da 11 a 15) che decide una pronuncia.
- **Commit.** Una modifica salvata nella storia del repository, con data e descrizione.
- **Confronto con il caso (modello nullo).** I dati rimescolati a caso, conservando ciò che è ovvio: dicono che cosa ci si aspetterebbe se non ci fosse nulla oltre il caso.
- **«Considerato in diritto» e «Ritenuto in fatto».** Nelle sentenze, il ragionamento della Corte e il riassunto degli argomenti delle parti. Nelle ordinanze: «Considerato che» e «Ritenuto che».
- **Correzione di Holm.** Quando si fanno molti confronti insieme, alza l'asticella in modo che la probabilità anche di un solo falso allarme resti sotto il 5%.
- **Densità.** Legami presenti diviso legami possibili. Nella rete delle citazioni si contano solo i legami possibili verso il passato.
- **Descrittivo, esplorativo, principale.** Le etichette dei risultati: una descrizione dei dati; un risultato trovato, aggiunto o cambiato dopo aver visto i dati; il risultato fissato prima, l'unico da cui si traggono conclusioni formali.
- **Dispositivo.** La parte finale della pronuncia, con la decisione vera e propria e le firme.
- **Distinzione o distacco.** Una citazione in cui la Corte dice che il precedente non è pertinente, riguarda un caso diverso, non è un vero precedente, oppure è superato.
- **Epigrafe.** La parte della pronuncia che dice chi ha portato la questione davanti alla Corte e su quale legge; nelle ordinanze contiene anche il ragionamento.
- **Esito.** Che cosa decide la pronuncia (per esempio una dichiarazione di incostituzionalità). Preso dalla banca dati SPARQL, solo dal 2005.
- **Forza.** La somma dei pesi dei legami di un nodo. Nella rete dei collegi tra giudici: quante coppie giudice–collega ha formato un giudice, sommate su tutte le pronunce.
- **Impronta (SHA-256).** Un codice calcolato dal contenuto di un file, che cambia se cambia anche un solo carattere.
- **Indice di Gini.** Misura quanto è disuguale una distribuzione: 0 se tutte le pronunce ricevono lo stesso numero di citazioni, 1 se una sola le riceve tutte.
- **Intervallo di confidenza al 95%.** L'insieme dei valori compatibili con i dati. Se l'intervallo di un rapporto non comprende 1, la differenza si considera reale.
- **Legge di potenza e lognormale.** Due forme matematiche per distribuzioni in cui pochi casi sono enormi e molti piccoli. Si confrontano con un test, non a occhio.
- **Legge impugnata (norma oggetto) e parametro.** La legge di cui si discute se è costituzionale, e la norma della Costituzione che si dice violata.
- **Manifest.** Il file `data/raw/MANIFEST.csv`, che annota quale versione dei dati è stata scaricata e quando.
- **Massima.** Il riassunto, scritto dall'Ufficio del massimario della Corte, del principio stabilito da una pronuncia.
- **Menzione.** Ogni volta che un numero di pronuncia compare nel testo. Più menzioni della stessa pronuncia nello stesso testo fanno una sola citazione.
- **Modularità, Leiden, Infomap.** Leiden e Infomap sono due metodi per dividere una rete in gruppi di nodi collegati più tra loro che con il resto (i filoni); la modularità misura quanto la divisione è netta.
- **Odds e odds ratio.** Gli odds sono la probabilità di un evento divisa per la probabilità che non accada. L'odds ratio è il rapporto tra gli odds di due gruppi: 1 nessuna differenza, 2 il doppio, 0,5 la metà.
- **PageRank.** Un algoritmo simile a HITS: conta essere citati da pronunce a loro volta citate.
- **Peso.** Il numero associato a un legame. Nella rete dei collegi tra giudici: quante pronunce due giudici hanno deciso insieme.
- **Potenza.** La probabilità di accorgersi di un effetto della grandezza cercata, se l'effetto esiste.
- **Precedente.** Una pronuncia citata, o che poteva essere citata, da una pronuncia successiva.
- **Precisione e richiamo.** La precisione è la quota delle citazioni trovate che sono vere; il richiamo è la quota delle citazioni vere che vengono trovate.
- **Proiezione.** Da una rete con due tipi di nodi (giudici e pronunce) si ottiene una rete con un solo tipo (giudici), collegando i giudici che hanno una pronuncia in comune.
- **Pronuncia, sentenza, ordinanza.** Pronuncia è ogni decisione della Corte. La sentenza decide in via definitiva; l'ordinanza ha una motivazione breve.
- **Pronuncia che cita.** La pronuncia nel cui testo compare la citazione.
- **Quota (nella rete dei collegi tra giudici).** Pronunce decise insieme da due giudici, diviso pronunce decise mentre erano tutti e due in attività.
- **Redattore e relatore.** Il relatore studia la causa e la presenta al collegio; il redattore scrive il testo dopo la decisione. Di solito sono la stessa persona.
- **Regressione logistica condizionata.** Il modello di D3: confronta, dentro ogni pronuncia che cita, i precedenti citati con quelli non citati.
- **Repository.** L'archivio del progetto, con la storia di ogni modifica (git).
- **Rete, nodo, legame, verso.** Una rete è un insieme di cose (nodi) e di relazioni tra loro (legami); un legame con un verso va da un nodo a un altro.
- **Rete di affiliazione.** Una rete che lega le persone agli eventi a cui partecipano: qui i giudici alle pronunce che hanno deciso.
- **Seme.** Il numero da cui parte il generatore casuale: con lo stesso seme, le scelte "a caso" sono sempre le stesse.
- **SPARQL.** Il linguaggio con cui si interroga la banca dati della Corte.
- **Temi (modello di topic, LDA).** Un programma che raggruppa in temi le parole che compaiono spesso insieme; qui dà la materia delle pronunce.
- **Testo di base.** Il testo in cui si cercano le citazioni: «Considerato in diritto» e dispositivo nelle sentenze, «Considerato che» e dispositivo nelle ordinanze.
- **Valore p.** La probabilità di vedere una differenza almeno così grande se in realtà non ci fosse nessuna differenza. Sotto 0,05 la differenza si considera reale.
- **Via incidentale e via principale.** Nel giudizio in via incidentale la questione è sollevata da un giudice durante una causa; in quello in via principale lo Stato o una Regione impugna direttamente una legge.
- **XML.** Il formato dei file del portale: ogni informazione sta tra due etichette con il suo nome.

## 17. Inventario dei file

Ogni file del repository, con che cos'è e come nasce. "A mano" vuol dire scritto a mano; "da X" vuol dire scritto dal programma X. Restano fuori dal repository, e quindi da questo elenco: i file del portale in `data/raw/` (tranne il manifest), i PDF della letteratura in `literature/` (diritti d'autore), l'ambiente `.venv/`.

### 17.1 Istruzioni e configurazione

| File | Che cos'è | Come nasce |
| --- | --- | --- |
| `README.md` | Presentazione del progetto, dati, come rifare tutto, struttura delle cartelle | A mano |
| `CLAUDE.md` | Istruzioni per chi lavora sul progetto, compreso l'assistente: stato, domande, regole sempre valide, soglie | A mano |
| `.claude/rules/data.md` | Regole per i dati, l'estrazione delle citazioni e i giudici | A mano |
| `.claude/rules/network-analysis.md` | Regole per le reti, i confronti con il caso, D3, le varianti | A mano |
| `.claude/settings.json` | Impostazioni dell'assistente: blocca le modifiche dirette a `data/raw/` | A mano |
| `.gitignore` | Che cosa resta fuori dal repository | A mano |
| `pytest.ini` | Limita i controlli automatici alla cartella `tests/` | A mano |
| `requirements.txt` | I pacchetti Python usati dal codice | A mano |
| `requirements.lock` | Le versioni esatte dei pacchetti con cui sono stati prodotti i risultati (Python 3.12.4) | A mano |

### 17.2 Documenti di lavoro (`docs/`)

| File | Che cos'è | Come nasce |
| --- | --- | --- |
| `docs/handbook.md` | Questo documento | A mano |
| `docs/spec.md` | Il piano del progetto, scritto prima dei risultati | A mano |
| `docs/decisions.md` | Il registro delle decisioni: data, decisione, motivo, chi; le liste delle cose da fare | A mano |
| `docs/context.md` | Come nasce una pronuncia, chi fa che cosa, che cosa registrano i dati, con le fonti | A mano |
| `docs/data_schema.md` | Che cosa c'è nei file del portale, campo per campo | A mano (numeri da `inspect_raw.py`) |
| `docs/context_corti.md` | Le altre quattro corti e i loro dati | A mano |
| `docs/sources.md` | Le fonti, con che cosa è stato letto di ciascuna e le pagine | A mano |
| `docs/course_mapping.md` | Ogni argomento del programma d'esame: se è usato e dove, o perché no | A mano |
| `docs/project_guide.md` | Una guida generale alla stesura e alla presentazione di un lavoro scientifico | A mano |

### 17.3 Dati

| File | Che cos'è | Come nasce |
| --- | --- | --- |
| `data/raw/MANIFEST.csv` | File scaricati, indirizzo, ora, impronta | Da `src/ingest/download.py` |
| `data/processed/pronunce.csv` | Una riga per pronuncia, senza testi | Da `src/ingest/build_pronunce.py` |
| `data/processed/citations.csv` | Una riga per menzione trovata | Da `src/extract/citations.py` |
| `data/processed/edges_citations.csv` | La rete delle citazioni (testo di base) | Da `src/extract/citations.py` |
| `data/processed/edges_citations_fulltext.csv` | La rete delle citazioni nel testo intero (variante) | Da `src/extract/citations.py` |
| `data/processed/edges_citations_with_notes.csv` | La rete più le coppie trovate solo nelle massime (variante) | Da `src/extract/citations_massime.py` |
| `data/processed/judges.csv` | Una riga per giudice | Da `src/judges/build_judges.py` |
| `data/processed/pronunce_judges.csv` | Relatore, redattore, fonte del nome, dimensione del collegio, per pronuncia | Da `src/judges/build_judges.py` |
| `data/processed/collegio.csv` | Una riga per coppia (pronuncia, giudice del collegio) | Da `src/judges/build_judges.py` |
| `data/processed/topics_theta.npz` | I pesi dei 20 temi per ogni pronuncia | Da `src/analysis/topics.py` |
| `data/processed/topics_pronunce.csv` | Il tema principale di ogni pronuncia | Da `src/analysis/topics.py` |
| `data/processed/parametri_pronunce.csv` | Gli articoli della Costituzione invocati da ogni pronuncia | Da `src/analysis/parametri.py` |
| `data/processed/nodes.csv` | La tabella completa delle pronunce, con tipo di giudizio e citazioni fatte e ricevute | Da `src/networks/build.py` |
| `data/processed/edges_redazione.csv` | Giudice → pronuncia scritta | Da `src/networks/build.py` |
| `data/processed/edges_judges.csv` | Rete tra giudici pesata con le citazioni | Da `src/networks/build.py` |
| `data/processed/edges_cositting.csv` | Rete dei collegi tra giudici: i legami | Da `src/networks/cositting.py` |
| `data/processed/judges_cositting.csv` | Rete dei collegi tra giudici: i giudici | Da `src/networks/cositting.py` |
| `data/processed/cositting_network.graphml` | Rete dei collegi tra giudici, per Gephi o networkx | Da `src/networks/cositting.py` |
| `data/processed/esiti.csv` | L'esito delle pronunce dal 2005 | Da `src/ingest/fetch_api.py` |
| `data/processed/wikipedia_links.csv` | Le pronunce citate in voci di Wikipedia | Da `src/ingest/fetch_api.py` |
| `data/processed/judges_attributes.csv` | Provenienza e organo di nomina di ogni giudice | Da `src/analysis/d2_d4_giudici.py` |
| `data/processed/communities.csv` | Il filone (gruppo di Leiden) di ogni pronuncia | Da `src/analysis/extras.py` |
| `data/validation/gold_test.txt`, `gold_test2.txt` | Le letture di riferimento delle citazioni, primo e secondo campione | A mano, dall'assistente |
| `data/validation/gold_human.txt` | Il file in cui una persona scrive le citazioni lette (oggi vuoto) | Modello da `src/validation/human_sheet.py`; da compilare a mano |
| `data/validation/human_check.md` | Il foglio con le 36 pronunce da leggere | Da `src/validation/human_sheet.py` |
| `data/validation/polarity_test_sample.csv` | I passi del campione di prova della polarità, senza le decisioni delle regole | Da `src/polarity/draw_sample.py` |
| `data/validation/polarity_test_labels.csv` | Le decisioni delle regole sugli stessi passi | Da `src/polarity/draw_sample.py` |
| `data/validation/gold_polarity_claude.txt` | La lettura di riferimento della polarità | A mano, dall'assistente |
| `data/validation/polarity_human_check.md` | Il foglio con i 67 passi per una persona | Da `src/polarity/draw_sample.py` |
| `data/validation/gold_polarity_human.txt` | Il file in cui una persona scrive la sua lettura (oggi vuoto) | Modello da `src/polarity/draw_sample.py`; da compilare a mano |
| `data/manual/` | Cartella per le correzioni fatte a mano: vuota, perché le correzioni sono nel codice | — |

**Fuori dal repository, in `data/interim/`** (si rigenerano rifacendo i programmi): `pronunce.pkl` (le pronunce con i testi, da `build_pronunce.py`); `citation_errors.csv`, `citation_excluded.csv`, `citation_same_date.csv`, `citation_type_mismatch.csv` (da `citations.py`); `collegio_errors.csv` (da `build_judges.py`); `sedute_membri.csv` (da `fetch_api.py`); `d1_yearly.pkl` e `d1_panel_<anno>.pkl` (da `d1_pronunce.py`); `d3_mandate.pkl` (da `d3_memoria_collegiale.py`); `d3_full.pkl` (da `d3_full_check.py`); `polarity_contexts.pkl` (da `polarity/contexts.py`); `courts_split.csv` (da `courts/sizing.py`); `courts_mentions_dev.csv` e `courts_dev_sheet.md` (da `courts/mentions.py`); `logs/` (i messaggi scritti dai programmi lunghi mentre giravano).

### 17.4 Risultati (`reports/`)

| File | Che cos'è | Come nasce |
| --- | --- | --- |
| `reports/relazione_for_dummies.md` | La relazione, in due parti | A mano; numeri confrontati con i file dei risultati da `tests/test_report_numbers.py` |
| `reports/validation.md` | Il quadro dei controlli di qualità | A mano |
| `reports/validation_round1.md` | La prima misura della qualità dell'estrazione, prima della correzione | Da `src/validation/evaluate.py` (versione del 17/11/2026, non più rifacibile); testo convertito a mano il 21/11/2026 con gli stessi numeri |
| `reports/validation_test.md`, `validation_test2.md` | Qualità dell'estrazione sul primo campione (dopo la correzione) e sul secondo | Da `src/validation/evaluate.py` |
| `reports/data_inspection.md` | Il primo controllo dei file | Da `src/ingest/inspect_raw.py` |
| `reports/sparql_reconciliation.md` | Il confronto con la banca dati SPARQL (12/11/2026) | Da `src/ingest/sparql_check.py`; testo convertito a mano il 21/11/2026 con gli stessi numeri |
| `reports/judges_quality.md` | Qualità del riconoscimento dei giudici | Da `src/judges/build_judges.py` |
| `reports/topics.md`, `topics.json` | I temi | Da `src/analysis/topics.py` (il `.md` convertito a mano il 21/11/2026 con gli stessi numeri) |
| `reports/parametri.json` | Gli articoli della Costituzione | Da `src/analysis/parametri.py` |
| `reports/network_basic.json` | Le misure di base della rete delle citazioni | Da `src/networks/build.py` |
| `reports/cositting_network.json` | La rete dei collegi tra giudici: descrizione e controlli | Da `src/networks/cositting.py` |
| `reports/massime_citations.json` | Le citazioni trovate nelle massime | Da `src/extract/citations_massime.py` |
| `reports/api_fetch.json` | La data delle interrogazioni delle API | Da `src/ingest/fetch_api.py` |
| `reports/collegio_vs_sedute.json` | Collegio contro presenti alle sedute | **Nessun programma** (sezione 11.1) |
| `reports/d1_results.json` | D1 e D1b | Da `src/analysis/d1_pronunce.py` |
| `reports/d2_results.json`, `d4_results.json` | D2 e D4 | Da `src/analysis/d2_d4_giudici.py` |
| `reports/d2_strata_check.json` | Il controllo dei gruppi di D2 | Da `src/analysis/d2_strata_check.py` |
| `reports/d3_results.json`, `d3_results.md` | D3 | Da `src/analysis/d3_memoria_collegiale.py` |
| `reports/d3_absences.json` | Le assenze dal collegio | Da `src/analysis/d3_absences.py` |
| `reports/d3_full_check.json` | Il controllo dello 0,88 | Da `src/analysis/d3_full_check.py` |
| `reports/precedent_succession.json` | La sostituzione dei precedenti | Da `src/analysis/precedent_succession.py` |
| `reports/extras.json` | Filoni, esito, Wikipedia, autocitazioni, HITS per gruppo | Da `src/analysis/extras.py` |
| `reports/course_measures.json` | Le misure dei libri di testo | Da `src/analysis/course_measures.py` |
| `reports/numbers.json` | Numeri della relazione che nessun programma di analisi salvava | Da `src/report/report_numbers.py` |
| `reports/polarity_validation_claude.md`, `.json` | La prova della polarità | Da `src/polarity/evaluate.py` |
| `reports/courts_sizing.json` | Quante pronunce nominano le altre corti | Da `src/courts/sizing.py` |
| `reports/figures/fig1_…png` … `fig10_…png` | Le 10 figure (elenco nella sezione 5.18) | Da `src/analysis/figures.py` |
| `reports/rete_interattiva.html` | La rete da esplorare nel browser | Da `src/analysis/interactive.py` |

Il paragrafo "In breve" in testa a 9 di questi report (`data_inspection.md`, `sparql_reconciliation.md`, `topics.md`, `d3_results.md`, `validation_round1.md`, `validation_test.md`, `validation_test2.md`, `polarity_validation_claude.md`, `judges_quality.md`) lo scrive `src/report/plain_intros.py`.

### 17.5 Programmi e controlli automatici

Tutti i programmi sono scritti a mano e descritti nella sezione 5: `src/ingest/` (download.py, inspect_raw.py, sparql_check.py, build_pronunce.py, fetch_api.py), `src/extract/` (citations.py, citations_massime.py), `src/validation/` (sample_passages.py, evaluate.py, human_sheet.py), `src/judges/build_judges.py`, `src/networks/` (build.py, cositting.py), `src/analysis/` (topics.py, parametri.py, d1_pronunce.py, d2_d4_giudici.py, d2_strata_check.py, d3_memoria_collegiale.py, d3_absences.py, d3_full_check.py, precedent_succession.py, extras.py, course_measures.py, figures.py, interactive.py, e il modello di pagina `interactive_template.html` usato da interactive.py), `src/polarity/` (contexts.py, lexicon.py, draw_sample.py, evaluate.py), `src/courts/` (sizing.py, mentions.py), `src/report/` (report_numbers.py, plain_intros.py). I controlli automatici sono in `tests/` (test_citations.py, test_report_numbers.py).

## 18. Mappa delle fonti di questa guida

Per ogni sezione, i file da cui è presa. Servono per approfondire, per controllare un punto, e per aggiornare questo documento quando il lavoro cambia: se cambia uno dei file elencati, va riletta la sezione corrispondente.

| Sezione | File da cui è presa |
| --- | --- |
| 0. Come usare questo documento | `tests/test_report_numbers.py`; `docs/decisions.md` (intestazione); `reports/relazione_for_dummies.md` (avvertenza iniziale) |
| 1. Il progetto in breve | `CLAUDE.md` ("Il progetto in breve", "Le domande di ricerca"); `docs/spec.md` ("La domanda"); `reports/relazione_for_dummies.md` (Parte I); `reports/d1_results.json`, `reports/d3_results.json`, `reports/precedent_succession.json` |
| 2. Il contesto | `docs/context.md` (tutte le sezioni); `reports/relazione_for_dummies.md` (1.3, "Chiarimenti di base") |
| 3. I dati di partenza | `docs/data_schema.md`; `reports/data_inspection.md`; `data/raw/MANIFEST.csv`; `docs/spec.md` ("I dati"); `reports/relazione_for_dummies.md` (1.1–1.3) |
| 4. Il piano | `docs/spec.md` ("Come si controlla ogni risultato"); `docs/decisions.md` (righe 8/11–16/11 e "Le decisioni principali, in breve"); `reports/relazione_for_dummies.md` (2.1, 2.9) |
| 5. I passaggi | L'intestazione di ogni programma in `src/`; `README.md` ("Come rifare tutto"); `reports/relazione_for_dummies.md` (2.2–2.7, 6); `reports/topics.md`; `reports/judges_quality.md`; `reports/numbers.json`; `reports/cositting_network.json`; `docs/context_corti.md`; `reports/courts_sizing.json` |
| 6. I controlli di qualità | `reports/validation.md`; `reports/validation_round1.md`, `validation_test.md`, `validation_test2.md`; `reports/judges_quality.md`; `reports/sparql_reconciliation.md`; `reports/collegio_vs_sedute.json`; `docs/decisions.md` (righe 16/11 e 19/11 sul controllo a mano) |
| 7. Le reti | `reports/relazione_for_dummies.md` (2.6, 3.1); `reports/network_basic.json`; `reports/cositting_network.json`; `docs/spec.md` ("I concetti delle reti applicati a questo caso"); `.claude/rules/network-analysis.md` |
| 8. Il confronto con il caso | `reports/relazione_for_dummies.md` (2.8); `.claude/rules/network-analysis.md`; `docs/spec.md` ("Come si controlla ogni risultato") |
| 9. I risultati | `reports/relazione_for_dummies.md` (3.2–3.9); `reports/d1_results.json`, `d2_results.json`, `d4_results.json`, `d3_results.json`, `d3_absences.json`, `d3_full_check.json`, `extras.json`, `course_measures.json`, `precedent_succession.json`, `polarity_validation_claude.md` |
| 10. I cambiamenti | `reports/relazione_for_dummies.md` (2.9); `docs/decisions.md` (tutte le righe) |
| 11. Problemi noti | `reports/cositting_network.json`; `data/interim/collegio_errors.csv`; `docs/decisions.md` (righe 21/11, 22/11, 24/11); la ricerca nel codice dei programmi che scrivono ogni file |
| 12. I limiti | `reports/relazione_for_dummies.md` (4) |
| 13. Che cosa resta da fare | `docs/decisions.md` ("Ancora da decidere", "Da chiedere al docente", "Prima di rendere pubblico il repository"); `CLAUDE.md` ("A che punto è"); `reports/relazione_for_dummies.md` (5) |
| 14. Come si corregge | `CLAUDE.md` ("Regole sempre valide"); `.claude/rules/data.md`; `README.md` |
| 15. L'uso dell'assistente | `reports/relazione_for_dummies.md` (8); `docs/decisions.md` (intestazione) |
| 16. Glossario | `reports/relazione_for_dummies.md` ("Le parole tecniche, spiegate"); `docs/context.md` |
| 17. Inventario dei file | `git ls-files`; il contenuto di `data/interim/`; la ricerca nel codice di chi scrive e chi legge ogni file |
