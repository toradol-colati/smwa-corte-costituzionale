---
paths:
  - "src/networks/**"
  - "src/analysis/**"
  - "notebooks/**"
---
# Regole di metodo per le reti e le analisi

Queste regole valgono quando si lavora sui programmi che costruiscono le reti e fanno le analisi.

## Le reti

- **Strato 1: pronuncia → precedente.** Ogni citazione va dalla pronuncia che cita a quella citata, e ha una data. Siccome si citano solo pronunce già uscite, la rete non può avere cicli (è un grafo aciclico): un ciclo è un errore da registrare, non un dato. Fanno eccezione, finché non è verificato, le citazioni tra pronunce con la stessa data (`docs/context.md`, sezione 3).
- **Strato 2: giudice → pronuncia che ha scritto.** Dal 2016 una pronuncia può avere più redattori (`.claude/rules/data.md`). Fino alla 286/1986 il redattore è approssimato dal relatore (`redattore_source = relatore_proxy`).
- **Strato 3: giudice — pronuncia**, per ogni giudice del collegio che l'ha decisa.
- **La rete tra giudici (derivata dalle altre):** giudice A → giudice B, con un peso pari al numero di citazioni dalle pronunce scritte da A a quelle scritte da B. Le citazioni di sé stessi (A = B) si tengono a parte.

## Le misure da non usare

- La reciprocità tra pronunce (quante citazioni vanno nei due sensi): è zero per costruzione, perché una pronuncia non può citarne una successiva.
- Le componenti fortemente connesse tra pronunce (gruppi in cui da ogni nodo si torna a sé seguendo le frecce): in una rete senza cicli ogni nodo è un gruppo a sé.
- Il clustering (quanti triangoli chiusi ci sono) sulla rete delle citazioni con il verso: si usa invece la co-citazione (due pronunce citate insieme dalla stessa pronuncia) o la rete senza verso.
- Le misure sulla sola rete dei collegi: è quasi completa, perché quasi tutti i giudici in carica siedono insieme. Serve solo a controllare le occasioni di citare.

## L'incertezza

- Ogni risultato è una stima con un intervallo al 95% (dal modello o dal bootstrap, cioè ripetendo il calcolo su campioni rifatti dai dati) e con il valore che ci si aspetterebbe per caso (sotto il modello nullo).
- I confronti con il caso si ripetono almeno 1.000 volte, partendo da un seme fisso; si riporta tutta la distribuzione dei risultati, non solo la media.
- Un risultato si dice statisticamente significativo al livello 0,05, con un test a due code (che guarda le differenze in tutti e due i sensi).

## I confronti con il caso: uno per ogni misura

Ogni risultato dice con quale confronto è stato fatto.

- **La coda delle citazioni ricevute (D1),** cioè quante pronunce sono citate moltissimo: si rimescolano le pronunce citate, solo tra quelle già depositate. Si conservano le citazioni fatte da ogni pronuncia e la curva osservata delle citazioni per età del precedente. Non si conservano le citazioni ricevute, perché sono proprio quello che si vuole verificare.
- **La struttura oltre i conteggi** (co-citazione, gruppi di pronunce, confronto tra le pronunce più autorevoli secondo HITS e le più citate): si scambiano le pronunce citate tra coppie di citazioni con lo stesso anno della pronuncia che cita e della pronuncia citata (Uzzi e altri, 2013). Uno scambio è ammesso solo se ogni pronuncia citata resta depositata prima, o lo stesso giorno, della pronuncia che la cita. Così si conservano le citazioni ricevute, le citazioni fatte e l'età delle citazioni. Variante: il modello di Karrer e Newman (2009), che non conserva l'età delle citazioni.
- **D1, autorevolezza e citazioni** (`docs/spec.md`, "Modelli nulli", punto 3):
  - HITS si calcola anno per anno, sulla rete fino a quell'anno; PageRank come variante;
  - la posizione di una pronuncia (il percentile) si calcola tra le pronunce depositate nello stesso anno, da quando la rete ha 1.000 pronunce (1966); una finestra di più anni come variante;
  - si riporta la quota di pronunce con autorevolezza zero;
  - prima si rifà il lavoro di Agnoloni e Pagallo (sentenze in via incidentale fino al 2014), poi si passa alla rete completa, poi alle sole sentenze. Se il loro risultato non si ritrova, lo si riporta come risultato, e i confronti successivi non dicono nulla sul loro lavoro;
  - la previsione su dati non usati per la stima: si stima fino al 2010 e si verifica sul 2011–2025. Il criterio: un miglioramento della devianza (una misura di quanto il modello sbaglia) di almeno il 2%, con un intervallo al 95% (bootstrap per pronuncia) che non comprende lo zero.
