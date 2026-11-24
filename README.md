# Chi fa il precedente? Pronunce e giudici della Corte costituzionale, 1956–2026

Progetto d'esame per il corso Social Media and Web Analytics (EM1421), Università Ca' Foscari Venezia, anno accademico 2026/27. Autore: Umberto Toraldo. Il lavoro è stato svolto con un assistente di programmazione basato sull'intelligenza artificiale (Claude Code): la relazione spiega che cosa ha fatto l'assistente e che cosa l'autore (sezione 8).

> **A che punto è.** Tutte le analisi sono fatte e i risultati sono nella relazione. Mancano tre cose: l'approvazione del tema da parte del docente; il controllo a mano, da parte di una persona, delle citazioni estratte dai testi; il controllo a mano della polarità delle citazioni.

## Di che cosa parla

In Italia una sentenza della Corte costituzionale non obbliga la Corte a decidere allo stesso modo in futuro: il precedente non vincola. Eppure la Corte cita di continuo le proprie decisioni passate. Il progetto si chiede due cose:

1. **Tra le sue decisioni, la Corte crea dei "precedenti importanti"?** Alcune decisioni vengono citate moltissimo e altre quasi mai, oppure le citazioni sono sparse più o meno a caso?
2. **Contano le persone?** Ogni decisione è presa da un gruppo di 11–15 giudici (il collegio) e scritta da uno solo di loro (il redattore). Un giudice tende a citare le decisioni a cui ha partecipato, o quelle che ha scritto lui?

Per rispondere, il progetto prende tutte le 22.427 decisioni della Corte dal 1956 al 2026, ricava dal loro testo chi cita chi, e collega ogni decisione al giudice che l'ha scritta e ai giudici che l'hanno decisa. Le domande hanno un nome breve, usato in tutto il lavoro:

- **D1**: le citazioni sono concentrate su poche decisioni? Quanto dura un precedente?
- **D2**: le decisioni scritte da un certo giudice sono citate più del normale?
- **D3**: un giudice cita di più le decisioni a cui ha partecipato, o quelle che ha scritto? È il risultato principale.
- **D4**: i giudici con la stessa provenienza (professori, magistrati) o nominati dallo stesso organo si citano di più tra loro?

**Dove leggere i risultati:** [`reports/relazione_for_dummies.md`](reports/relazione_for_dummies.md). La Parte I racconta il lavoro in parole semplici; la Parte II spiega i dettagli con lo stesso linguaggio.

## I dati

