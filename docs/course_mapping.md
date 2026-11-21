# Il programma d'esame, punto per punto

> Questo documento prende ogni argomento del programma del corso e dice se il progetto lo usa e dove, oppure perché no. "Usato" vuol dire che esistono il programma che fa il calcolo, il file con i risultati e la sezione della relazione (`reports/relazione_for_dummies.md`) che lo racconta. Aggiornato il 21/11/2026.

## Da dove viene l'elenco degli argomenti

- **Il programma ufficiale** del corso EM1421 per il 2026/27 ([pagina del corso](https://www.unive.it/data/insegnamento/790312/programma), letta il 18/11/2026; "programma definitivo", ultima modifica 26/06/2026) elenca sei voci, senza dettagli: introduzione alla data science e alla social media analysis; social network analysis; lavorare con API; data and information visualisation; topic extraction; sentiment analysis. Aggiunge che cosa lo studente deve saper fare alla fine, che cosa deve sapere prima, e due libri di testo, senza indicare i capitoli.
- **Gli argomenti più precisi** (concetti, misure, modelli) vengono quindi dagli indici dei due libri, letti il 18/11/2026: Easley e Kleinberg, *Networks, Crowds, and Markets* (2010, [versione degli autori](https://www.cs.cornell.edu/home/kleinber/networks-book/)); Barabási, *Network Science* (2016, [networksciencebook.com](http://networksciencebook.com/)).
- **Non vengono dall'elenco delle lezioni**, che sta su Moodle e non è stato visto. Questa mappa va confrontata con le slide del corso: a lezione gli argomenti possono essere di meno, o diversi.
- **Che cosa dei libri è stato letto.** Gli indici, e per intero solo le parti citate nella relazione: Easley e Kleinberg §14.5 (18/11/2026), capitoli 5 e 20 (20/11/2026); Barabási §3.8–3.10 (20/11/2026). Per gli altri argomenti le spiegazioni qui sotto sono nostre, e un capitolo va letto prima di citarlo nella relazione (`docs/sources.md`).

## 1. Le sei voci del programma

| Voce | Usata? | Dove | Spiegazione |
| --- | --- | --- | --- |
| Introduzione alla data science e alla social media analysis | La data science sì; i dati dei social network no | I programmi che scaricano i dati e ne annotano la versione (`src/ingest/`), che trovano le citazioni nei testi (`src/extract/`) e che ne misurano la qualità (`src/validation/`); relazione, sezioni 1–2 | I dati sono dati aperti di una corte, non dati di social network: il tema va concordato con il docente (`docs/decisions.md`). L'unica misura dell'attenzione sul web è quanto le pronunce sono citate su Wikipedia (sezione 3.7) |
| Social network analysis | Sì | `src/networks/build.py` costruisce le reti; le analisi sono in `src/analysis/` (`d1_pronunce.py`, `d2_d4_giudici.py`, `d3_memoria_collegiale.py`, `extras.py`, `course_measures.py`); relazione, sezioni 2.6, 2.8 e 3 | Il dettaglio, concetto per concetto, è nella parte 3 di questo documento |
| Lavorare con API | Sì | `src/ingest/sparql_check.py` e `fetch_api.py`, con i risultati in `data/processed/esiti.csv`, `data/interim/sedute_membri.csv`, `data/processed/wikipedia_links.csv`, `reports/api_fetch.json`, `reports/sparql_reconciliation.md`; relazione, sezioni 1.1, 2.5 e 3.7 | Due servizi interrogati da un programma: la banca dati della Corte (domande scritte nel linguaggio SPARQL, risposte in formato JSON), per l'esito delle pronunce, i giudici presenti alle udienze e il controllo del relatore; l'interfaccia di Wikipedia (MediaWiki), per sapere quali voci citano una pronuncia, scorrendo i risultati pagina per pagina |
| Data and information visualisation | Sì | `src/analysis/figures.py` disegna le 10 figure in `reports/figures/`; `src/analysis/interactive.py` produce `reports/rete_interattiva.html`, una rete da esplorare nel browser (le pronunce sono disposte con un metodo che avvicina quelle collegate, detto di Fruchterman e Reingold); relazione, figure 1–10 e sezione 3.2 | Ogni figura ha un titolo che dice il risultato e mostra sempre l'incertezza (`docs/project_guide.md`, sezione 3) |
| Topic extraction | Sì | `src/analysis/topics.py`, con i risultati in `reports/topics.md`, `reports/topics.json`, `data/processed/topics_pronunce.csv`; relazione, sezione 2.7 | Un programma (modello LDA) raggruppa in temi le parole delle massime che compaiono spesso insieme. Il numero di temi è scelto con una misura di quanto le parole di un tema stanno insieme (coerenza NPMI); la stabilità è controllata ripetendo il calcolo 5 volte; i temi sono confrontati con i titoli delle massime e con gli articoli della Costituzione invocati. Serve come controllo della materia in D2 e D3 e per capire i filoni della rete. Dal 19/11 la materia si controlla anche con gli articoli della Costituzione (`src/analysis/parametri.py`; relazione, sezioni 3.4 e 3.5) |
| Sentiment analysis | Usata come metodo, con esito negativo | `src/polarity/` (estrazione dei passi, regole, campione letto alla cieca, valutazione), con i risultati in `reports/polarity_validation_claude.md`; relazione, sezione 3.9 | Adattata a una corte su decisione di Umberto (18/11/2026): la polarità delle citazioni, cioè se una pronuncia prende le distanze da un precedente che cita. Le regole hanno una precisione di 0,76 (intervallo 0,60–0,87), sotto la soglia di 0,80 decisa prima, quindi non sono state usate nelle analisi. Il foglio per il controllo di una persona è `data/validation/polarity_human_check.md` |

## 2. Che cosa lo studente deve saper fare, e che cosa deve sapere prima

| Dal programma | Usato? | Dove |
| --- | --- | --- |
| Gestire, elaborare, visualizzare e interpretare grandi quantità di dati | Sì | 22.427 pronunce in formato XML, 155.982 menzioni di precedenti, 46.658 massime; relazione, sezioni 1–3 |
| Usare tecniche di data science su dati del web e dei social network | In parte | Dati del web: il portale della Corte, la sua banca dati SPARQL, Wikipedia. Dati dei social network: nessuno |
| Conoscere i metodi della social network analysis e le loro basi teoriche | Sì | Parte 3 di questo documento |
| Lavorare con dati strutturati (in campi) e non strutturati (testo libero) | Sì | Strutturati: i campi dei file XML. Non strutturati: il testo delle motivazioni, da cui si ricavano le citazioni, e quello delle massime, da cui si ricavano i temi |
| Usare software e linguaggi di programmazione adatti | Sì | Python, con le librerie pandas, igraph, networkx, leidenalg, scikit-learn, statsmodels, lifelines, powerlaw, matplotlib (`requirements.lock`). Il corso potrebbe chiedere R: la migrazione è prevista dopo la fine del lavoro |
| Interpretare i risultati in modo critico e comunicarli con rigore | Sì | Ogni risultato è confrontato con ciò che darebbe il caso (sezione 2.8); i limiti sono elencati (sezione 4); è detto che cosa era deciso prima e che cosa è cambiato dopo (sezione 2.9; date e motivi in `docs/decisions.md`) |
| Leggere la documentazione tecnica di strumenti e librerie | Sì | La descrizione ufficiale dei file del portale (`docs/data_schema.md`), la banca dati SPARQL (`reports/sparql_reconciliation.md`), l'interfaccia di Wikipedia |
| Prerequisiti: programmazione, statistica descrittiva, probabilità, inferenza | Usati | Parte 4 di questo documento |

## 3. Concetti, misure e modelli dei libri di testo

### Barabási, *Network Science*

| Capitolo e concetto, in breve | Usato? | Dove, oppure perché no |
| --- | --- | --- |
| 2. Grado (quanti legami ha un nodo), grado medio, distribuzione dei gradi | Sì | `network_basic.json`, `d1_results.json`; sezioni 3.1 e 3.2, figura 3 |
| 2. Matrice di adiacenza (la tabella di chi è collegato a chi) | Sì | HITS e PageRank fanno i conti sulla tabella delle citazioni (`d1_pronunce.py`); sezione 2.8 |
| 2. Reti rade (pochi legami rispetto a quelli possibili) | Sì | Densità 0,00037 (`network_basic.json`); sezione 3.1 |
| 2. Reti pesate (i legami hanno un valore) | Sì | La rete tra giudici, pesata con il numero di citazioni (`edges_judges.csv`); sezioni 2.6 e 3.6 |
| 2. Reti con due tipi di nodi e loro proiezioni | Sì | Giudici e pronunce (chi ha scritto, chi sedeva), e da lì la rete tra giudici (`build.py`); sezione 2.6 |
| 2. Cammini e distanze | Sì | La catena più lunga, 148 anelli (`network_basic.json`); la distanza media (`course_measures.json`); sezioni 3.1 e 3.8 |
| 2. Connessione (quali nodi si raggiungono) | Sì | Il blocco principale, 86% delle pronunce (`network_basic.json`); sezioni 3.1 e 3.8 |
| 2. Coefficiente di clustering (quanti triangoli sono chiusi) | Sì | Sulla rete senza verso, confrontato con reti rimescolate (`course_measures.json`); sezione 3.8. Con il verso non ha senso, perché una pronuncia cita solo il passato |
| 3. Rete casuale (modello di Erdős–Rényi) | Usata come termine di confronto | Distanze e clustering confrontati con una rete a caso con gli stessi nodi e lo stesso numero di legami (`course_measures.json`); sezione 3.8 |
| 3. Distribuzione di Poisson | In parte | Quando le citazioni vanno a caso, il numero di citazioni ricevute segue quasi una distribuzione di Poisson; la distanza tra questa e la rete vera è proprio la misura della concentrazione; sezione 3.2 |
| 3. Blocco principale e transizioni di fase | In parte | Il blocco principale è misurato (sezioni 3.1 e 3.8). Le transizioni di fase no: la rete non nasce aggiungendo legami a caso |
| 3. Piccolo mondo | Sì | `course_measures.json`; sezione 3.8. Letti §3.8, §3.9 e il box 3.9 sul modello di Watts e Strogatz |
| 4. Leggi di potenza e reti "senza scala" | Sì | Test di Clauset, Shalizi e Newman, che confronta la legge di potenza con la lognormale (`d1_results.json`); sezione 3.2 |
| 4. Hub (nodi con moltissimi legami) | Sì | Le pronunce più citate; sezione 3.2 |
| 4. Stima dell'esponente della legge di potenza | Sì | 2,92, dalle pronunce con almeno 10 citazioni (`d1_results.json`); sezione 3.2 |
| 4. Grafici delle leggi di potenza | Sì | Figura 3 |
| 4. Distanze "ultra-piccole" | No | Valgono per le reti "senza scala", che i dati non sostengono (sezione 3.2) |
| 4. Reti con una distribuzione dei gradi data (modello di configurazione) | Usato come confronto con il caso | Citazioni scambiate tra pronunce in modo che ognuna conservi quante ne fa e quante ne riceve (`d1_pronunce.py`, `swap_null`); sezione 2.8 |
| 5. Crescita e attaccamento preferenziale ("chi è ricco diventa più ricco") | Sì | L'esponente di attaccamento (`course_measures.json`); sezione 3.8 |
| 5. Misurare l'attaccamento; attaccamento non proporzionale | Sì | Lo stesso esponente dice se le nuove citazioni crescono in proporzione a quelle già ricevute, di più o di meno; sezione 3.8 |
| 5. Perché nasce l'attaccamento preferenziale | Non come modello | Se ne parla (sezione 3.8), non si simula |
| 5. Distanze e clustering del modello di Barabási–Albert | No | La rete non si confronta con questo modello: le citazioni invecchiano (sezione 3.3), e il modello non lo prevede |
| 6. Fitness (l'attrattiva propria di un nodo, modello di Bianconi–Barabási) | No | Con questi dati l'attrattiva propria di una pronuncia e l'effetto "ricco diventa più ricco" non si separano; è detto come limite (sezione 3.8) |
| 6. Reti che invecchiano | Sì | Quanto a lungo un precedente resta citato (`d1_results.json`); sezione 3.3, figura 5 |
| 6. Condensazione di Bose–Einstein (un nodo prende quasi tutto) | No | Nessuna pronuncia prende una quota grande delle citazioni: la più citata ne ha 113 su 93.467 |
| 7. Assortatività (i nodi molto collegati si collegano tra loro?) | Sì | Confrontata con le reti a citazioni scambiate (`course_measures.json`); sezione 3.8 |
| 7. Limiti strutturali; generare reti con queste correlazioni | No | Contano quando ci sono hub enormi, qui assenti |
| 8. Robustezza: che cosa succede togliendo nodi (percolazione) | Sì | Si tolgono le pronunce più citate e, per confronto, pronunce a caso (`course_measures.json`); sezione 3.8 |
| 8. Guasti a catena | No | Nella rete non passa nulla che possa guastarsi |
| 9. Gruppi di nodi (comunità) e modularità | Sì | Metodo di Leiden (`extras.py`, `communities.csv`); sezione 3.2 |
| 9. Raggruppamento gerarchico | No | Leiden e Infomap sono più adatti a 22.000 nodi |
| 9. Gruppi che si sovrappongono | No | Ogni pronuncia sta in un filone; la sovrapposizione per materia la danno i temi, perché una pronuncia può averne più di uno |
| 9. Verificare e descrivere i gruppi | Sì | La modularità è confrontata con 100 reti rimescolate; i gruppi sono confrontati con i temi e con un secondo metodo (Infomap); per ogni gruppo dimensione, anno e tema prevalente (`extras.json`, rete interattiva); sezione 3.2 |
| 10. Diffusione, epidemie, vaccinazione | No | Una citazione non è un contagio con stati che si osservano (sano, infetto): non c'è un processo di diffusione da seguire |

### Easley e Kleinberg, *Networks, Crowds, and Markets*

| Capitolo e concetto, in breve | Usato? | Dove, oppure perché no |
| --- | --- | --- |
| 2. Grafi: cammini, connessione, distanza, ricerca in ampiezza | Sì | Sezioni 3.1 e 3.8 |
| 2. Dati di reti reali | Sì | Sezione 1 |
| 3. Chiusura dei triangoli (se A conosce B e C, B e C tendono a conoscersi) | Sì | Clustering sulla rete senza verso, confrontato con reti rimescolate (`course_measures.json`); sezione 3.8 |
| 3. La forza dei legami deboli | No | Tra pronunce un legame non ha forza (una coppia conta una volta). Tra giudici sì, ma l'idea di Granovetter riguarda come circolano le informazioni tra persone, non le citazioni tra testi |
| 3. Buchi strutturali e capitale sociale (chi fa da ponte tra gruppi) | In parte | Le pronunce ponte tra filoni, misurate con la betweenness (`course_measures.json`); sezione 3.8. Il capitale sociale dei giudici no: i dati non dicono come i giudici interagiscono |
| 3. Betweenness e divisione di un grafo | Sì | Betweenness nella sezione 3.8; divisione con Leiden e Infomap nella sezione 3.2 |
| 4. Omofilia (ci si lega a chi è simile) | Sì | D4 (`d4_results.json`); sezione 3.6 |
| 4. Selezione e influenza sociale | No | Con una rete che accumula tutto il tempo non si distinguono. D3 però separa l'esposizione a un precedente (sedere nel collegio) dallo scriverlo |
| 4. Reti di affiliazione (persone legate agli eventi a cui partecipano) | Sì | I collegi legano i giudici alle decisioni a cui partecipano; usati in D3; sezioni 2.6 e 3.4 |
| 4. Legami online; segregazione nello spazio | No | Non ci sono dati online sui giudici né una dimensione nello spazio |
| 5. Legami positivi e negativi, equilibrio strutturale | No | Il segno dei legami doveva venire dalla polarità delle citazioni (sezione 3.9), che non ha superato la soglia di qualità: l'analisi, decisa prima con un numero minimo di triangoli, non si è fatta. Capitolo letto (pp. 119–152): la teoria riguarda legami senza verso, e con legami con verso le sue previsioni possono non valere (§5.3, p. 128); per le citazioni andrebbe adattata |
| 13. Il web come rete con verso | Sì | La rete delle citazioni ha un verso e non ha cicli; sezione 2.6 |
| 13. Struttura "a farfallino" del web | No | Richiede gruppi di nodi che si raggiungono a vicenda seguendo il verso, impossibili in una rete senza cicli |
| 14. Hub e authority (HITS) | Sì | D1 (`d1_results.json`); sezione 3.2 |
| 14. PageRank | Sì | Variante di D1; sezione 3.2 |
| 14. Applicazioni oltre il web | Sì | È l'impianto del progetto: il §14.5 del libro tratta proprio le citazioni tra sentenze |
| 14. Analisi spettrale e passeggiate a caso | In parte | HITS e PageRank si calcolano proprio così; nessun'altra analisi di questo tipo |
| 16. Cascate informative (ognuno segue chi ha scelto prima) | No | Servono scelte in sequenza con informazioni private osservabili; una citazione non lo è |
| 18. Leggi di potenza | Sì | Sezione 3.2 |
| 18. Modelli "chi è ricco diventa più ricco" | Sì | Attaccamento preferenziale; sezione 3.8 |
| 18. Imprevedibilità del successo | In parte | Si misura quanto le citazioni passate prevedono quelle future (`d1_results.json`, voce "prediction"; sezione 3.2). Il fenomeno di cui parla il libro (letto solo il titolo) non è stato usato |
| 18. Coda lunga | In parte | La parte della distribuzione con le pronunce poco citate: il 29,5% non è mai citato (sezione 3.2). Il concetto del libro, che dal titolo riguarda i mercati, non è stato usato |
| 19. Comportamenti che si diffondono a catena | No | Non c'è un comportamento che si adotta |
| 20. Piccolo mondo: sei gradi di separazione | Sì | Sezione 3.8. Capitolo letto (pp. 611–644) |
| 20. Ricerca senza mappa (trovare un bersaglio passando di mano in mano) | No | Nessuno cerca un bersaglio muovendosi nella rete |
| 20. Strutture centro-periferia | No | Possibile in futuro, scomponendo la rete in strati sempre più interni (k-core) |
| 21. Epidemie | No | Come per Barabási, capitolo 10 |
| Teoria dei giochi (capitoli 6–9), mercati e scambi su reti (10–12), aste della pubblicità (15), effetti di rete (17), mercati e informazione, voto, diritti di proprietà (22–24) | Fuori dal programma | Il programma del corso non li elenca, e non hanno legame con questi dati |

## 4. Metodi statistici usati

| Metodo, in breve | Dove |
| --- | --- |
| Statistica descrittiva: indice di Gini (disuguaglianza), quantili, distribuzioni | D1 (sezioni 3.1–3.2) |
| Intervalli di confidenza (l'insieme dei valori compatibili con i dati): di Wilson per le proporzioni, ricampionando i dati (bootstrap), con incertezza raggruppata | Qualità dell'estrazione (sezione 2.4), D1, D2, D3 |
| Confronti con il caso (dati rimescolati), da 100 a 10.000 ripetizioni, sempre con lo stesso seme | D1, D2, D4, misure dei libri di testo (sezioni 2.8 e 3.8) |
| Correzione per molti confronti insieme (Holm) | D2, D4 (sezioni 3.5 e 3.6) |
| Regressione logistica condizionata, con calcolo esatto | D3 (sezione 3.4) |
| Regressione binomiale negativa (un modello per contare eventi) | Previsione in D1, attaccamento preferenziale (sezioni 3.2 e 3.8) |
| Curve di sopravvivenza (Kaplan–Meier) | Durata dei precedenti (sezione 3.3) |
| Test di Mann–Whitney (confronta due gruppi senza assumere una forma) | Esito (sezione 3.7) |
| Informazione mutua normalizzata (accordo tra due classificazioni, da 0 a 1) | Temi e gruppi (sezioni 2.7 e 3.2) |
| Potenza calcolata simulando (la probabilità di accorgersi di un effetto) | D4 (sezione 3.6) |

## 5. Che cosa resta da decidere

- **Sentiment.** Affrontato il 18/11/2026 con la polarità delle citazioni (sezione 3.9): le regole non hanno superato la soglia (precisione 0,76 contro 0,80). Una seconda versione andrebbe decisa prima e provata su dati mai visti, con la lettura di una persona.
- **Dati dei social network.** Non ce ne sono: il tema resta da concordare con il docente.
- **Elenco delle lezioni.** Questa mappa va confrontata con le slide del corso su Moodle.
