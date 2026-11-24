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

<!-- SEZIONI 5-10: in scrittura -->

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

<!-- SEZIONI 12-18: in scrittura -->
