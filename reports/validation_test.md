# Controllo del programma che trova le citazioni

Prodotto da `src/validation/evaluate.py`. Si contano le coppie "pronuncia che cita – pronuncia citata" trovate nel testo di base (il ragionamento della Corte e il dispositivo).

## In breve

Questo file rifà il calcolo sul primo campione dopo la correzione del programma. Non è una misura indipendente, perché la correzione è stata scritta guardando gli errori di questo stesso campione: serve solo a controllare che la correzione non abbia rotto altro, cioè che non abbia aggiunto citazioni sbagliate. Il quadro di tutti i controlli, spiegato, è in `reports/validation.md`.

**Chi ha deciso quali citazioni sono vere.** L'elenco di riferimento (`data/validation/gold_test.txt`) è stato scritto da Claude, l'assistente automatico, leggendo i passi dei testi che contengono una parola chiave (come "sentenza" o "ordinanza") o un rimando (`src/validation/sample_passages.py`). Claude li ha letti prima di far girare il programma su questo campione, senza vederne il risultato. Non l'ha scritto una persona, e non copre i testi interi.

**Il campione.** Il campione è il primo campione di controllo: 4 pronunce per ogni decennio e tipo (sentenza o ordinanza), estratte a caso con il seme 20261117. Dopo la prima misura (conservata in `validation_round1.md`) il programma è stato corretto guardando gli errori di questo campione: i numeri qui sotto non sono più una stima indipendente. È diverso dal campione usato per mettere a punto il programma (2 pronunce per gruppo, seme 20261116). Chi vuole controllare a mano trova in `data/validation/gold_test.txt`, pronuncia per pronuncia, le citazioni giudicate vere.

**Come si legge la tabella.** "Trovate giuste" sono le citazioni vere che il programma ha trovato; "trovate per errore" quelle che ha trovato ma non sono vere; "mancate" quelle vere che non ha trovato. La precisione è trovate giuste diviso tutte le trovate; il richiamo è trovate giuste diviso le citazioni vere. Tra parentesi c'è l'intervallo di confidenza al 95%, calcolato con il metodo di Wilson: i valori compatibili con i dati.

| Gruppo | Pronunce | Citazioni vere | Trovate giuste | Trovate per errore | Mancate | Precisione | Richiamo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Totale** | 64 | 270 | 264 | 0 | 6 | 1,000 (0,986–1,000) | 0,978 (0,952–0,990) |
| Sentenze | 32 | 205 | 199 | 0 | 6 | 1,000 (0,981–1,000) | 0,971 (0,938–0,987) |
| Ordinanze | 32 | 65 | 65 | 0 | 0 | 1,000 (0,944–1,000) | 1,000 (0,944–1,000) |
| Anni 1950 | 8 | 9 | 8 | 0 | 1 | 1,000 (0,676–1,000) | 0,889 (0,565–0,980) |
| Anni 1960 | 8 | 11 | 11 | 0 | 0 | 1,000 (0,741–1,000) | 1,000 (0,741–1,000) |
| Anni 1970 | 8 | 14 | 14 | 0 | 0 | 1,000 (0,785–1,000) | 1,000 (0,785–1,000) |
| Anni 1980 | 8 | 10 | 10 | 0 | 0 | 1,000 (0,722–1,000) | 1,000 (0,722–1,000) |
| Anni 1990 | 8 | 43 | 42 | 0 | 1 | 1,000 (0,916–1,000) | 0,977 (0,879–0,996) |
| Anni 2000 | 8 | 31 | 31 | 0 | 0 | 1,000 (0,890–1,000) | 1,000 (0,890–1,000) |
| Anni 2010 | 8 | 48 | 48 | 0 | 0 | 1,000 (0,926–1,000) | 1,000 (0,926–1,000) |
| Anni 2020 | 8 | 104 | 100 | 0 | 4 | 1,000 (0,963–1,000) | 0,962 (0,905–0,985) |
| Fino alla 286/1986 | 27 | 40 | 39 | 0 | 1 | 1,000 (0,910–1,000) | 0,975 (0,871–0,996) |
| Dalla 287/1986 in poi | 37 | 230 | 225 | 0 | 5 | 1,000 (0,983–1,000) | 0,978 (0,950–0,991) |

Ogni riga degli elenchi qui sotto si legge così: la pronuncia a sinistra (anno/numero) cita quella a destra.

## Citazioni trovate per errore (trovate dal programma, ma non nell'elenco di riferimento)

Nessuna.

## Citazioni mancate (nell'elenco di riferimento, ma non trovate dal programma)

- 1957/63 → 1957/60
- 1991/47 → 1972/10
- 2020/56 → 2010/278
- 2020/56 → 2016/63
- 2020/56 → 2016/110
- 2020/56 → 2016/242
