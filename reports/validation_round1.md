# Controllo del programma che trova le citazioni: la prima misura

Prodotto da `src/validation/evaluate.py` con il programma come era prima della correzione per le forme antiche di citazione. Con il programma attuale non si può rifare: questo file è conservato così com'era, con il testo riscritto in parole semplici il 21/11/2026 e gli stessi numeri. Si contano le coppie "pronuncia che cita – pronuncia citata" trovate nel testo di base (il ragionamento della Corte e il dispositivo).

## In breve

Questo file è la prima misura dell'affidabilità del programma che trova le citazioni, fatta prima di correggerlo. Il programma non trovava mai citazioni sbagliate, ma nelle pronunce fino al 1986 perdeva troppe citazioni vere: lì il richiamo stava sotto la soglia decisa prima (0,90). Per questo il programma è stato corretto. Il quadro di tutti i controlli, spiegato, è in `reports/validation.md`.

**Chi ha deciso quali citazioni sono vere.** L'elenco di riferimento (`data/validation/gold_test.txt`) è stato scritto da Claude, l'assistente automatico, leggendo i passi dei testi che contengono una parola chiave (come "sentenza" o "ordinanza") o un rimando (`src/validation/sample_passages.py`). Claude li ha letti prima di far girare il programma su questo campione, senza vederne il risultato. Non l'ha scritto una persona.

**Il campione.** 4 pronunce per ogni decennio e tipo (sentenza o ordinanza), estratte a caso con il seme 20261117. È diverso dal campione usato per mettere a punto il programma (2 pronunce per gruppo, seme 20261116). Chi vuole controllare a mano trova in `data/validation/gold_test.txt`, pronuncia per pronuncia, le citazioni giudicate vere.

**Come si legge la tabella.** "Trovate giuste" sono le citazioni vere che il programma ha trovato; "trovate per errore" quelle che ha trovato ma non sono vere; "mancate" quelle vere che non ha trovato. La precisione è trovate giuste diviso tutte le trovate; il richiamo è trovate giuste diviso le citazioni vere. Tra parentesi c'è l'intervallo di confidenza al 95%, calcolato con il metodo di Wilson: i valori compatibili con i dati.

| Gruppo | Pronunce | Citazioni vere | Trovate giuste | Trovate per errore | Mancate | Precisione | Richiamo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Totale** | 64 | 270 | 254 | 0 | 16 | 1,000 (0,985–1,000) | 0,941 (0,906–0,963) |
| Sentenze | 32 | 205 | 189 | 0 | 16 | 1,000 (0,980–1,000) | 0,922 (0,877–0,951) |
| Ordinanze | 32 | 65 | 65 | 0 | 0 | 1,000 (0,944–1,000) | 1,000 (0,944–1,000) |
| Anni 1950 | 8 | 9 | 4 | 0 | 5 | 1,000 (0,510–1,000) | 0,444 (0,189–0,733) |
| Anni 1960 | 8 | 11 | 11 | 0 | 0 | 1,000 (0,741–1,000) | 1,000 (0,741–1,000) |
| Anni 1970 | 8 | 14 | 11 | 0 | 3 | 1,000 (0,741–1,000) | 0,786 (0,524–0,924) |
| Anni 1980 | 8 | 10 | 8 | 0 | 2 | 1,000 (0,676–1,000) | 0,800 (0,490–0,943) |
| Anni 1990 | 8 | 43 | 41 | 0 | 2 | 1,000 (0,914–1,000) | 0,953 (0,845–0,987) |
| Anni 2000 | 8 | 31 | 31 | 0 | 0 | 1,000 (0,890–1,000) | 1,000 (0,890–1,000) |
| Anni 2010 | 8 | 48 | 48 | 0 | 0 | 1,000 (0,926–1,000) | 1,000 (0,926–1,000) |
| Anni 2020 | 8 | 104 | 100 | 0 | 4 | 1,000 (0,963–1,000) | 0,962 (0,905–0,985) |
| Fino alla 286/1986 | 27 | 40 | 30 | 0 | 10 | 1,000 (0,886–1,000) | 0,750 (0,598–0,858) |
| Dalla 287/1986 in poi | 37 | 230 | 224 | 0 | 6 | 1,000 (0,983–1,000) | 0,974 (0,944–0,988) |

Ogni riga degli elenchi qui sotto si legge così: la pronuncia a sinistra (anno/numero) cita quella a destra.

## Citazioni trovate per errore (trovate dal programma, ma non nell'elenco di riferimento)

Nessuna.

## Citazioni mancate (nell'elenco di riferimento, ma non trovate dal programma)

- 1957/63 → 1957/59
- 1957/63 → 1957/60
- 1958/56 → 1957/3
- 1958/56 → 1957/28
- 1958/56 → 1958/53
- 1970/51 → 1970/50
- 1979/42 → 1966/63
- 1979/42 → 1972/174
- 1985/95 → 1977/16
- 1985/95 → 1982/168
- 1990/285 → 1964/66
- 1991/47 → 1972/10
- 2020/56 → 2010/278
- 2020/56 → 2016/63
- 2020/56 → 2016/110
- 2020/56 → 2016/242
