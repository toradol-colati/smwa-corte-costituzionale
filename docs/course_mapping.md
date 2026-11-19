# Il programma d'esame, punto per punto

> Per ogni argomento: se è applicato, dove (script → file dei risultati → sezione della relazione `reports/relazione_for_dummies.md`); se non lo è, perché. "Applicato" vale solo se esistono lo script, il file dei risultati e la sezione della relazione. Aggiornato il 18/11/2026.

## Da dove viene l'elenco

- **Il programma ufficiale** di EM1421 per il 2026/27 ([pagina del corso](https://www.unive.it/data/insegnamento/790312/programma), letta il 18/11/2026, "programma definitivo", ultima modifica 26/06/2026) elenca sei voci senza sotto-argomenti: introduzione alla data science e alla social media analysis; social network analysis; lavorare con API; data and information visualisation; topic extraction; sentiment analysis. Aggiunge i risultati di apprendimento attesi, i prerequisiti e due libri di testo, senza indicare capitoli.
- **Concetti, misure e modelli più fini** vengono quindi dagli indici dei due libri, letti il 18/11/2026: Easley e Kleinberg, *Networks, Crowds, and Markets* (2010, [versione degli autori](https://www.cs.cornell.edu/home/kleinber/networks-book/)); Barabási, *Network Science* (2016, [networksciencebook.com](http://networksciencebook.com/)).
- **Non vengono dall'elenco delle lezioni**, che sta su Moodle e non è stato visto. Questa mappa va confrontata con le slide del corso: gli argomenti trattati a lezione possono essere di meno, o diversi.
- **Dei libri sono stati letti gli indici** (e il §14.5 di Easley e Kleinberg), non i capitoli: le descrizioni dei concetti qui sotto sono nostre, e un capitolo va letto prima di citarlo nella relazione (`docs/sources.md`).

## 1. Le sei voci del programma

| Voce | Stato | Dove | Note |
| --- | --- | --- | --- |
| Introduzione alla data science e alla social media analysis | Data science: applicato. Dati social: no | Pipeline dai dati grezzi: `src/ingest/` (download con manifest e impronte, lettura dell'XML), `src/extract/` (estrazione delle citazioni dal testo), `src/validation/` (precisione e richiamo); relazione §1–2 | I dati sono open data di una corte, non dati social: il tema va concordato con il docente (`docs/decisions.md`). L'unica misura di attenzione sul web sono i link da Wikipedia (§3.7) |
| Social network analysis | Applicato | `src/networks/build.py`, `src/analysis/d1_pronunce.py`, `d2_d4_giudici.py`, `d3_memoria_collegiale.py`, `extras.py`, `course_measures.py`; relazione §2.6, §2.8, §3 | Dettaglio concetto per concetto nella parte 3 |
| Lavorare con API | Applicato | `src/ingest/sparql_check.py` e `fetch_api.py` → `data/processed/esiti.csv`, `data/interim/sedute_membri.csv`, `data/processed/wikipedia_links.csv`, `reports/api_fetch.json`, `reports/sparql_reconciliation.md`; relazione §1.1, §2.5, §3.7 | Endpoint SPARQL della Corte (query in SPARQL, risposte in JSON) per l'esito, i membri delle sedute e il controllo del relatore; API di MediaWiki (`list=exturlusage`, paginazione con `continue`) per i link da Wikipedia |
| Data and information visualisation | Applicato | `src/analysis/figures.py` → `reports/figures/` (10 figure); `src/analysis/interactive.py` → `reports/rete_interattiva.html` (rete esplorabile, disposizione a forze di Fruchterman e Reingold); relazione, figure 1–10 e §3.2 | Regole delle figure in `docs/project_guide.md`, §3: un titolo che dice il risultato, intervalli sempre visibili |
| Topic extraction | Applicato | `src/analysis/topics.py` → `reports/topics.md`, `reports/topics.json`, `data/processed/topics_pronunce.csv`; relazione §2.7 | LDA sulle massime: scelta del numero di temi con la coerenza NPMI, stabilità su 5 seed, verifica con i titoli e con i parametri costituzionali. Usata come controllo in D2 e D3 e per leggere le comunità. Dal 19/11 la materia si controlla anche con gli articoli della Costituzione invocati nelle massime (`src/analysis/parametri.py`; relazione §3.4, §3.5) |
| Sentiment analysis | Applicato come metodo, con esito negativo | `src/polarity/` (contesti, lessico, campione alla cieca, valutazione) → `reports/polarity_validation_claude.md`; relazione §3.9 | Forma adattata decisa da Umberto il 18/11/2026: la polarità delle citazioni (distinzione o distacco da un precedente). Il lessico ha precisione 0,76 (0,60–0,87), sotto la soglia di 0,80 fissata prima: nessuna analisi sui dati. Foglio per il controllo di una persona: `data/validation/polarity_human_check.md` |

## 2. Risultati di apprendimento attesi e prerequisiti

| Dal programma | Stato | Dove |
| --- | --- | --- |
| Gestire, elaborare, visualizzare e interpretare grandi volumi di dati | Applicato | 22.427 pronunce in XML, 155.982 menzioni di precedenti, 46.658 massime; relazione §1–3 |
| Tecniche di data science su dati del web e dei social | In parte | Dati del web: portale open data, endpoint SPARQL, Wikipedia. Dati social: nessuno |
| Metodologie della social network analysis, con le basi teoriche | Applicato | Parte 3 |
| Dati strutturati e non strutturati | Applicato | Strutturati: i campi dell'XML. Non strutturati: il testo delle motivazioni (estrazione delle citazioni) e delle massime (topic) |
| Software e linguaggi di programmazione adeguati | Applicato | Python: pandas, igraph, networkx, leidenalg, scikit-learn, statsmodels, lifelines, powerlaw, matplotlib (`requirements.lock`) |
| Interpretare criticamente i risultati e comunicarli con rigore | Applicato | Un modello nullo per ogni statistica (§2.8), limiti (§6), il check del 17/11/2026 e le correzioni (`docs/decisions.md`) |
| Consultare la documentazione tecnica di strumenti e librerie | Applicato | DTD del portale (`docs/data_schema.md`), endpoint SPARQL (`reports/sparql_reconciliation.md`), API di MediaWiki |
| Prerequisiti: programmazione, statistica descrittiva, probabilità, inferenza | Applicati | Parte 4 |

## 3. Concetti, misure e modelli dei libri di testo

### Barabási, *Network Science*

| Capitolo e concetto | Stato | Dove, oppure perché no |
| --- | --- | --- |
| 2. Grado, grado medio, distribuzione dei gradi | Applicato | `network_basic.json`, `d1_results.json`; §3.1, §3.2, figura 3 |
| 2. Matrice di adiacenza | Applicato | HITS e PageRank lavorano sulla matrice delle citazioni (`d1_pronunce.py`); §2.8 |
| 2. Reti sparse | Applicato | Densità 0,00037 (`network_basic.json`); §3.1 |
| 2. Reti pesate | Applicato | Rete tra giudici pesata per numero di citazioni (`edges_judges.csv`); §2.6, §3.6 |
| 2. Reti bipartite e proiezioni | Applicato | Strati giudice–pronuncia (redazione, collegio) e loro proiezione nella rete tra giudici (`build.py`); §2.6 |
| 2. Cammini e distanze | Applicato | Catena più lunga, 148 (`network_basic.json`); distanza media (`course_measures.json`); §3.1, §3.8 |
| 2. Connessione | Applicato | Componente gigante, 86% (`network_basic.json`); §3.1, §3.8 |
| 2. Coefficiente di clustering | Applicato | Versione non orientata, contro un modello nullo (`course_measures.json`); §3.8. La versione orientata non ha senso in un grafo aciclico (`.claude/rules/network-analysis.md`) |
| 3. Modello di Erdős–Rényi | Applicato come riferimento | Distanze e clustering confrontati con un grafo casuale con gli stessi nodi e legami (`course_measures.json`); §3.8 |
| 3. Distribuzione di Poisson | In parte | Il nullo di D1, che ripesca a caso il bersaglio, produce gradi quasi di Poisson: la distanza dalla rete vera è la misura della concentrazione; §3.2 |
| 3. Componente gigante e transizioni di fase | In parte | Componente gigante misurata (§3.1, §3.8). Transizioni di fase no: la rete non si genera aggiungendo legami a caso |
| 3. Piccolo mondo | Applicato | `course_measures.json`; §3.8 |
| 4. Leggi di potenza e reti a invarianza di scala | Applicato | Test di Clauset, Shalizi e Newman, legge di potenza contro lognormale (`d1_results.json`); §3.2 |
| 4. Hub | Applicato | Le pronunce più citate; §3.2 |
| 4. Stima dell'esponente | Applicato | α = 2,92 da k = 10 in su (`d1_results.json`); §3.2 |
| 4. Grafici delle leggi di potenza | Applicato | Figura 3 |
| 4. Proprietà ultra-piccola | Non applicato | Presuppone una rete a invarianza di scala, che i dati non sostengono (§3.2) |
| 4. Reti con una distribuzione dei gradi data (modello di configurazione) | Applicato come modello nullo | Scambi di citazioni che conservano i gradi (`d1_pronunce.py`, `swap_null`); §2.8 |
| 5. Crescita e attaccamento preferenziale | Applicato | Esponente di attaccamento (`course_measures.json`); §3.8 |
| 5. Misurare l'attaccamento preferenziale; attaccamento non lineare | Applicato | Lo stesso esponente dice se l'attaccamento è lineare, sub- o superlineare; §3.8 |
| 5. Origini dell'attaccamento preferenziale | Non applicato come modello | Se ne discute (§3.8), non si simula |
| 5. Diametro e clustering del modello di Barabási–Albert | Non applicato | La rete non si confronta con il modello BA: la crescita delle citazioni ha anche l'invecchiamento (§3.3), che il modello BA non prevede |
| 6. Fitness (modello di Bianconi–Barabási) | Non applicato | Con questi dati l'attrattiva propria di una pronuncia e l'attaccamento preferenziale non si separano; lo si dichiara come limite dell'esponente (§3.8) |
| 6. Reti che evolvono: invecchiamento | Applicato | Curva di invecchiamento e durata dei precedenti (`d1_results.json`); §3.3, figura 5 |
| 6. Condensazione di Bose–Einstein | Non applicato | Nessuna pronuncia raccoglie una quota rilevante delle citazioni: la più citata ne ha 113 su 93.467 |
| 7. Assortatività e correlazioni di grado | Applicato | Contro il modello nullo degli scambi (`course_measures.json`); §3.8 |
| 7. Cut-off strutturali; generare reti correlate | Non applicato | Contano con hub enormi, qui assenti |
| 8. Percolazione e tolleranza agli attacchi | Applicato | Rimozione delle pronunce più citate contro rimozione casuale (`course_measures.json`); §3.8 |
| 8. Guasti a cascata | Non applicato | Nella rete non scorre nulla che possa guastarsi |
| 9. Comunità e modularità | Applicato | Leiden (`extras.py`, `communities.csv`); §3.2 |
| 9. Clustering gerarchico | Non applicato | Leiden e Infomap sono più adatti a 22.000 nodi |
| 9. Comunità sovrapposte | Non applicato | Ogni pronuncia sta in un filone; la sovrapposizione per materia la danno i topic (una pronuncia può averne più di uno) |
| 9. Verificare e caratterizzare le comunità | Applicato | Modularità contro 100 ricablaggi che conservano i gradi, confronto con i topic e con Infomap; dimensione, anno mediano, topic prevalente (`extras.json`, rete interattiva); §3.2 |
| 10. Fenomeni di diffusione, modelli epidemici, immunizzazione | Non applicato | Una citazione non è un contagio con stati osservabili (suscettibile, infetto): non c'è un processo di diffusione da seguire |

### Easley e Kleinberg, *Networks, Crowds, and Markets*

| Capitolo e concetto | Stato | Dove, oppure perché no |
| --- | --- | --- |
| 2. Grafi: cammini, connessione, distanza, ricerca in ampiezza | Applicato | §3.1, §3.8 |
| 2. Dataset di reti | Applicato | §1 |
| 3. Chiusura triadica | Applicato | Clustering non orientato contro il nullo (`course_measures.json`); §3.8 |
| 3. Forza dei legami deboli | Non applicato | Tra pronunce un legame non ha forza (una coppia conta una volta). Tra giudici la forza c'è, ma l'ipotesi di Granovetter riguarda la circolazione di informazioni tra persone, non le citazioni tra testi |
| 3. Buchi strutturali e capitale sociale | In parte | Le pronunce ponte tra filoni, misurate con la betweenness (`course_measures.json`); §3.8. Il capitale sociale dei giudici no: i dati non dicono come interagiscono |
| 3. Betweenness e partizione del grafo | Applicato | Betweenness §3.8; partizione con Leiden e Infomap §3.2 |
| 4. Omofilia | Applicato | D4 (`d4_results.json`); §3.6 |
| 4. Selezione e influenza sociale | Non applicato | Con una rete cumulata non si distinguono. D3 separa però l'esposizione a un precedente (sedere nel collegio) dalla scrittura (redigerlo) |
| 4. Reti di affiliazione | Applicato | Lo strato del collegio è una rete di affiliazione tra giudici e decisioni, usata in D3; §2.6, §3.4 |
| 4. Formazione dei legami online; segregazione spaziale | Non applicato | Nessun dato online sui giudici; nessuna dimensione spaziale |
| 5. Relazioni positive e negative, equilibrio strutturale | Non applicato | Il segno dei legami doveva venire dalla polarità delle citazioni (§3.9), che non ha superato la soglia di qualità: l'analisi, fissata prima con una soglia minima di triangoli, non si è fatta |
| 13. Il web come grafo orientato | Applicato | La rete delle citazioni è orientata e aciclica; §2.6 |
| 13. Struttura a farfallino (bow-tie) | Non applicato | In un grafo aciclico non ci sono componenti fortemente connesse: ogni nodo è una componente a sé |
| 14. Hub e authority (HITS) | Applicato | D1 (`d1_results.json`); §3.2 |
| 14. PageRank | Applicato | Variante di D1; §3.2 |
| 14. Applicazioni oltre il web | Applicato | È l'impianto del progetto: il §14.5 del libro tratta proprio le citazioni tra sentenze |
| 14. Analisi spettrale e passeggiate aleatorie | In parte | HITS e PageRank sono un autovettore e una passeggiata aleatoria; nessun'altra analisi spettrale |
| 16. Cascate informative | Non applicato | Servono decisioni in sequenza con un'informazione privata osservabile; una citazione non lo è |
| 18. Leggi di potenza | Applicato | §3.2 |
| 18. Modelli "chi è ricco diventa più ricco" | Applicato | Attaccamento preferenziale; §3.8 |
| 18. Imprevedibilità del successo | In parte | Si misura quanto le citazioni passate prevedono quelle future (`d1_results.json`, "prediction"; §3.2). Il fenomeno di cui parla il libro (letto solo il titolo) non è stato applicato |
| 18. Coda lunga | In parte | La coda della distribuzione delle citazioni: il 29,5% delle pronunce non è mai citato (§3.2). Il concetto del libro, che dal titolo riguarda la coda lunga dei mercati, non è applicato |
| 19. Comportamento a cascata nelle reti (diffusione con soglie) | Non applicato | Non c'è un comportamento che si adotta |
| 20. Piccolo mondo: sei gradi di separazione, struttura e casualità | Applicato | §3.8 |
| 20. Ricerca decentrata | Non applicato | Nessuno cerca un bersaglio muovendosi nella rete |
| 20. Strutture centro-periferia | Non applicato | Possibile in futuro con la decomposizione in k-core |
| 21. Epidemie | Non applicato | Come per Barabási, cap. 10 |
| Teoria dei giochi (capp. 6–9), mercati e scambi su reti (10–12), aste per la pubblicità (15), effetti di rete (17), mercati e informazione, voto, diritti di proprietà (22–24) | Fuori dal programma | Il programma del corso non li elenca, e non hanno legame con questi dati |

## 4. Metodi statistici (prerequisiti: statistica descrittiva, probabilità, inferenza)

| Metodo | Dove |
| --- | --- |
| Statistica descrittiva: indice di Gini, quantili, distribuzioni | D1 (§3.1–3.2) |
| Intervalli di confidenza: Wilson, bootstrap, errori robusti per gruppi | Validazione (§2.4), D1, D2, D3 |
| Modelli nulli e test di permutazione, da 100 a 10.000 ripetizioni con seed fisso | D1, D2, D4, misure del corso (§2.8, §3.8) |
| Correzione per test multipli (Holm) | D2, D4 (§3.5, §3.6) |
| Regressione logistica condizionata, verosimiglianza esatta | D3 (§3.4) |
| Regressione binomiale negativa | Previsione in D1, attaccamento preferenziale (§3.2, §3.8) |
| Analisi di sopravvivenza (Kaplan–Meier) | D1b (§3.3) |
| Test di Mann–Whitney | Esito (§3.7) |
| Informazione mutua normalizzata | Topic e comunità (§2.7, §3.2) |
| Potenza calcolata per simulazione | D4 (§3.6) |

## 5. Cosa resta da decidere

- **Sentiment.** Affrontato il 18/11/2026 con la polarità delle citazioni (§3.9): il lessico non ha superato la soglia (precisione 0,76 contro 0,80). Una seconda versione andrebbe fissata prima e provata su dati mai visti, con un'annotazione umana; il foglio per il controllo di questa versione è pronto.
- **Dati social.** Non ce ne sono: il tema resta da concordare con il docente.
- **Elenco delle lezioni.** Questa mappa va confrontata con le slide del corso su Moodle.
