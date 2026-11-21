# Quanto ci si può fidare dei dati: i controlli di qualità

Questo file riassume tutti i controlli fatti per sapere se i dati ricavati dai testi sono giusti: le citazioni tra pronunce, i nomi di chi ha scritto, i collegi. È scritto a mano partendo dai report prodotti dai programmi, che restano la fonte di ogni numero: `validation_round1.md`, `validation_test.md`, `validation_test2.md` (prodotti da `src/validation/evaluate.py`), `judges_quality.md` (`src/judges/build_judges.py`), `sparql_reconciliation.md` (`src/ingest/sparql_check.py`), `collegio_vs_sedute.json` (`src/ingest/fetch_api.py`).

## 1. Le citazioni estratte dai testi

**Che cosa si misura.** Due cose:

- la **precisione**: delle citazioni trovate dal programma, quante sono vere. Se ne trova 100 e 95 sono vere, la precisione è 0,95;
- il **richiamo**: delle citazioni vere, quante ne trova. Se nel testo ce ne sono 100 e ne trova 90, il richiamo è 0,90.

Le soglie, decise prima, erano una precisione di almeno 0,95 e un richiamo di almeno 0,90. Si contano le coppie "pronuncia che cita – pronuncia citata" nel testo di base (il ragionamento della Corte e il dispositivo). Tra parentesi c'è l'intervallo di confidenza al 95%, cioè i valori compatibili con i dati, dato che i campioni sono piccoli (calcolato con il metodo di Wilson).

**Chi ha deciso quali citazioni sono vere.** L'assistente automatico (Claude), non una persona. Ha letto i testi prima di far girare il programma sul campione, ma solo i passi che contengono una parola chiave (come "sentenza" o "ordinanza") o un rimando, non i testi interi (`src/validation/sample_passages.py`). È il punto debole di tutta la misura: le parole chiave somigliano a quelle che usa il programma, quindi una citazione scritta in un modo che nessuno dei due riconosce sfuggirebbe a entrambi, e il richiamo risulterebbe più alto del vero. Le citazioni giudicate vere sono elencate, pronuncia per pronuncia, in `data/validation/gold_test.txt` e `gold_test2.txt`.

| Passo | Campione | Pronunce | Citazioni vere | Precisione | Richiamo | File |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Primo campione, tutti i decenni (seme 20261117) | 64 | 270 | 1,000 (0,985–1,000) | 0,941 (0,906–0,963) | `validation_round1.md` |
| 1 | di cui fino alla pronuncia 286/1986 | 27 | 40 | 1,000 (0,886–1,000) | **0,750** (0,598–0,858): sotto la soglia | `validation_round1.md` |
| 1 | di cui dal 1987 | 37 | 230 | 1,000 (0,983–1,000) | 0,974 (0,944–0,988) | `validation_round1.md` |
| 2 | Il programma è stato corretto per le forme antiche di citazione (per esempio "12/1957" senza "n.", elenchi con più date, "in pari data", i due punti come separatore) | | | | | `src/extract/citations.py` |
| 3 | Secondo campione, mai visto prima, solo fino alla 286/1986 | 48 | 72 | 0,985 (0,920–0,997) | 0,917 (0,830–0,961) | `validation_test2.md` |

**Come si legge la tabella.**

- Le stime da usare sono due: **dal 1987, richiamo 0,974** (passo 1); **fino al 1986, richiamo 0,917** (passo 3). La precisione è almeno 0,985 in entrambi i periodi.
- Il file `validation_test.md` ricalcola il primo campione dopo la correzione (richiamo 0,978). Non è una stima indipendente, perché la correzione è stata scritta guardando proprio gli errori di quel campione: serve solo a controllare che la correzione non abbia rotto altro (nessuna citazione trovata per errore in più).
- Per i testi fino al 1986 il valore stimato supera la soglia, ma il limite inferiore dell'intervallo (0,830) sta sotto 0,90: con 72 citazioni non si può escludere che il richiamo vero sia sotto la soglia.
- `validation_round1.md` è la fotografia della prima misura, fatta con il programma prima della correzione: con il codice attuale non si può rifare.
- Rispetto al piano, le citazioni controllate sono 342 invece delle 460 previste.
- Le 6 citazioni mancate nel secondo campione e l'unica citazione trovata per errore sono elencate in `validation_test2.md`.

**Il controllo di una persona, ancora da fare.** `data/validation/human_check.md` contiene 36 pronunce mai usate prima (seme 20261119), con tutto il testo di base e senza il risultato del programma: 3 pronunce per decennio e tipo negli anni 1950–1980, scendendo a 1 negli anni 2010–2020, per circa 100 citazioni attese. Una persona scrive le citazioni che trova in `data/validation/gold_human.txt` (le istruzioni sono in testa al foglio); poi il comando `.venv/bin/python src/validation/evaluate.py human` calcola precisione e richiamo e scrive `reports/validation_human.md`. Con circa 100 citazioni il controllo può smentire le soglie, ma non confermarle con sicurezza: il limite inferiore dell'intervallo supera 0,95 solo con 100 citazioni giuste su 100, e 0,90 solo con almeno 97 su 100. Finché il controllo non è fatto, precisione e richiamo restano quelli stimati dall'assistente.

## 2. Giudici: chi ha scritto e chi sedeva nel collegio

| Controllo | Risultato | Soglia decisa prima |
| --- | --- | --- |
| Nome di chi ha scritto collegato all'elenco ufficiale dei giudici | 99,84% delle pronunce | 98% |
| Collegio riconosciuto per intero (da 11 a 15 giudici, tutti collegati all'elenco) | 98,85% | 98% |
| Nome del relatore collegato all'elenco | 99,95% | |

Da dove viene il nome di chi ha scritto: dal campo dei dati in 8.384 pronunce, dalla firma in fondo al testo in 8.349, dal relatore usato al suo posto in 5.678 (fino alla 286/1986); in 16 pronunce non c'è.

## 3. Il confronto con la banca dati SPARQL della Corte

La Corte ha anche una banca dati interrogabile da un programma (con il linguaggio SPARQL), separata dai file scaricati: è una seconda fonte ufficiale con cui confrontare i dati.

| Controllo | Risultato |
| --- | --- |
| Relatore: file scaricati contro banca dati, 22.426 pronunce | Coincide nel 97,12% dei casi; 635 delle 645 differenze sono due errori di grafia nei file ("Caianello" per Caianiello, "Capolozza" per Capalozza), corretti nel codice |
| Collegio ricavato dal testo contro i giudici presenti all'udienza, 3.684 pronunce dal 2004 | Il 97,8% dei giudici del collegio risulta presente all'udienza; il 99,1% dei presenti all'udienza risulta nel collegio; i due elenchi sono identici nel 73,5% delle pronunce |

Collegio e udienza non devono coincidere sempre: in un'udienza si discutono più cause, e un giudice può non partecipare a tutte. Per questo conta la quota di giudici in comune, non la quota di elenchi identici.
