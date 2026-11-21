---
paths:
  - "src/ingest/**"
  - "src/extract/**"
  - "src/judges/**"
  - "src/validation/**"
  - "data/**"
---
# Regole per i dati e per l'estrazione delle citazioni

Queste regole valgono quando si lavora sui programmi che leggono i dati, estraggono le citazioni o riconoscono i giudici.

## Scaricare i dati

- I file del portale si scaricano solo con un programma in `src/ingest/`, mai a mano. `.claude/settings.json` impedisce di modificare direttamente `data/raw/`.
- Ogni download aggiunge una riga a `data/raw/MANIFEST.csv`, con quattro colonne: `file, url, downloaded_at, sha256` (il file, l'indirizzo da cui viene, quando è stato scaricato, la sua impronta).
- Il portale si aggiorna ogni giorno o ogni settimana: il manifest dice quale versione dei dati ha prodotto i risultati. Il manifest si salva in git; i file scaricati no.

## Il testo in cui si cercano le citazioni (il testo di base)

- Nelle sentenze: il «Considerato in diritto» e il dispositivo. Nelle ordinanze: il «Considerato che» e il dispositivo.
- È escluso il «Ritenuto in fatto» («Ritenuto che…» nelle ordinanze), perché riassume gli argomenti del giudice che ha sollevato la questione e delle parti, con le loro citazioni: non sono citazioni della Corte.
- Le note delle massime le scrive l'Ufficio del massimario della Corte, non i giudici. Quindi non entrano nella rete dei giudici e stanno in una tabella a parte.
- Due varianti servono a vedere se i risultati reggono: il testo intero; il testo con le note delle massime. La colonna `section` di `citations.csv` deve permettere di ricostruirle tutte e due.
- Dove stanno le parti del testo nei file (`docs/data_schema.md`):
  - nelle sentenze, dentro `<testo>`, le etichette `<fatto>` e `<diritto>` racchiudono solo il titolo; il testo della parte viene dopo l'etichetta. Il «Considerato in diritto» va dall'etichetta `<diritto>` alla fine di `<testo>`;
  - nelle ordinanze il ragionamento sta dentro `<epigrafe>`, non in `<testo>`. La formula «Considerato che» compare solo nel 50% delle epigrafi: prima di scrivere il programma che legge le ordinanze, si elencano le altre formule, decennio per decennio;
  - il dispositivo sta in `<dispositivo>`; le firme in fondo non contengono citazioni.
- Nei testi più vecchi ci sono errori di trascrizione, con cifre al posto di lettere ("PERASS1", "MAR10"). Possono colpire anche i numeri delle citazioni (per esempio una "l" al posto di un "1"): va controllato sul campione 1956–1980.

## I modi in cui la Corte scrive una citazione, da riconoscere tutti

- Una citazione sola: "sentenza n. 120 del 2019", "ordinanza n. 45 del 2020".
- Le abbreviazioni: "sent.", "ord.", "sentt.", "ordd."; il numero al singolare "n." e al plurale "nn." ("sentenze nn. 26 e 320 del 2007").
- Un elenco con l'anno scritto una volta sola: "sentenze n. 26 e n. 320 del 2007" diventa due citazioni, tutte e due del 2007.
- Un elenco separato da virgole: "ordinanze n. 10, n. 20 e n. 30 del 2015".
- Un elenco con anni diversi: "sentenze n. 10 del 2015 e n. 20 del 2016".
- Un elenco con tipi diversi: "sentenza n. 26 del 2007 e ordinanza n. 5 del 2008". Ogni elemento prende il proprio tipo.
- La forma con la barra: "n. 26 e n. 320/2007".
- Gli spazi mancanti: "n.4/2008".
- La data per esteso: "sentenza 26 giugno 1956, n. 1". Prima di aggiungerla al programma, si controlla sul campione 1956–1980 se compare e in quali forme.

## Che cosa non è una citazione della Corte

- Le ordinanze con cui i giudici comuni mandano una questione alla Corte (ordinanze di rimessione): si riconoscono dal numero di registro ("reg. ord.", "r.o.").
- Le pronunce di altre corti, che si scrivono allo stesso modo: Corte di cassazione (anche "sezioni unite"), Consiglio di Stato, TAR, Corte dei conti, Corte europea dei diritti dell'uomo, Corte di giustizia. Si escludono guardando le parole che vengono prima della citazione; quante parole guardare si decide sul campione di controllo.
- Gli atti amministrativi scritti allo stesso modo, per esempio le ordinanze della Protezione civile o le ordinanze delle Regioni e dei sindaci.
- I rimandi senza numero ("la citata ordinanza"): non diventano citazioni nella rete.
- Ciò che viene escluso va in `data/interim/citation_excluded.csv`, con il motivo, così lo si può controllare.

## I controlli

- Una citazione verso una pronuncia che non esiste, o depositata dopo quella che cita, va in `data/interim/citation_errors.csv`, non nella rete.
- Le citazioni tra pronunce con la stessa data vanno in `data/interim/citation_same_date.csv`, non tra gli errori, finché `docs/context.md` non chiarisce se sono possibili. La data che mette in ordine le pronunce (decisione o deposito) è quella scritta in `docs/decisions.md`.
- Il controllo del tipo: il tipo scritto nella citazione (sentenza o ordinanza) si confronta con il tipo della pronuncia citata. I casi in cui non coincidono vanno in `data/interim/citation_type_mismatch.csv`. Restano nella rete finché il controllo di qualità non dice se sono errori; come trattarli si scrive in `docs/decisions.md`. Il controllo ha senso solo se la numerazione è comune a sentenze e ordinanze (vedi `CLAUDE.md`).

## Che cosa producono i programmi

- `data/processed/citations.csv`, una riga per ogni citazione trovata: `citing_id, cited_id, raw_match, section, char_start, char_end` (chi cita, chi è citato, il testo trovato, la parte del testo, dove comincia e dove finisce).
- `data/processed/edges_citations.csv`, una riga per ogni coppia di pronunce, con `n_mentions` (quante volte la prima cita la seconda).

## I giudici

- I nomi si rendono uniformi (solo il cognome, nome e cognome, tutto maiuscolo). I nomi scritti male nei file si correggono nel codice (`NAME_FIX` in `src/judges/build_judges.py`), con la fonte della correzione; i casi dubbi si controllano a mano.
- Presidente, relatore, redattore e collegio si interpretano secondo `docs/context.md`. Il redattore scrive il ragionamento dopo che il collegio ha deciso: non è chi decide.
- Il nome del redattore sta in posti diversi a seconda del periodo (`docs/context.md`, sezione 5):
  - fino alla pronuncia 286/1986 non è scritto: firmano tutti i giudici;
  - dalla 287/1986 al 2001 sta solo nelle firme in fondo al dispositivo ("Il redattore: COGNOME");
  - dal 2002 sta nel campo `redattore_pronuncia`, che dal 2016 può contenere più nomi separati da " - ".

  La colonna `redattore_source` dice da dove viene il nome: `field` (il campo), `signature` (la firma) oppure `relatore_proxy` (il relatore, usato al posto del redattore). Per le pronunce fino alla 286/1986 il redattore è il relatore: è un'approssimazione dichiarata in `docs/decisions.md`.
- Ci sono giudici con lo stesso cognome (Sandulli, Reale, Gallo, Marini): il collegamento all'elenco dei giudici usa nome, cognome e periodo del mandato, mai il solo cognome. Le righe dell'elenco con più nomi ("Lattanzi - Cartabia") non sono giudici e si scartano.
- L'elenco dei giudici va completato, con la fonte di ogni correzione: mancano 33 date di fine mandato (calcolate come giuramento più 9 anni, `docs/decisions.md`, 16/11/2026) e la fine del mandato di Spagnoli è sbagliata (1995, non 2005). Le correzioni stanno nel codice di `src/judges/build_judges.py`.
- Relatore e redattore possono essere persone diverse: si conservano tutti e due, e si segnalano i casi in cui sono diversi.
- Nei collegi dei giudizi d'accusa possono comparire giudici aggiunti, che non sono giudici costituzionali: non si collegano all'elenco dei giudici.
- Una pronuncia può avere più redattori: nel campo `redattore_pronuncia` succede in 17 pronunce, dal 2016. Come contarle nella rete dei giudici si decide e si scrive in `docs/decisions.md`.
- Il collegio non è un campo ordinato: l'elenco dei giudici presenti si ricava dal testo ("composta dai signori" o formule simili).
- La soglia per il collegio: almeno il 98% delle pronunce con il collegio riconosciuto per intero, cioè tra 11 (il numero legale) e 15 giudici, tutti collegati all'elenco. Le pronunce sotto la soglia vanno in `data/interim/collegio_errors.csv`.

## I controlli con la banca dati SPARQL della Corte

- Relatore: si confronta il relatore dei file con quello della banca dati (`relatorePronuncia`), con il programma `src/ingest/sparql_check.py`; la quota di accordo va in `reports/sparql_reconciliation.md`. Al 12/11/2026 era del 97,12%. Due cognomi scritti male nei file vanno corretti: "Caianello" in Caianiello e "Capolozza" in Capalozza. Per le 10 pronunce con il relatore vuoto nei file si usa quello della banca dati. La banca dati distingue i giudici con lo stesso cognome con l'iniziale ("SANDULLI A.").
- Collegio: dopo averlo ricavato dal testo, lo si confronta con i giudici presenti alle sedute collegate alla pronuncia (`onto:seduta`, `onto:haMembro`, dal 2004). In `reports/validation.md` si riportano due quote: quanti giudici del collegio risultano presenti alla seduta, e quanti presenti alla seduta risultano nel collegio. È un controllo parziale: la seduta non coincide sempre con la riunione in cui la Corte decide (la camera di consiglio).
- Esito: si prende dalla banca dati, con tutte le sue etichette, dal 2005; non si ricava dal dispositivo.

## Il controllo di qualità dell'estrazione

- Un campione diviso per decennio e tipo di pronuncia, in `data/validation/`, letto da chi controlla. L'elenco delle citazioni giuste (il riferimento) non si ricava mai con il programma che si sta controllando.
- Si contano le coppie di pronunce (`citing_id, cited_id`).
- Le pronunce del campione si leggono per intero, cioè con tutte le citazioni del testo di base: altrimenti non si può misurare quante citazioni il programma perde (il richiamo).
- La dimensione: almeno 460 coppie in tutto. È il numero che serve per stimare una precisione di 0,95 con un margine di ±0,02 (1,96² × 0,95 × 0,05 / 0,02² ≈ 456). Si aggiungono pronunce intere finché non si arriva a quel numero.
- In `reports/validation.md` si riportano: precisione e richiamo per ogni gruppo del campione, i casi del controllo del tipo, un controllo a mano delle citazioni escluse guardando le parole che le precedono.
