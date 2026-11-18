---
paths:
  - "src/networks/**"
  - "src/analysis/**"
  - "notebooks/**"
---
# Regole metodologiche

## Reti
- Strato 1: pronuncia → precedente, diretto e datato. È un grafo aciclico: un ciclo è un errore da registrare, non un dato. Fanno eccezione, finché non si è verificato, le citazioni tra pronunce con la stessa data (`docs/context.md`, sezione 3).
- Strato 2: giudice → pronuncia redatta. Dal 2016 una pronuncia può avere più redattori (`.claude/rules/data.md`). Fino alla 286/1986 il redattore è approssimato dal relatore (`redattore_source = relatore_proxy`).
- Strato 3: giudice — pronuncia, per ogni membro del collegio.
- Rete derivata: giudice A → giudice B, con peso pari alle citazioni dalle pronunce redatte da A a quelle redatte da B. Le autocitazioni (A = B) si tengono separate.

## Metriche da non usare
- Reciprocità tra pronunce: zero per costruzione.
- Componenti fortemente connesse tra pronunce: in un grafo aciclico ogni nodo è una componente a sé.
- Clustering sulla rete diretta delle citazioni: usare la co-citazione o la versione non orientata.
- Metriche sulla sola rete dei collegi: è quasi completa, serve solo a controllare le opportunità.

## Incertezza
- Ogni risultato è una stima, un intervallo al 95% (dal modello o da bootstrap) e il valore atteso sotto il nullo.
- Randomizzazioni dei modelli nulli: almeno 1.000, seed fisso; riportare la distribuzione, non solo la media.
- Significatività: 0,05, bilaterale.

## Modelli nulli: uno per ogni statistica
Ogni risultato dichiara quale nullo ha usato.
- Coda delle citazioni ricevute (D1): i bersagli si rimescolano solo tra pronunce già depositate, conservando i gradi in uscita e la curva osservata delle citazioni per età del precedente. Non conservare i gradi in entrata: sono la statistica sotto verifica.
- Struttura oltre i gradi (co-citazione, comunità, authority HITS confrontate con le pronunce più citate): scambi di citazioni solo tra coppie con lo stesso anno della citante e della citata (Uzzi et al. 2013), ammessi solo se ogni citata resta depositata prima o lo stesso giorno della citante, che conservano citazioni ricevute, citazioni fatte ed età delle citazioni. Variante: Karrer e Newman (2009), che non conserva l'età delle citazioni.
- D1, authority e citazioni (`docs/spec.md`, Modelli nulli, punto 3):
  - HITS anno per anno sulla rete fino a *t*, con PageRank come variante;
  - percentile calcolato tra le pronunce dello stesso anno di deposito, da quando la rete ha 1.000 pronunce (1966); finestra di più anni come variante;
  - riportare la quota di authority nulle;
  - prima la replica di Agnoloni e Pagallo (sentenze in via incidentale fino al 2014), poi la rete completa, poi le sole sentenze. Se la replica non riesce si riporta come risultato, e i confronti successivi non dicono nulla sul loro lavoro;
  - previsione fuori campione: stima fino al 2010, verifica 2011–2025, criterio una riduzione della devianza di almeno il 2% con intervallo al 95% (bootstrap per pronuncia) che esclude lo zero.
- Giudici: influenza = citazioni osservate / citazioni attese. Per ogni pronuncia che cita, le attese si calcolano sull'insieme dei precedenti disponibili. Ogni precedente ha una probabilità di essere scelto proporzionale alla curva osservata delle citazioni per età, mai uniforme.
  - Il rapporto di ogni giudice va con il suo intervallo al 95%.
  - Test multipli: correzione di Holm sui valori p di tutti i giudici testati prima di dire che un giudice "fa scuola".
  - Si testano solo i giudici con il numero minimo di pronunce redatte registrato in `docs/decisions.md`.
- D4: test di permutazione degli attributi tra giudici in carica negli stessi anni. Si esegue solo se una simulazione fatta prima dà una potenza di almeno 0,80, con α = 0,05, per l'effetto minimo d'interesse registrato in `docs/decisions.md`. Altrimenti si omette e lo si dichiara.

## D3: memoria collegiale
- Dati: per ogni pronuncia che cita, tutti i precedenti citati più un campione casuale di precedenti disponibili non citati, con seed fisso. Il numero (50 o 100) si decide e si registra in `docs/decisions.md`.
- Modello: regressione logistica condizionata, uno strato per pronuncia che cita.
- Variabili del modello principale:
  - `self_drafted`: il redattore citante ha redatto il precedente;
  - `sat_not_drafted`: il redattore citante sedeva nel collegio del precedente senza redigerlo;
  - età del precedente con indicatori per classe di età, mai con un termine lineare;
  - materia.
- Identificazione: il collegio è quasi completo, quindi `sat_not_drafted` coincide quasi con "precedente successivo al giuramento del redattore", cioè con l'età. Due fonti di variazione:
  - assenze dal collegio, cioè precedenti decisi durante il mandato del redattore ma senza di lui: sono la base del risultato principale;
  - soglia del giuramento: tra redattori di anzianità diversa, un precedente della stessa età cade dentro o fuori dal mandato.
- **Risultato principale del progetto**, fissato prima di vedere i dati:
  - è l'odds ratio di `sat_not_drafted`, con intervallo al 95%;
  - si stima solo sui precedenti decisi durante il mandato del redattore citante (presente o assente), con `self_drafted`, classi di età e materia come controlli;
  - gli errori standard sono raggruppati per redattore citante.

  Il modello completo con la soglia del giuramento è secondario. Il risultato principale non si cambia dopo aver visto i dati.
- Riportare quante osservazioni sostengono ciascuna fonte di variazione, per esempio quante assenze ci sono, e descrivere le assenze per tipo di giudizio e materia.

## Censura
- Le pronunce recenti hanno avuto meno tempo per essere citate.
- Citazioni ricevute: finestre fisse dopo il deposito (durata da decidere in `docs/decisions.md`) o misure normalizzate per età.
- Durata di un precedente (D1b): analisi della sopravvivenza.
- Influenza dopo il mandato (D2): la stessa finestra dopo la cessazione per tutti i giudici, esclusi quelli che non l'hanno completata.

## Materia
- Si ricava dalle massime. Per le pronunce con più massime e materie diverse, la regola (materia prevalente o più etichette) si decide e si registra in `docs/decisions.md`.
- Prima di usarla, controllare la copertura delle massime per decennio e documentarla in `docs/data_schema.md`. Le pronunce senza materia si dichiarano, non si riempiono in silenzio.

## Distribuzioni
- Code pesanti con il metodo di Clauset, Shalizi e Newman (pacchetto `powerlaw`), confrontando con la lognormale. Mai stime a occhio sulla scala log-log.

## Robustezza: ripetere le analisi principali in sei varianti
Il testo di base è definito in `.claude/rules/data.md`. Le varianti:
- testo intero, compreso il «Ritenuto in fatto»;
- testo con le note editoriali;
- senza le ordinanze di correzione;
- senza le autocitazioni del redattore;
- separando i periodi prima e dopo il 2001;
- per D2 e D3, solo le pronunce dalla 287/1986 in poi, citanti e citate, cioè quelle con `redattore_source` diverso da `relatore_proxy`.

## Figure
- Generate da script in `reports/figures/`, con un titolo che dice il risultato.
