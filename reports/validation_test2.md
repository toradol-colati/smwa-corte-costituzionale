# Controllo del programma che trova le citazioni

Prodotto da `src/validation/evaluate.py`. Si contano le coppie "pronuncia che cita – pronuncia citata" trovate nel testo di base (il ragionamento della Corte e il dispositivo).

## In breve

Questo file misura l'affidabilità del programma che trova le citazioni su un secondo campione, mai visto prima, di pronunce fino alla 286/1986, dopo la correzione. Precisione e richiamo superano le soglie decise prima (0,95 e 0,90), ma il campione è piccolo: il limite inferiore dell'intervallo del richiamo resta sotto 0,90. Il quadro di tutti i controlli, spiegato, è in `reports/validation.md`.

**Chi ha deciso quali citazioni sono vere.** L'elenco di riferimento (`data/validation/gold_test2.txt`) è stato scritto da Claude, l'assistente automatico, leggendo i passi dei testi che contengono una parola chiave (come "sentenza" o "ordinanza") o un rimando (`src/validation/sample_passages.py`). Claude li ha letti prima di far girare il programma su questo campione, senza vederne il risultato. Non l'ha scritto una persona, e non copre i testi interi.

**Il campione.** Il campione è il secondo campione di controllo: solo pronunce fino alla 286/1986, 6 per ogni decennio e tipo, estratte a caso con il seme 20261118 dopo la correzione del programma e mai usate per metterlo a punto. È diverso dal campione usato per mettere a punto il programma (2 pronunce per gruppo, seme 20261116). Chi vuole controllare a mano trova in `data/validation/gold_test2.txt`, pronuncia per pronuncia, le citazioni giudicate vere.

**Come si legge la tabella.** "Trovate giuste" sono le citazioni vere che il programma ha trovato; "trovate per errore" quelle che ha trovato ma non sono vere; "mancate" quelle vere che non ha trovato. La precisione è trovate giuste diviso tutte le trovate; il richiamo è trovate giuste diviso le citazioni vere. Tra parentesi c'è l'intervallo di confidenza al 95%, calcolato con il metodo di Wilson: i valori compatibili con i dati.

| Gruppo | Pronunce | Citazioni vere | Trovate giuste | Trovate per errore | Mancate | Precisione | Richiamo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Totale** | 48 | 72 | 66 | 1 | 6 | 0,985 (0,920–0,997) | 0,917 (0,830–0,961) |
| Sentenze | 24 | 47 | 43 | 1 | 4 | 0,977 (0,882–0,996) | 0,915 (0,801–0,966) |
| Ordinanze | 24 | 25 | 23 | 0 | 2 | 1,000 (0,857–1,000) | 0,920 (0,750–0,978) |
| Anni 1950 | 12 | 16 | 14 | 0 | 2 | 1,000 (0,785–1,000) | 0,875 (0,640–0,965) |
| Anni 1960 | 12 | 26 | 25 | 0 | 1 | 1,000 (0,867–1,000) | 0,962 (0,811–0,993) |
| Anni 1970 | 12 | 17 | 16 | 1 | 1 | 0,941 (0,730–0,990) | 0,941 (0,730–0,990) |
| Anni 1980 | 12 | 13 | 11 | 0 | 2 | 1,000 (0,741–1,000) | 0,846 (0,578–0,957) |
| Fino alla 286/1986 | 48 | 72 | 66 | 1 | 6 | 0,985 (0,920–0,997) | 0,917 (0,830–0,961) |
| Dalla 287/1986 in poi | 0 | 0 | 0 | 0 | 0 | — | — |

Ogni riga degli elenchi qui sotto si legge così: la pronuncia a sinistra (anno/numero) cita quella a destra.

## Citazioni trovate per errore (trovate dal programma, ma non nell'elenco di riferimento)

- 1977/79 → 1975/112

## Citazioni mancate (nell'elenco di riferimento, ma non trovate dal programma)

- 1958/16 → 1957/46
- 1959/17 → 1958/70
- 1969/158 → 1967/48
- 1971/209 → 1965/119
- 1982/188 → 1971/45
- 1982/188 → 1971/183
