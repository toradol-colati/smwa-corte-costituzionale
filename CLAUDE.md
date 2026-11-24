# Rete della Corte costituzionale: istruzioni per chi lavora sul progetto

Questo file dice a chi lavora sul progetto, compreso Claude Code (l'assistente di programmazione), che cosa c'è, dove si trova e quali regole seguire. Le regole valgono sempre, anche quando non sono ripetute altrove.

## Il progetto in breve

- È il progetto d'esame per il corso Social Media and Web Analytics (EM1421, Università Ca' Foscari, anno 2026/27, docente Pierluigi Zama Ramirez). Vale il 70% del voto; si può fare da soli o in coppia, da concordare con il docente.
- Costruisce la rete delle citazioni tra le pronunce della Corte costituzionale, dal 1956 a oggi, e la collega ai giudici: chi ha scritto ogni pronuncia (il redattore) e chi sedeva nel collegio che l'ha decisa.

## Che cosa leggere prima

| Prima di… | Leggere |
| --- | --- |
| capire tutto il progetto in un posto | `docs/handbook.md`, la guida completa: ogni programma, ogni file, i problemi noti e come si corregge |
| qualsiasi scelta di metodo | `docs/spec.md`, il piano del progetto |
| interpretare un campo dei dati | `docs/context.md`: come nasce una pronuncia e che cosa vuol dire ogni campo |
| citare una fonte | `docs/sources.md`: per ogni fonte, che cosa è stato letto. Nella relazione si citano solo le fonti del nucleo indicato lì, solo le parti lette, con le pagine |
| scrivere la relazione o fare figure | `docs/project_guide.md`, la guida generale (domanda, dati, rete, metodi, risultati, limiti, grafici). Le istruzioni del corso valgono di più; le parti pensate per la ricerca medica vanno adattate, non applicate alla lettera |
| lavorare sui dati o sull'estrazione | `.claude/rules/data.md` (Claude Code la carica da solo quando si lavora su quei file) |
| lavorare sul metodo | `.claude/rules/network-analysis.md` (idem) |

- Ogni scelta che cambia i dati, il metodo o il perimetro del lavoro si scrive in `docs/decisions.md`, con la data, la decisione e il motivo.
- Le sessioni di Claude Code vanno aperte dentro questa cartella (`smwa-corte-costituzionale/`). Aperte dalla cartella superiore, non caricano `.claude/settings.json`, e quindi non vale il blocco che impedisce di modificare `data/raw/`.

## A che punto è (24/11/2026)

