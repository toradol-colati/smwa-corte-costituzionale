# Rete della Corte costituzionale — istruzioni di progetto

Progetto d'esame per Social Media and Web Analytics (EM1421, Ca' Foscari, a.a. 2026/27, docente Pierluigi Zama Ramirez). Vale il 70% del voto; individuale o in coppia, da concordare.
Costruisce la rete delle pronunce della Corte costituzionale (1956–oggi) e la incrocia con i giudici: chi le ha redatte e chi sedeva nel collegio.

Specifica completa: `docs/spec.md`. Leggila prima di qualsiasi scelta metodologica.
Fonti e letteratura, con lo stato di lettura di ogni voce: `docs/sources.md`. Nella relazione si cita solo il nucleo minimo indicato lì, e solo ciò che è stato letto, con le pagine.
Contesto istituzionale e significato dei campi: `docs/context.md`. Leggilo prima di interpretare qualsiasi campo dei dati.
Guida generale per impostare, scrivere e presentare il lavoro (domanda, dati, rete, metodi, risultati, limiti, grafici): `docs/project_guide.md`. Leggila prima di scrivere la relazione o produrre figure. Le istruzioni del corso prevalgono; le parti pensate per la ricerca clinica vanno tradotte al caso, non applicate alla lettera.
Decisioni prese durante il lavoro: `docs/decisions.md` (data, decisione, motivo). Aggiornalo a ogni scelta che cambia dati, metodo o perimetro.
Regole di dettaglio, caricate quando lavori sui file corrispondenti: `.claude/rules/data.md` (dati ed estrazione), `.claude/rules/network-analysis.md` (metodo).
Apri le sessioni di Claude Code dentro questa cartella (`smwa-corte-costituzionale/`). Dalla cartella superiore `.claude/settings.json` non si carica, e il blocco delle modifiche a `data/raw/` non vale.

## Stato (2026-11-16)
- Il tema non è ancora approvato dal docente. Il 16/11/2026 Umberto ha chiesto di eseguire comunque tutte le analisi: la regola "nessuna analisi prima dell'approvazione" è superata (`docs/decisions.md`).
- Dati scaricati l'8/11/2026 (`data/raw/MANIFEST.csv`). Tutte le scelte aperte sono state fissate il 16/11/2026 prima dei risultati.
- Redattore prima del 23/12/1986 (pronunce fino alla 286/1986): si usa il relatore come approssimazione, con colonna `redattore_source`; D2 e D3 si rifanno sulle sole pronunce dal 1987 come variante.
- Analisi eseguite il 16/11/2026 e corrette il 18/11/2026 dopo un check (su `main`, un commit per correzione dopo la fotografia del 17/11, etichetta git `versione-17-11`): risultati in `reports/relazione_for_dummies.md`; scostamenti e correzioni in `docs/decisions.md`; mappa programma → analisi in `docs/course_mapping.md`. Restano aperti: approvazione del docente, controllo umano dell'estrazione (`data/validation/human_check.md`), confronto della mappa con l'elenco delle lezioni, controllo umano della polarità delle citazioni (`data/validation/polarity_human_check.md`), che non ha superato la soglia.
- Ambiente: i risultati del 16–18/11/2026 vengono da un `.venv` creato con `--system-site-packages` sopra Anaconda (Python 3.12.4); le versioni usate sono fissate in `requirements.lock`. I comandi della pipeline si lanciano con `.venv/bin/python`.

## Domande di ricerca
Formulazione unica, da usare identica in relazione, abstract e presentazione: "In un ordinamento in cui il precedente non vincola, la Corte costituzionale costruisce comunque una gerarchia di precedenti? E quanto di quell'autorità passa attraverso i giudici che redigono e decidono le pronunce?"
Risultato principale, l'unico da cui si traggono conclusioni formali: l'odds ratio di `sat_not_drafted` in D3, stimato sulle assenze dal collegio (`docs/spec.md`, Modelli nulli, punto 5). Gli altri risultati sono secondari.
- D1 · Pronunce: l'autorità è concentrata in poche pronunce? Le authority (HITS) coincidono con le più citate? Quanto dura un precedente?
- D2 · Giudici: l'influenza di un giudice supera quella attesa date le sue opportunità? Dura oltre il mandato?
- D3 · Intersezione: a parità di età e materia, un redattore cita di più i precedenti decisi da collegi di cui faceva parte? È il contributo nuovo del progetto.
- D4 · Estensione, solo se la potenza statistica basta: ci si cita di più tra giudici con la stessa provenienza o lo stesso organo di nomina?

