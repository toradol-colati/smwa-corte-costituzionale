---
paths:
  - "src/ingest/**"
  - "src/extract/**"
  - "src/judges/**"
  - "data/**"
---
# Regole per dati ed estrazione

## Download
- I file del portale si scaricano solo con uno script in `src/ingest/`, mai a mano. Le modifiche dirette a `data/raw/` sono bloccate da `.claude/settings.json`.
- Ogni download aggiunge una riga a `data/raw/MANIFEST.csv`: `file, url, downloaded_at, sha256`.
- Il portale si aggiorna ogni giorno o ogni settimana: il manifest dice quale versione dei dati ha prodotto i risultati. Il manifest si versiona, i file scaricati no.

## Testo di base
- Sentenze: «Considerato in diritto» e dispositivo. Ordinanze: «Considerato che» e dispositivo.
- Escluso il «Ritenuto in fatto» («Ritenuto che…» nelle ordinanze): riassume gli argomenti del giudice che ha sollevato la questione e delle parti, con le loro citazioni.
- Le note delle massime le scrive l'Ufficio del massimario della Corte, non i giudici: escluderle dalla rete dei giudici e tenerle in una tabella separata.
- Varianti di robustezza: testo intero; testo con le note editoriali. Il campo `section` di `citations.csv` deve permettere di ricostruirle tutte e due.
- Dove stanno le sezioni nei file (`docs/data_schema.md`):
  - sentenze: in `<testo>`, i tag `<fatto>` e `<diritto>` contengono solo il titolo; il testo della sezione segue il tag. Il «Considerato in diritto» va dal tag `<diritto>` alla fine di `<testo>`;
  - ordinanze: la motivazione sta dentro `<epigrafe>`, non in `<testo>`. «Considerato che» compare solo nel 50% delle epigrafi: prima di scrivere il parser, censire le altre formule per decennio;
  - dispositivo: in `<dispositivo>`; le firme in fondo non contengono citazioni.
- Nei testi più vecchi ci sono errori di trascrizione con cifre al posto di lettere ("PERASS1", "MAR10"): possono colpire anche i numeri delle citazioni (per esempio "l" al posto di "1"). Da verificare sul campione 1956–1980.

## Formati da riconoscere
- Singola: "sentenza n. 120 del 2019", "ordinanza n. 45 del 2020".
- Abbreviazioni: "sent.", "ord.", "sentt.", "ordd."; numero al singolare "n." e al plurale "nn." ("sentenze nn. 26 e 320 del 2007").
- Elenco con l'anno indicato una volta: "sentenze n. 26 e n. 320 del 2007" diventa due archi, entrambi con anno 2007.
- Elenco separato da virgole: "ordinanze n. 10, n. 20 e n. 30 del 2015".
- Elenco con anni diversi: "sentenze n. 10 del 2015 e n. 20 del 2016".
- Elenco con tipi diversi: "sentenza n. 26 del 2007 e ordinanza n. 5 del 2008". Ogni elemento prende il proprio tipo.
- Forma con la barra: "n. 26 e n. 320/2007".
- Spazi mancanti: "n.4/2008".
- Data per esteso: "sentenza 26 giugno 1956, n. 1". Prima di aggiungerla all'estrattore, verificare sul campione 1956–1980 se ricorre e in quali forme.

## Cosa non è una citazione della Corte
- Le ordinanze di rimessione dei giudici comuni: si riconoscono dal numero di registro ("reg. ord.", "r.o.").
- Le pronunce di altre corti, che hanno lo stesso formato: Corte di cassazione (anche "sezioni unite"), Consiglio di Stato, TAR, Corte dei conti, Corte EDU, Corte di giustizia. Si escludono con un filtro sul contesto che precede la citazione. L'ampiezza del contesto si fissa sul campione di validazione.
- Gli atti amministrativi con lo stesso formato, per esempio le ordinanze della Protezione civile o le ordinanze regionali e sindacali.
- I rinvii senza numero ("la citata ordinanza"): non generano archi.
- Ciò che il filtro esclude va in `data/interim/citation_excluded.csv`, con il motivo, per poterlo controllare.

## Controlli
- Un arco verso una pronuncia inesistente o successiva alla citante va in `data/interim/citation_errors.csv`, non nella rete.
- Le citazioni tra pronunce con la stessa data vanno in `data/interim/citation_same_date.csv`, non tra gli errori, finché `docs/context.md` non chiarisce se sono legittime. La data che ordina le pronunce (decisione o deposito) è quella registrata in `docs/decisions.md`.
- Controllo del tipo: il tipo scritto nella citazione (sentenza o ordinanza) si confronta con il tipo della pronuncia citata. I casi in cui non coincide vanno in `data/interim/citation_type_mismatch.csv`. Restano nella rete finché la validazione non dice se sono errori; come trattarli si registra in `docs/decisions.md`. Il controllo vale solo se la numerazione è comune a sentenze e ordinanze (vedi `CLAUDE.md`).