- **I giudici:** l'influenza di un giudice è il rapporto tra le citazioni osservate e quelle attese. Per ogni pronuncia che cita, le citazioni attese si calcolano su tutti i precedenti che poteva citare. Ogni precedente ha una probabilità di essere scelto proporzionale alla curva osservata delle citazioni per età, mai uguale per tutti.
  - Il rapporto di ogni giudice si riporta con il suo intervallo al 95%.
  - Siccome si provano molti giudici insieme, prima di dire che un giudice "fa scuola" si correggono i valori p di tutti i giudici provati con il metodo di Holm.
  - Si provano solo i giudici che hanno scritto almeno il numero minimo di pronunce scritto in `docs/decisions.md`.
- **D4:** si rimescolano gli attributi (provenienza, organo di nomina) tra giudici in carica negli stessi anni (test di permutazione). Si fa solo se una simulazione fatta prima dice che, per l'effetto più piccolo che interessa (scritto in `docs/decisions.md`), il test lo troverebbe almeno 8 volte su 10 (potenza di almeno 0,80, con α = 0,05). Altrimenti non si fa, e lo si dichiara.

## D3: la memoria del collegio

- **I dati.** Per ogni pronuncia che cita: tutti i precedenti citati, più un campione casuale, con un seme fisso, di precedenti che poteva citare e non ha citato. Il numero (50 o 100) si decide e si scrive in `docs/decisions.md`.
- **Il modello.** Una regressione logistica condizionata: ogni pronuncia che cita è un gruppo a sé (uno strato), e i precedenti si confrontano solo dentro lo stesso gruppo.
- **Le caratteristiche nel modello principale:**
  - `self_drafted`: chi scrive la pronuncia che cita ha scritto anche il precedente;
  - `sat_not_drafted`: chi scrive la pronuncia che cita sedeva nel collegio del precedente, senza averlo scritto;
  - l'età del precedente, divisa in classi (mai come una retta);
  - la materia.
- **Da dove viene l'informazione.** Il collegio è quasi sempre completo, quindi `sat_not_drafted` coincide quasi con "precedente uscito dopo il giuramento di chi scrive", cioè con l'età del precedente. Le differenze utili vengono da due fonti:
  - le assenze dal collegio: precedenti decisi durante il mandato di chi scrive, ma senza di lui. Sono la base del risultato principale;
  - la data del giuramento: tra giudici entrati in anni diversi, un precedente della stessa età cade dentro o fuori dal mandato.
- **Il risultato principale del progetto**, fissato prima di vedere i dati:
  - è l'odds ratio di `sat_not_drafted`, con il suo intervallo al 95%;
  - si stima solo sui precedenti decisi durante il mandato di chi scrive la pronuncia che cita (presente o assente), con `self_drafted`, le classi di età e la materia come controlli;
  - l'incertezza (gli errori standard) si calcola raggruppando le pronunce scritte dallo stesso giudice.

  Il modello completo, che usa anche la data del giuramento, è secondario. Il risultato principale non si cambia dopo aver visto i dati.
- Si riporta su quante osservazioni si regge ogni fonte di informazione (per esempio quante sono le assenze), e si descrivono le assenze per tipo di giudizio e per materia.

## Le pronunce recenti (censura)

- Le pronunce recenti hanno avuto meno tempo per essere citate.
- Per le citazioni ricevute: finestre di durata fissa dopo il deposito (la durata si decide in `docs/decisions.md`), oppure misure che tengono conto dell'età.
- Per la durata di un precedente (D1b): l'analisi della sopravvivenza, che tiene conto di chi è ancora "in osservazione".
- Per l'influenza dopo il mandato (D2): la stessa finestra dopo la fine del mandato per tutti i giudici, esclusi quelli per cui la finestra non è ancora finita.

## La materia

- Si ricava dalle massime. Per le pronunce con più massime di materie diverse, la regola (la materia prevalente o più materie insieme) si decide e si scrive in `docs/decisions.md`.
- Prima di usarla si controlla quante pronunce hanno massime, decennio per decennio, e lo si scrive in `docs/data_schema.md`. Le pronunce senza materia si dichiarano: non si riempiono di nascosto.

## Le distribuzioni

- Le code pesanti (pochi valori molto grandi) si studiano con il metodo di Clauset, Shalizi e Newman (pacchetto `powerlaw`), confrontando la legge di potenza con la lognormale. Mai stime a occhio sul grafico in scala logaritmica.

## La robustezza: le analisi principali si ripetono in sei varianti

Il testo di base è definito in `.claude/rules/data.md`. Le varianti:

- il testo intero, compreso il «Ritenuto in fatto»;
- il testo con le note editoriali alle massime;
- senza le ordinanze che correggono errori materiali;
- senza le citazioni delle pronunce scritte dallo stesso giudice;
- separando gli anni prima e dopo il 2001;
- per D2 e D3, solo le pronunce dalla 287/1986 in poi, sia quelle che citano sia quelle citate, cioè quelle con `redattore_source` diverso da `relatore_proxy`.

## Le figure

- Si producono con programmi, in `reports/figures/`, con un titolo che dice il risultato.