## Dati (fonte: dati.cortecostituzionale.it, licenza CC BY-SA 3.0)
- `data/raw/pronunce/`: 22.427 pronunce in XML, un file per anno (1956–2026), estratti da tre archivi.
- `data/raw/massime/`: massime in XML, un file per anno fino a oggi; contengono anche il tipo di giudizio. I CSV e JSON si fermano al 2015: usare l'XML.
- `data/raw/giudici/`: anagrafica dei giudici in XML (125 giudici). Date di cessazione incomplete: si completano in `data/manual/`.
- `data/raw/MANIFEST.csv`: una riga per file scaricato, con URL, data e SHA-256. Lo scrive lo script di download; è l'unico file di `data/raw/` versionato.
- `data/processed/judges_attributes.csv`: organo di nomina (dal campo `eletto_da`) e provenienza professionale, codificata in automatico dalla nota biografica dell'anagrafica (`src/analysis/d2_d4_giudici.py`). Non è una codifica manuale.
- Endpoint SPARQL del portale: solo per verifiche puntuali.
- I dati derivati si pubblicano solo con licenza CC BY-SA 3.0, citando la Corte.

## Struttura
```
data/raw/         file originali del portale: mai modificati, non versionati
data/interim/     tabelle intermedie e log degli errori, non versionati
data/processed/   tabelle finali di nodi e archi
data/validation/  campioni di riferimento, annotati da Claude leggendo i testi (non da una persona)
data/manual/      codifiche manuali, ognuna con la sua fonte
src/ingest/       lettura dei file del portale
src/extract/      estrazione delle citazioni dal testo
src/judges/       normalizzazione dei nomi, redattori, collegi
src/networks/     costruzione dei tre strati e delle reti derivate
src/analysis/     metriche, modelli nulli, test
notebooks/        solo esplorazione: i risultati finali vengono da src/
reports/figures/  figure generate da script
tests/
reports/          report generati da script (data_inspection.md, validation.md)
docs/             spec.md, context.md, decisions.md, data_schema.md
```

## Ambiente e comandi
- Installazione riproducibile: `python3.12 -m venv .venv && .venv/bin/pip install -r requirements.lock` (versioni esatte; non ancora provata da zero). `requirements.txt` elenca solo i pacchetti usati dal codice.
- Quando si aggiunge un pacchetto: aggiungerlo a `requirements.txt` e la sua versione, con le dipendenze, a `requirements.lock`.
- Test: `pytest`
- Scaricare i dati: `python3 -I src/ingest/download.py` (tutti) oppure con un gruppo (`pronunce`, `massime`, `giudici`). Aggiunge righe al manifest.
- Ispezionare i dati: `python3 src/ingest/inspect_raw.py`, che scrive `reports/data_inspection.md`.
- Pipeline completa, nell'ordine (ambiente da `requirements.lock`):
  `src/ingest/download.py` → `src/ingest/inspect_raw.py` → `src/ingest/build_pronunce.py` → `src/extract/citations.py` → `src/extract/citations_massime.py` → `src/validation/evaluate.py test` e `test2` → `src/judges/build_judges.py` → `src/analysis/topics.py` → `src/analysis/parametri.py` → `src/networks/build.py` → `src/ingest/fetch_api.py` → `src/analysis/d1_pronunce.py` → `src/analysis/d2_d4_giudici.py` → `src/analysis/d3_memoria_collegiale.py` → `src/analysis/extras.py` → `src/analysis/course_measures.py` → `src/analysis/figures.py` → `src/analysis/interactive.py` → `src/report/report_numbers.py` → `pytest` (anche il test dei numeri della relazione). Polarità delle citazioni: `src/polarity/contexts.py` → `draw_sample.py` (campione già estratto, non rifarlo) → `evaluate.py claude|human`. Tutti con `.venv/bin/python`; `REPS=100` riduce le ripetizioni dei nulli per una prova veloce.
