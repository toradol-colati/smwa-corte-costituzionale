# Validazione dell'estrazione delle citazioni

Generato da `src/validation/evaluate.py`. Unità: la coppia (pronuncia che cita, pronuncia citata) nel testo di base.

## In breve

Questo file ricalcola il primo campione dopo la correzione del programma. Non è una misura indipendente, perché la correzione è stata scritta guardando gli errori di questo stesso campione: serve solo a controllare che non abbia rotto altro. La **precisione** è la quota di citazioni trovate dal programma che sono vere; il **richiamo** è la quota di citazioni vere che il programma trova. Le soglie decise prima erano 0,95 e 0,90. Tra parentesi c'è l'intervallo di confidenza al 95%, cioè i valori compatibili con i dati. Chi ha deciso quali citazioni sono vere è l'assistente automatico (Claude), non una persona. Il quadro di tutti i controlli, spiegato, è in `reports/validation.md`.

**Chi ha annotato.** L'annotazione di riferimento (`data/validation/gold_test.txt`) è stata fatta da Claude leggendo i passi dei testi che contengono una parola chiave o un richiamo (`src/validation/sample_passages.py`), prima di eseguire l'estrattore su questo campione e senza vederne il risultato. Non è un'annotazione umana, e non copre i testi interi. Campione: primo campione di verifica, 4 pronunce per decennio e tipo, seed 20261117. Dopo la prima misura (conservata in `validation_round1.md`) l'estrattore è stato corretto guardando gli errori di questo campione: i numeri qui sotto non sono più una stima indipendente. È separato da quello usato per mettere a punto l'estrattore (2 per strato, seed 20261116). Per il controllo a campione di una persona: `data/validation/gold_test.txt` elenca per ogni pronuncia le citazioni annotate.

Intervalli di confidenza al 95% di Wilson.

| Strato | Pronunce | Coppie vere | Trovate | False | Mancate | Precisione | Richiamo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Totale** | 64 | 270 | 264 | 0 | 6 | 1.000 (0.986–1.000) | 0.978 (0.952–0.990) |
| Sentenze | 32 | 205 | 199 | 0 | 6 | 1.000 (0.981–1.000) | 0.971 (0.938–0.987) |
| Ordinanze | 32 | 65 | 65 | 0 | 0 | 1.000 (0.944–1.000) | 1.000 (0.944–1.000) |
| Anni 1950 | 8 | 9 | 8 | 0 | 1 | 1.000 (0.676–1.000) | 0.889 (0.565–0.980) |
| Anni 1960 | 8 | 11 | 11 | 0 | 0 | 1.000 (0.741–1.000) | 1.000 (0.741–1.000) |
| Anni 1970 | 8 | 14 | 14 | 0 | 0 | 1.000 (0.785–1.000) | 1.000 (0.785–1.000) |
| Anni 1980 | 8 | 10 | 10 | 0 | 0 | 1.000 (0.722–1.000) | 1.000 (0.722–1.000) |
| Anni 1990 | 8 | 43 | 42 | 0 | 1 | 1.000 (0.916–1.000) | 0.977 (0.879–0.996) |
| Anni 2000 | 8 | 31 | 31 | 0 | 0 | 1.000 (0.890–1.000) | 1.000 (0.890–1.000) |
| Anni 2010 | 8 | 48 | 48 | 0 | 0 | 1.000 (0.926–1.000) | 1.000 (0.926–1.000) |
| Anni 2020 | 8 | 104 | 100 | 0 | 4 | 1.000 (0.963–1.000) | 0.962 (0.905–0.985) |
| 1956–1986 | 27 | 40 | 39 | 0 | 1 | 1.000 (0.910–1.000) | 0.975 (0.871–0.996) |
| 1987–2026 | 37 | 230 | 225 | 0 | 5 | 1.000 (0.983–1.000) | 0.978 (0.950–0.991) |

## Coppie false (trovate dall'estrattore, assenti nell'annotazione)


## Coppie mancate (annotate, non trovate dall'estrattore)

- 19570063 → 1957/60
- 19910047 → 1972/10
- 20200056 → 2010/278
- 20200056 → 2016/63
- 20200056 → 2016/110
- 20200056 → 2016/242