Tutti i dati vengono dal [portale open data della Corte costituzionale](https://dati.cortecostituzionale.it), cioè il sito su cui la Corte pubblica i propri dati perché chiunque li possa riusare, con la licenza CC BY-SA 3.0.

- I file originali non sono nel repository, perché sono grandi: si scaricano con lo script `src/ingest/download.py`.
- [`data/raw/MANIFEST.csv`](data/raw/MANIFEST.csv) annota per ogni file scaricato l'indirizzo, la data e un'impronta del contenuto (un codice che cambia se cambia anche un solo carattere). Così si sa quale versione dei dati ha prodotto i risultati.
- [`docs/data_schema.md`](docs/data_schema.md) spiega che cosa c'è in ogni file.

## Come rifare tutto

I risultati sono stati prodotti con Python 3.12.4 e con le versioni dei pacchetti fissate in `requirements.lock`. L'installazione da zero non è ancora stata provata.

Installare l'ambiente:

```bash
python3.12 -m venv .venv
```

```bash
.venv/bin/pip install -r requirements.lock
```

Scaricare i dati dal portale della Corte (le versioni vengono annotate in `data/raw/MANIFEST.csv`):

```bash
.venv/bin/python -I src/ingest/download.py
```

Poi i passaggi, nell'ordine. Tutti i passaggi casuali partono da un seme fisso, quindi rifacendoli si ottengono gli stessi numeri. Scrivendo `REPS=100` davanti ai comandi di analisi si riducono le ripetizioni dei confronti con il caso, per una prova veloce.

```bash
.venv/bin/python src/ingest/inspect_raw.py
.venv/bin/python src/ingest/build_pronunce.py
.venv/bin/python src/extract/citations.py
.venv/bin/python src/extract/citations_massime.py
.venv/bin/python src/validation/evaluate.py test
.venv/bin/python src/validation/evaluate.py test2
.venv/bin/python src/judges/build_judges.py
.venv/bin/python src/analysis/topics.py
.venv/bin/python src/analysis/parametri.py
.venv/bin/python src/networks/build.py
.venv/bin/python src/networks/cositting.py
.venv/bin/python src/ingest/fetch_api.py
.venv/bin/python src/analysis/d1_pronunce.py
.venv/bin/python src/analysis/d2_d4_giudici.py
.venv/bin/python src/analysis/d2_strata_check.py
.venv/bin/python src/analysis/d3_memoria_collegiale.py
.venv/bin/python src/analysis/d3_absences.py
.venv/bin/python src/analysis/d3_full_check.py
.venv/bin/python src/analysis/precedent_succession.py
.venv/bin/python src/analysis/extras.py
.venv/bin/python src/analysis/course_measures.py
.venv/bin/python src/analysis/figures.py
.venv/bin/python src/analysis/interactive.py
.venv/bin/python src/report/report_numbers.py
.venv/bin/python src/report/plain_intros.py
.venv/bin/python src/courts/sizing.py
.venv/bin/python src/polarity/contexts.py
.venv/bin/python src/polarity/evaluate.py claude
```

Infine i controlli automatici. Tra l'altro verificano che i numeri della relazione coincidano con i file dei risultati:

```bash
.venv/bin/python -m pytest
```

## Com'è organizzato il repository

```
data/raw/         file originali del portale (non nel repository, salvo MANIFEST.csv)
data/interim/     tabelle intermedie e registri degli errori (non nel repository)
data/processed/   tabelle finali: le pronunce, le citazioni, i giudici, i collegi, le reti
data/validation/  campioni per controllare la qualità dell'estrazione; la lettura di riferimento è dell'assistente, non di una persona
data/manual/      correzioni fatte a mano (per ora vuota: le correzioni dichiarate sono nel codice)
src/              i programmi, divisi per fase: lettura dei file, estrazione delle citazioni, giudici, reti, analisi, altre corti, polarità
notebooks/        solo prove, nessun risultato finale
reports/          la relazione, i controlli di qualità, i risultati in formato JSON e le figure
docs/             documenti di lavoro (elencati qui sotto)
tests/            controlli automatici
```

## Documenti di lavoro

- [`docs/handbook.md`](docs/handbook.md): tutto il progetto in un unico documento: contesto, dati, ogni programma, controlli, risultati, problemi noti, lavoro che resta, come correggere, glossario, inventario dei file.
- [`docs/context.md`](docs/context.md): come nasce una decisione della Corte, chi la decide e chi la scrive, che cosa registrano i dati.
- [`docs/context_corti.md`](docs/context_corti.md): le altre quattro corti (Cassazione, Consiglio di Stato, Corte europea dei diritti dell'uomo, Corte di giustizia dell'Unione europea) e i loro dati.
- [`docs/course_mapping.md`](docs/course_mapping.md): ogni argomento del programma d'esame, se è stato usato e dove, o perché no.
- [`docs/data_schema.md`](docs/data_schema.md): che cosa c'è nei file del portale.
- [`docs/sources.md`](docs/sources.md): fonti e letteratura, con che cosa è stato letto di ciascuna.
- [`docs/decisions.md`](docs/decisions.md): il registro delle decisioni, con la data e il motivo di ogni scelta.
- [`docs/spec.md`](docs/spec.md): il piano iniziale del progetto.
- [`docs/project_guide.md`](docs/project_guide.md): una guida generale alla stesura e alla presentazione del lavoro.

## Licenza

- Dati derivati (`data/processed/`, `data/validation/`, `data/manual/`): CC BY-SA 3.0, come i dati originali.
- Codice: da decidere.

Per citare i dati originali: Corte costituzionale, dati.cortecostituzionale.it, licenza CC BY-SA 3.0.