- Il tema non è ancora approvato dal docente. Il 16/11/2026 Umberto ha chiesto di fare comunque tutte le analisi: la regola "nessuna analisi prima dell'approvazione" non vale più (`docs/decisions.md`).
- I dati sono stati scaricati l'8/11/2026 (`data/raw/MANIFEST.csv`). Tutte le scelte aperte sono state fissate il 16/11/2026, prima di vedere i risultati.
- Fino alla pronuncia 286/1986 (cioè prima del 23/12/1986) i dati non dicono chi ha scritto la pronuncia: al suo posto si usa il relatore, e la colonna `redattore_source` dice da dove viene il nome. D2 e D3 sono rifatti anche sulle sole pronunce dal 1987, come variante.
- Le analisi sono state fatte il 16/11/2026 e corrette il 18/11/2026 dopo un controllo (sul ramo `main`, un commit per ogni correzione dopo la fotografia del 17/11, che ha l'etichetta git `versione-17-11`). I risultati sono in `reports/relazione_for_dummies.md`; le correzioni in `docs/decisions.md`; il collegamento tra il programma d'esame e le analisi in `docs/course_mapping.md`.
- 19/11/2026, su richiesta di Umberto: una materia più fine, ricavata dagli articoli della Costituzione invocati (varianti di D2 e D3, `src/analysis/parametri.py`); un controllo del contesto e dei dati di Cassazione, Consiglio di Stato, Corte europea dei diritti dell'uomo e Corte di giustizia dell'Unione europea (`docs/context_corti.md`), fatto prima di scrivere qualsiasi programma di estrazione.
- 20/11/2026, dopo una revisione esterna incollata da Umberto: descritte le assenze dal collegio (`src/analysis/d3_absences.py`); controllato il numero 0,88 del modello completo di D3, con regole fissate prima (`src/analysis/d3_full_check.py`); citati i libri di testo solo nei capitoli letti (`docs/sources.md`); divisa la relazione in due parti (Parte I, il lavoro in breve; Parte II, i dettagli), senza la cronologia nel testo. La storia delle correzioni sta in `docs/decisions.md` e nella sezione 2.9 della relazione.
- 20/11/2026, su richiesta di Umberto: impostata la rete tra corti. Le menzioni delle altre corti si estraggono con `src/courts/mentions.py`. Le regole sono alla versione 2, scritte guardando solo la metà dei dati per lo sviluppo, e non sono ancora congelate: fino ad allora il programma si rifiuta di leggere la metà di prova. Le domande, che cosa si può verificare per ogni corte e il controllo di qualità sono fissati in `docs/decisions.md`.
- 20/11/2026, su richiesta di Umberto: controllato se un precedente dimenticato viene "sostituito" dalle pronunce che lo citano (`src/analysis/precedent_succession.py`).
- 21/11/2026, su richiesta di Umberto: tutti i documenti, e i report scritti dai programmi, sono stati riscritti in italiano semplice. I numeri non cambiano.
- 22/11/2026: il programma dei giudici scrive le pronunce con il collegio non riconosciuto per intero in `data/interim/collegio_errors.csv` (257).
- 24/11/2026, su richiesta di Umberto: la rete dei collegi tra giudici (`src/networks/cositting.py`), solo descrittiva; la guida completa `docs/handbook.md`, che nella sezione 11 elenca i problemi noti e i punti non verificati (tra questi: `reports/collegio_vs_sedute.json` non ha un programma che lo scrive).
- Restano da fare:
  - l'approvazione del docente;
  - il controllo a mano, da parte di una persona, delle citazioni estratte (`data/validation/human_check.md`): è la priorità, prima di qualsiasi estensione;
  - il controllo a mano della polarità delle citazioni (`data/validation/polarity_human_check.md`), che non ha superato la soglia;
  - il confronto della mappa del programma d'esame con l'elenco delle lezioni;
  - due scelte che spettano a Umberto dopo aver visto il materiale: la seconda versione della polarità e l'unità della rete tra corti (`docs/decisions.md`, "Ancora da decidere").
- Più avanti, dopo aver finito tutto in Python: l'analisi andava fatta in R, quindi andrà rifatta in R. Per ora non si cambia nulla.
- L'ambiente: i risultati del 16–18/11/2026 vengono da un ambiente virtuale (`.venv`) creato con `--system-site-packages` sopra Anaconda (Python 3.12.4); le versioni usate sono fissate in `requirements.lock`. I comandi si lanciano con `.venv/bin/python`.
- La cartella è sincronizzata con iCloud, con l'ottimizzazione dello spazio: molti file di `data/` restano sul cloud finché non servono, e la lettura può bloccarsi. `brctl download <file>` li riporta sul computer.

## Le domande di ricerca

La formulazione unica, da usare identica nel riassunto e nella presentazione: "In un ordinamento in cui il precedente non vincola, la Corte costituzionale costruisce comunque una gerarchia di precedenti? E quanto di quell'autorità passa attraverso i giudici che redigono e decidono le pronunce?" Nella relazione la stessa domanda è spiegata in parole semplici (Parte I, "La domanda"), senza cambiarne il senso.

Il risultato principale, l'unico da cui si traggono conclusioni formali, è l'odds ratio di `sat_not_drafted` in D3, stimato sulle assenze dal collegio (`docs/spec.md`, "Come si controlla ogni risultato", punto 5). Gli altri risultati sono secondari.

- **D1, le pronunce.** Le citazioni sono concentrate su poche pronunce? Le pronunce più autorevoli secondo il metodo HITS (le "authority") sono anche le più citate? Quanto dura un precedente?
- **D2, i giudici.** Le pronunce scritte da un giudice sono citate più di quanto ci si aspetta date le sue occasioni? L'effetto dura oltre il mandato?
- **D3, l'incrocio.** A parità di età e di materia, chi scrive una pronuncia cita di più i precedenti decisi da collegi di cui faceva parte? È il contributo nuovo del progetto.
- **D4, un'estensione.** Ci si cita di più tra giudici con la stessa provenienza o nominati dallo stesso organo? Si fa solo se i dati bastano a vedere un effetto (potenza statistica).

## I dati

La fonte è il portale dati.cortecostituzionale.it, con la licenza CC BY-SA 3.0.

- `data/raw/pronunce/`: 22.427 pronunce in XML, un file per anno (1956–2026), estratti da tre archivi compressi.
- `data/raw/massime/`: le massime in XML, un file per anno fino a oggi; contengono anche il tipo di giudizio. Le versioni CSV e JSON si fermano al 2015: si usa l'XML.
- `data/raw/giudici/`: l'elenco ufficiale dei giudici in XML (136 righe, 125 giudici). Le date di fine mandato sono incomplete.
- `data/raw/MANIFEST.csv`: una riga per ogni file scaricato, con l'indirizzo, la data e l'impronta SHA-256 (un codice che cambia se cambia il file). Lo scrive il programma di download; è l'unico file di `data/raw/` salvato in git.
- `data/processed/judges_attributes.csv`: l'organo che ha nominato ogni giudice (dal campo `eletto_da`) e la sua provenienza professionale, ricavata in automatico dalla nota biografica dell'elenco (`src/analysis/d2_d4_giudici.py`). Non è una classificazione fatta a mano.
- Le correzioni dichiarate (due cognomi scritti male, la fine del mandato di Spagnoli, le date di fine mandato mancanti, calcolate come giuramento più 9 anni) sono nel codice di `src/judges/build_judges.py`, con il rimando a `docs/decisions.md`. Per ora `data/manual/` è vuota.
- La banca dati SPARQL della Corte serve solo per controlli puntuali.
- I dati derivati si pubblicano solo con la licenza CC BY-SA 3.0, citando la Corte.

## Com'è organizzata la cartella

```
data/raw/         file originali del portale: mai modificati, non in git (salvo MANIFEST.csv)
data/interim/     tabelle intermedie e registri degli errori, non in git
data/processed/   tabelle finali: pronunce, citazioni, giudici, collegi, reti
data/validation/  campioni per controllare l'estrazione; la lettura di riferimento è di Claude, non di una persona
data/manual/      correzioni fatte a mano, ognuna con la sua fonte (per ora vuota)
src/ingest/       lettura dei file del portale e controlli con altre fonti
src/extract/      estrazione delle citazioni dal testo
src/validation/   misura della qualità dell'estrazione
src/judges/       nomi dei giudici, redattori, collegi
src/networks/     costruzione delle reti
src/analysis/     misure, confronti con il caso, modelli
src/polarity/     regole sulla polarità delle citazioni (non usate: sotto la soglia)
src/courts/       menzioni delle altre corti (impostato, non concluso)
src/report/       numeri usati nella relazione e introduzioni dei report
notebooks/        solo prove: i risultati finali vengono da src/
tests/            controlli automatici
reports/          relazione, controlli di qualità, risultati in JSON, figure (reports/figures/)
docs/             documenti di lavoro
```

## L'ambiente e i comandi

- Installazione: `python3.12 -m venv .venv && .venv/bin/pip install -r requirements.lock` (versioni esatte; l'installazione da zero non è ancora stata provata). `requirements.txt` elenca solo i pacchetti usati dal codice.
- Quando si aggiunge un pacchetto, lo si scrive in `requirements.txt`, e la sua versione, con quelle dei pacchetti da cui dipende, in `requirements.lock`.
- Controlli automatici: `.venv/bin/python -m pytest`.
- Scaricare i dati: `python3 -I src/ingest/download.py` (tutto) oppure con un gruppo (`pronunce`, `massime`, `giudici`). Ogni download aggiunge righe al manifest.
- Primo controllo dei dati: `.venv/bin/python src/ingest/inspect_raw.py`, che scrive `reports/data_inspection.md`.
- La sequenza completa, nell'ordine, sempre con `.venv/bin/python`:
  `src/ingest/download.py` → `src/ingest/inspect_raw.py` → `src/ingest/build_pronunce.py` → `src/extract/citations.py` → `src/extract/citations_massime.py` → `src/validation/evaluate.py test` e `test2` → `src/judges/build_judges.py` → `src/analysis/topics.py` → `src/analysis/parametri.py` → `src/networks/build.py` → `src/networks/cositting.py` → `src/ingest/fetch_api.py` → `src/analysis/d1_pronunce.py` → `src/analysis/d2_d4_giudici.py` → `src/analysis/d2_strata_check.py` → `src/analysis/d3_memoria_collegiale.py` → `src/analysis/d3_absences.py` → `src/analysis/d3_full_check.py` → `src/analysis/precedent_succession.py` → `src/analysis/extras.py` → `src/analysis/course_measures.py` → `src/analysis/figures.py` → `src/analysis/interactive.py` → `src/report/report_numbers.py` → `src/report/plain_intros.py` → `pytest` (che controlla anche i numeri della relazione).
- La polarità delle citazioni: `src/polarity/contexts.py` → `draw_sample.py` (il campione è già estratto: non rifarlo) → `evaluate.py claude` oppure `human`.
- Scrivere `REPS=100` davanti ai comandi di analisi riduce le ripetizioni dei confronti con il caso, per una prova veloce.
- Alcuni report si possono riscrivere senza rifare i calcoli: `src/analysis/d3_memoria_collegiale.py --md-only` riscrive `reports/d3_results.md` dai numeri salvati; `src/analysis/topics.py --labels-only` ricalcola solo i nomi dei temi.
- I report scritti dai programmi sono in italiano semplice; `src/report/plain_intros.py` aggiunge, o aggiorna, il riassunto "In breve" in testa a ognuno. `reports/validation.md` e la relazione sono scritti a mano.
- La relazione è scritta a mano in italiano semplice; `pytest` controlla che i suoi numeri coincidano con i file dei risultati, separatamente nella Parte I e nella Parte II. Dopo aver rifatto un'analisi si aggiorna il testo finché il controllo passa.
- Dove sono i risultati: `reports/relazione_for_dummies.md` (la relazione, in due parti), `reports/validation.md` (la qualità dei dati), `reports/*.json` (i numeri), `reports/figures/` (le figure).
- Codice, nomi dei file e commenti in inglese. Documenti in italiano semplice: frasi brevi, parole tecniche solo se spiegate o tra parentesi, i dubbi di base anticipati.

## Regole sempre valide

1. Prima di scrivere un programma che legge i file (un parser), si guardano i file e si scrive in `docs/data_schema.md` quali campi ci sono e quanto sono completi anno per anno, e in `docs/context.md` a quale concetto giuridico corrisponde ogni campo. Non si inventano nomi di campi.
2. Ogni concetto giuridico usato nel codice o nella relazione (redattore, relatore, collegio, date, tipo di giudizio, esito, materia) ha una definizione, con la fonte, in `docs/context.md`. Se la definizione manca, o se i dati non tornano con la definizione, ci si ferma e lo si segnala: non si sceglie un'interpretazione da soli.
3. La pronuncia è della Corte: la decide il collegio, il redattore la scrive. Nei risultati si scrive "pronunce redatte da X", mai "decisioni di X".
4. Una pronuncia si identifica con anno e numero, lo stesso schema del codice europeo ECLI. Prima di usarlo si verifica sui dati che la numerazione riparta ogni anno e sia comune a sentenze e ordinanze.
5. Il testo in cui si cercano le citazioni (il testo di base) è il «Considerato in diritto» con il dispositivo nelle sentenze, il «Considerato che» con il dispositivo nelle ordinanze. Il «Ritenuto in fatto» e le note editoriali entrano solo nelle varianti, per vedere se i risultati reggono.
6. I dati del portale si scaricano solo con il programma in `src/ingest/`, che aggiorna `data/raw/MANIFEST.csv`.
7. Ogni numero della relazione viene da un programma in `src/`, mai scritto a mano. Tutto ciò che è casuale parte da un seme fisso.
8. Se una soglia di qualità non è raggiunta, ci si ferma e lo si segnala: non si passa alle analisi.
9. Nessun risultato senza il confronto con il caso (il modello nullo) previsto in `.claude/rules/network-analysis.md`. Ogni risultato è una stima, con il suo intervallo al 95% e con il valore che ci si aspetterebbe per caso. "Forte", "alto" o "concentrato" si scrivono solo se c'è un test dietro.
10. Nessun dato da fonti diverse da quelle elencate, senza dirlo chiaramente.
11. I file in `data/raw/` non si modificano a mano: `.claude/settings.json` blocca le modifiche dirette.
12. Il repository diventerà pubblico: prima di pubblicarlo si segue la lista "Prima di rendere pubblico il repository" in `docs/decisions.md`.

## Le soglie di qualità, fissate prima di vedere i risultati

- **Estrazione delle citazioni:** precisione di almeno 0,95 e richiamo di almeno 0,90, misurati sulle coppie di pronunce (pronuncia che cita, pronuncia citata). La precisione è la quota delle citazioni trovate che sono vere; il richiamo è la quota delle citazioni vere che vengono trovate. Il campione è diviso per decennio e tipo di pronuncia, ha almeno 460 coppie, e le sue pronunce si leggono per intero.
- **Chi ha scritto la pronuncia:** il nome è collegato all'elenco dei giudici in almeno il 98% delle pronunce.
- **Collegio:** almeno il 98% delle pronunce ha il collegio riconosciuto per intero, cioè tra 11 (il numero legale) e 15 giudici, tutti collegati all'elenco.

## I controlli con fonti esterne

Sono quote di accordo, da rifare a ogni nuovo download.

- **Relatore, file contro banca dati SPARQL** (`reports/sparql_reconciliation.md`, 12/11/2026): accordo nel 97,12% di 22.426 pronunce. Delle 645 differenze, 635 sono due errori di grafia nel campo dei file ("Caianello" per Caianiello, 471; "Capolozza" per Capalozza, 164), corretti nel codice (`src/judges/build_judges.py`); le altre 10 sono pronunce con il relatore vuoto nei file e due relatori nella banca dati.
- **Collegio ricavato dal testo contro i giudici presenti alle sedute** nella banca dati (dal 2004): il 97,8% dei giudici del collegio risulta presente alla seduta, e il 99,1% dei presenti alla seduta risulta nel collegio, su 3.684 pronunce (`reports/collegio_vs_sedute.json`).
