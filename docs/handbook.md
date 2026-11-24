# Il progetto in un unico documento

<!-- SEZIONI 0-10: in scrittura -->

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
