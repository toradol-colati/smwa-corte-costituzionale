# Chi fa il precedente? Pronunce e giudici della Corte costituzionale, 1956–2026

Progetto per il corso Social Media and Web Analytics (EM1421), Università Ca' Foscari Venezia, a.a. 2026/27. Autore: Umberto Toraldo.

> **Stato:** in preparazione. Il tema è in attesa dell'approvazione del docente. Non ci sono ancora né dati né risultati.

## Cosa fa

Costruisce la rete delle pronunce della Corte costituzionale dal 1956 a oggi, collegate dalle citazioni. La incrocia con i giudici che le hanno redatte e con quelli che sedevano nel collegio. Serve a misurare dove sta l'autorità del precedente in un ordinamento in cui il precedente non è vincolante.

La domanda: in un ordinamento in cui il precedente non vincola, la Corte costituzionale costruisce comunque una gerarchia di precedenti? E quanto di quell'autorità passa attraverso i giudici che redigono e decidono le pronunce?

Le sotto-domande:

- **D1 · Pronunce:** l'autorità è concentrata in poche pronunce? Quanto dura un precedente?
- **D2 · Giudici:** l'influenza di un giudice supera quella attesa date le sue opportunità?
- **D3 · Memoria collegiale:** un redattore cita di più i precedenti decisi da collegi di cui faceva parte?
- **D4 · Estensione:** ci si cita di più tra giudici con la stessa provenienza o lo stesso organo di nomina?

La specifica completa è in [`docs/spec.md`](docs/spec.md).

## Dati

Fonte: [portale open data della Corte costituzionale](https://dati.cortecostituzionale.it), licenza CC BY-SA 3.0.

- I file originali non sono nel repository: si scaricano con lo script di download (da aggiungere).
- [`data/raw/MANIFEST.csv`](data/raw/MANIFEST.csv) registra URL, data e SHA-256 di ogni file scaricato, cioè la versione dei dati usata per i risultati.
- Lo schema dei file è documentato in [`docs/data_schema.md`](docs/data_schema.md).

## Come rieseguire

I risultati sono stati prodotti con Python 3.12.4 e le versioni dei pacchetti fissate in `requirements.lock` (installazione da zero non ancora provata).

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.lock
```

Scaricare i dati dal portale della Corte (registra le versioni in `data/raw/MANIFEST.csv`):

```bash
python3 -I src/ingest/download.py
```

Ispezionare i file scaricati (scrive `reports/data_inspection.md`):

```bash
python3 src/ingest/inspect_raw.py
```

Il resto della pipeline, nell'ordine (`REPS=100` davanti ai comandi di analisi riduce le ripetizioni dei modelli nulli):

```bash
.venv/bin/python src/ingest/build_pronunce.py
.venv/bin/python src/extract/citations.py
.venv/bin/python src/extract/citations_massime.py
.venv/bin/python src/validation/evaluate.py test
.venv/bin/python src/validation/evaluate.py test2
.venv/bin/python src/judges/build_judges.py
.venv/bin/python src/analysis/topics.py
.venv/bin/python src/networks/build.py
.venv/bin/python src/ingest/fetch_api.py
.venv/bin/python src/analysis/d1_pronunce.py
.venv/bin/python src/analysis/d2_d4_giudici.py
.venv/bin/python src/analysis/d3_memoria_collegiale.py
.venv/bin/python src/analysis/extras.py
.venv/bin/python src/analysis/course_measures.py
.venv/bin/python src/analysis/figures.py
.venv/bin/python src/analysis/interactive.py
.venv/bin/python src/report/report_numbers.py
.venv/bin/python src/polarity/contexts.py
.venv/bin/python src/polarity/evaluate.py claude
```

Risultati: [`reports/relazione_for_dummies.md`](reports/relazione_for_dummies.md); qualità dei dati: [`reports/validation.md`](reports/validation.md).

Test:

```bash
pytest
```

## Struttura

```
data/raw/         file originali del portale (non versionati, salvo MANIFEST.csv)
data/interim/     tabelle intermedie e log degli errori (non versionati)
data/processed/   tabelle finali di nodi e archi
data/validation/  campioni di riferimento annotati da Claude (non da una persona)
data/manual/      codifiche manuali, ognuna con la sua fonte
src/              pipeline: ingest, extract, judges, networks, analysis
notebooks/        solo esplorazione
reports/          relazione, validazione e figure
docs/             specifica, schema dei dati, registro delle decisioni
```

## Documentazione

- [`docs/context.md`](docs/context.md): come nasce una pronuncia, chi la decide e chi la scrive, cosa registrano i dati.
- [`docs/spec.md`](docs/spec.md): domande, dati, metodo, limiti.
- [`docs/sources.md`](docs/sources.md): fonti e letteratura.
- [`docs/project_guide.md`](docs/project_guide.md): guida generale alla stesura e alla presentazione del lavoro.
- [`docs/decisions.md`](docs/decisions.md): registro delle decisioni.
- [`docs/course_mapping.md`](docs/course_mapping.md): ogni argomento del programma d'esame, applicato (dove) o no (perché).
- [`docs/data_schema.md`](docs/data_schema.md): campi e copertura dei file del portale.

## Licenza

- Dati derivati (`data/processed/`, `data/validation/`, `data/manual/`): CC BY-SA 3.0, come i dati originali.
- Codice: da definire.

Per citare i dati originali: Corte costituzionale, dati.cortecostituzionale.it, licenza CC BY-SA 3.0.