## Output
- `data/processed/citations.csv`: `citing_id, cited_id, raw_match, section, char_start, char_end`.
- `data/processed/edges_citations.csv`: un arco per coppia, con `n_mentions`.

## Giudici
- Normalizzare i nomi (solo cognome, nome e cognome, maiuscole) con `data/manual/judge_name_map.csv`; i casi ambigui si controllano a mano.
- Presidente, relatore, redattore e collegio si interpretano secondo `docs/context.md`. Il redattore scrive la motivazione dopo la decisione del collegio: non è chi decide.
- Il redattore sta in posti diversi a seconda del periodo (`docs/context.md`, sezione 5):
  - fino alla pronuncia 286/1986 non è registrato: firmano tutti i giudici;
  - da 287/1986 al 2001 sta solo nelle firme del dispositivo ("Il redattore: COGNOME");
  - dal 2002 sta nel campo `redattore_pronuncia`, che dal 2016 può contenere più nomi separati da " - ".

  Conservare in una colonna (`redattore_source`) da dove viene il dato: `field`, `signature` oppure `relatore_proxy`. Per le pronunce fino alla 286/1986 il redattore è il relatore, come approssimazione dichiarata (`docs/decisions.md`).
- Gli omonimi esistono (Sandulli, Reale, Gallo, Marini): l'abbinamento all'anagrafica usa nome e cognome e il periodo di mandato, mai il solo cognome. Le righe dell'anagrafica con più nomi ("Lattanzi - Cartabia") non sono giudici e si scartano.
- L'anagrafica va completata in `data/manual/`, con la fonte in ogni riga: 33 date di cessazione mancanti e la cessazione di Spagnoli (1995, non 2005).
- Redattore e relatore possono essere diversi: conservare entrambi e marcare i casi in cui differiscono.
- Nei collegi dei giudizi d'accusa possono comparire giudici aggregati, che non sono giudici costituzionali: non vanno abbinati all'anagrafica dei giudici.
- Una pronuncia può avere più redattori: nei dati succede in 17 pronunce, dal 2016. Come pesarle nello strato 2 e nella rete tra giudici si decide e si registra in `docs/decisions.md`.
- Collegio: se non è un campo strutturato, estrarre dal testo l'elenco dei giudici presenti ("composta dai signori" o formule equivalenti).
- Soglia per il collegio: almeno il 98% delle pronunce con il collegio riconosciuto per intero, tra 11 (il numero legale) e 15 giudici, tutti abbinati all'anagrafica. Le pronunce fuori soglia vanno in `data/interim/collegio_errors.csv`.

## Controlli incrociati con l'endpoint SPARQL
- Relatore: confronto tra il relatore dei file e `relatorePronuncia` dell'endpoint (script `src/ingest/sparql_check.py`); tasso di concordanza in `reports/sparql_reconciliation.md`. Al 12/11/2026: 97,12%. Nella tabella dei nomi vanno corretti "Caianello" in Caianiello e "Capolozza" in Capalozza; per le 10 pronunce con relatore vuoto nei file si usa quello dell'endpoint. L'endpoint distingue gli omonimi con l'iniziale ("SANDULLI A.").
- Collegio: dopo l'estrazione, confronto con i membri delle sedute collegate alla pronuncia (`onto:seduta`, `onto:haMembro`, dal 2004). Si riportano in `reports/validation.md` la quota di membri estratti presenti nella seduta e la quota di membri della seduta presenti nell'estratto. È un controllo parziale: la seduta non coincide sempre con la camera di consiglio.
- Esito: dall'endpoint, dal 2005, tutte le etichette; nessuna estrazione dal dispositivo.

## Validazione
- Campione stratificato per decennio e tipo in `data/validation/`, annotato a mano. Il gold standard non si genera mai con l'estrattore.
- Unità di misura: la coppia di pronunce (`citing_id, cited_id`).
- Le pronunce del campione si annotano per intero, cioè tutte le citazioni del testo di base: altrimenti il richiamo non si può misurare.
- Dimensione: almeno 460 coppie in totale, cioè la precisione di 0,95 stimata con un margine di ±0,02 (1,96² × 0,95 × 0,05 / 0,02² ≈ 456). Si estraggono pronunce intere finché non si raggiunge il numero.
- In `reports/validation.md` si riportano: precisione e richiamo per strato, i casi del controllo del tipo, un controllo a mano delle citazioni escluse dal filtro sul contesto.
