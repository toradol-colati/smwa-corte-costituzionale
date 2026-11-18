# Validazione: quadro d'insieme

Questo file riassume le verifiche di qualità. È scritto a mano a partire dai report generati dagli script, che restano la fonte di ogni numero: `validation_round1.md`, `validation_test.md`, `validation_test2.md` (`src/validation/evaluate.py`), `judges_quality.md` (`src/judges/build_judges.py`), `sparql_reconciliation.md` (`src/ingest/sparql_check.py`), `collegio_vs_sedute.json` (`src/ingest/fetch_api.py`).

## 1. Estrazione delle citazioni

Soglie fissate prima: precisione almeno 0,95, richiamo almeno 0,90, sulle coppie (pronuncia che cita, pronuncia citata) del testo di base. Intervalli al 95% di Wilson.

**Chi ha annotato.** Claude, prima di eseguire l'estrattore sul campione, leggendo solo i passi che contengono una parola chiave o un richiamo (`src/validation/sample_passages.py`), non i testi interi. Non è un'annotazione umana, e le parole chiave del filtro somigliano a quelle dell'estrattore: una citazione scritta in una forma che nessuno dei due riconosce sfuggirebbe a entrambi, e il richiamo risulterebbe più alto del vero. I file `data/validation/gold_test.txt` e `gold_test2.txt` elencano le citazioni annotate, pronuncia per pronuncia.

| Passo | Campione | Pronunce | Coppie vere | Precisione | Richiamo | File |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Primo campione di verifica, tutti i decenni (seed 20261117) | 64 | 270 | 1,000 (0,985–1,000) | 0,941 (0,906–0,963) | `validation_round1.md` |
| 1 | di cui fino alla 286/1986 | 27 | 40 | 1,000 (0,886–1,000) | **0,750** (0,598–0,858): sotto soglia | `validation_round1.md` |
| 1 | di cui dal 1987 | 37 | 230 | 1,000 (0,983–1,000) | 0,974 (0,944–0,988) | `validation_round1.md` |
| 2 | Estrattore corretto sulle forme antiche (forma "12/1957" senza "n.", elenchi con più date, "in pari data", due punti come confine) | | | | | `src/extract/citations.py` |
| 3 | Secondo campione, mai visto, solo fino alla 286/1986 | 48 | 72 | 0,985 (0,920–0,997) | 0,917 (0,830–0,961) | `validation_test2.md` |

Come leggere la tabella.

- Le stime valide sono due: **dal 1987, richiamo 0,974** (passo 1); **fino al 1986, richiamo 0,917** (passo 3). La precisione è almeno 0,985 in entrambi i periodi.
- Il file `validation_test.md` riporta il primo campione ricalcolato dopo la correzione (richiamo 0,978). Non è una stima indipendente: la correzione è stata scritta guardando proprio gli errori di quel campione. Serve solo a controllare che la correzione non abbia rotto altro (nessuna coppia falsa in più).
- Per i testi fino al 1986 la soglia è superata dalla stima, ma il limite inferiore dell'intervallo (0,830) sta sotto 0,90: con 72 coppie non si può escludere un richiamo sotto soglia.
- `validation_round1.md` è la fotografia della prima misura, fatta con l'estrattore prima della correzione: non si può rigenerare con il codice attuale.
- Scostamento dal piano: 342 coppie annotate, non le 460 previste.
- Le 6 coppie mancate nel secondo campione e l'unica coppia falsa sono elencate in `validation_test2.md`.

**Controllo umano, da fare.** `data/validation/human_check.md` contiene 36 pronunce mai usate prima (seed 20261119), con tutto il testo di base e senza il risultato dell'estrattore: da 3 pronunce per decennio e tipo negli anni 1950–1980 a 1 negli anni 2010–2020, per circa 100 coppie attese. Una persona annota le citazioni in `data/validation/gold_human.txt` (istruzioni in testa al foglio); poi `.venv/bin/python src/validation/evaluate.py human` scrive `reports/validation_human.md`. Finché questo non è fatto, precisione e richiamo restano quelli stimati da Claude.

## 2. Giudici

| Verifica | Risultato | Soglia |
| --- | --- | --- |
| Redattore abbinato all'anagrafica | 99,84% delle pronunce | 98% |
| Collegio riconosciuto per intero (11–15 giudici, tutti abbinati) | 98,85% | 98% |
| Relatore abbinato | 99,95% | |

Fonte del redattore: campo dei file 8.384 pronunce, firma nel testo 8.349, relatore come approssimazione 5.678 (fino alla 286/1986), nessuna 16.

## 3. Controlli con l'endpoint SPARQL della Corte

| Verifica | Risultato |
| --- | --- |
| Relatore: file contro endpoint, 22.426 pronunce | concordanza 97,12%; 635 delle 645 discordanze sono due errori di grafia nei file (Caianello, Capolozza), corretti nel codice |
| Collegio estratto dal testo contro membri della seduta, 3.684 pronunce dal 2004 | il 97,8% dei giudici del collegio risulta nella seduta; il 99,1% dei membri della seduta risulta nel collegio; insiemi identici nel 73,5% delle pronunce |

Il collegio e la seduta non devono coincidere sempre: in una seduta si discutono più cause e un giudice può non partecipare a tutte. Per questo il dato utile è la quota di giudici in comune, non la quota di insiemi identici.
