# Validazione dell'estrazione delle citazioni

Generato da `src/validation/evaluate.py`. Unità: la coppia (pronuncia che cita, pronuncia citata) nel testo di base.

**Chi ha annotato.** L'annotazione di riferimento (`data/validation/gold_test2.txt`) è stata fatta da Claude leggendo i passi dei testi che contengono una parola chiave o un richiamo (`src/validation/sample_passages.py`), prima di eseguire l'estrattore su questo campione e senza vederne il risultato. Non è un'annotazione umana. Campione: secondo campione di verifica, solo pronunce fino alla 286/1986, 6 per decennio e tipo, seed 20261118, estratto dopo la correzione dell'estrattore e mai usato per metterlo a punto. È separato da quello usato per mettere a punto l'estrattore (2 per strato, seed 20261116). Per il controllo a campione di una persona: `data/validation/gold_test2.txt` elenca per ogni pronuncia le citazioni annotate.

Intervalli di confidenza al 95% di Wilson.

| Strato | Pronunce | Coppie vere | Trovate | False | Mancate | Precisione | Richiamo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Totale** | 48 | 72 | 66 | 1 | 6 | 0.985 (0.920–0.997) | 0.917 (0.830–0.961) |
| Sentenze | 24 | 47 | 43 | 1 | 4 | 0.977 (0.882–0.996) | 0.915 (0.801–0.966) |
| Ordinanze | 24 | 25 | 23 | 0 | 2 | 1.000 (0.857–1.000) | 0.920 (0.750–0.978) |
| Anni 1950 | 12 | 16 | 14 | 0 | 2 | 1.000 (0.785–1.000) | 0.875 (0.640–0.965) |
| Anni 1960 | 12 | 26 | 25 | 0 | 1 | 1.000 (0.867–1.000) | 0.962 (0.811–0.993) |
| Anni 1970 | 12 | 17 | 16 | 1 | 1 | 0.941 (0.730–0.990) | 0.941 (0.730–0.990) |
| Anni 1980 | 12 | 13 | 11 | 0 | 2 | 1.000 (0.741–1.000) | 0.846 (0.578–0.957) |
| 1956–1986 | 48 | 72 | 66 | 1 | 6 | 0.985 (0.920–0.997) | 0.917 (0.830–0.961) |
| 1987–2026 | 0 | 0 | 0 | 0 | 0 | nan (nan–nan) | nan (nan–nan) |

## Coppie false (trovate dall'estrattore, assenti nell'annotazione)

- 19770079 → 1975/112

## Coppie mancate (annotate, non trovate dall'estrattore)

- 19580016 → 1957/46
- 19590017 → 1958/70
- 19690158 → 1967/48
- 19710209 → 1965/119
- 19820188 → 1971/45
- 19820188 → 1971/183