- Risultati: `reports/relazione_for_dummies.md` (relazione completa), `reports/validation.md` (qualità), `reports/*.json` (numeri), `reports/figures/`.
- Codice, nomi di file e commenti in inglese; documenti di lavoro in italiano.

## Regole sempre valide
- Prima di scrivere un parser, ispeziona i file e documenta campi e copertura per anno in `docs/data_schema.md`, e il concetto giuridico a cui corrisponde ogni campo in `docs/context.md`. Non inventare nomi di campi.
- Ogni concetto giuridico usato nel codice o nella relazione (redattore, relatore, collegio, date, tipo di giudizio, esito, materia) ha una definizione con fonte in `docs/context.md`. Se manca, o se i dati non tornano con la definizione, fermati e segnalalo: non scegliere un'interpretazione da solo.
- La pronuncia è della Corte: la decide il collegio, il redattore la scrive. Nei risultati si scrive "pronunce redatte da X", mai "decisioni di X".
- ID canonico di una pronuncia: anno + numero, lo stesso schema dell'ECLI. Prima di usarlo, verifica sui dati che la numerazione sia annuale e comune a sentenze e ordinanze.
- Testo di base delle citazioni: «Considerato in diritto» e dispositivo nelle sentenze, «Considerato che» e dispositivo nelle ordinanze. Il «Ritenuto in fatto» e le note editoriali entrano solo come varianti di robustezza.
- I dati del portale si scaricano solo con lo script in `src/ingest/`, che aggiorna `data/raw/MANIFEST.csv`.
- Ogni numero della relazione viene da uno script in `src/`, mai scritto a mano. Seed fissi per tutto ciò che è casuale.
- Se una soglia di qualità non è raggiunta, fermati e segnalalo: non passare alle analisi.
- Nessun risultato senza il confronto con il modello nullo previsto in `.claude/rules/network-analysis.md`. Ogni risultato è una stima con il suo intervallo al 95% più il valore atteso sotto il nullo; "forte", "alto" o "concentrato" solo con un test dietro.
- Nessun dato da fonti diverse da quelle elencate senza dirlo esplicitamente.
- I file in `data/raw/` non si modificano a mano: `.claude/settings.json` blocca le modifiche dirette.
- Il repository diventerà pubblico: prima di pubblicarlo, segui la lista "Prima della pubblicazione" in `docs/decisions.md`.

## Soglie di qualità (fissate prima di vedere i risultati)
- Estrazione delle citazioni: precisione ≥ 0,95 e richiamo ≥ 0,90, misurate sulle coppie di pronunce (citante, citata). Campione stratificato per decennio e tipo di pronuncia, di almeno 460 coppie, con le pronunce annotate per intero.
- Abbinamento del redattore all'anagrafica: ≥ 98% delle pronunce.
- Collegio: ≥ 98% delle pronunce con il collegio riconosciuto per intero, tra 11 (il numero legale) e 15 giudici, tutti abbinati all'anagrafica.

## Verifiche di qualità con fonti esterne (tassi di concordanza, da riportare a ogni nuovo download)
- Relatore, file contro endpoint SPARQL (`reports/sparql_reconciliation.md`, 12/11/2026): concordanza 97,12% su 22.426 pronunce. Delle 645 discordanze, 635 sono due errori di grafia nel campo dei file ("Caianello" per Caianiello, 471; "Capolozza" per Capalozza, 164), da correggere in `data/manual/judge_name_map.csv`; le altre 10 sono pronunce con il relatore vuoto nei file e due relatori nell'endpoint.
- Collegio, estratto dal testo contro membri delle sedute dell'endpoint (dal 2004): il 97,8% dei giudici del collegio risulta nella seduta e il 99,1% dei membri della seduta nel collegio, su 3.684 pronunce (`reports/collegio_vs_sedute.json`).
