# Validazione dell'estrazione delle citazioni

Generato da `src/validation/evaluate.py`. Unità: la coppia (pronuncia che cita, pronuncia citata) nel testo di base.

**Chi ha annotato.** L'annotazione di riferimento (`data/validation/gold_test.txt`) è stata fatta da Claude leggendo i passi dei testi che contengono una parola chiave o un richiamo (`src/validation/sample_passages.py`), prima di eseguire l'estrattore su questo campione e senza vederne il risultato. Non è un'annotazione umana. Il campione di verifica (4 pronunce per decennio e tipo, seed 20261117) è separato da quello usato per mettere a punto l'estrattore (2 per strato, seed 20261116). Per il controllo a campione di Umberto: `data/validation/gold_test.txt` elenca per ogni pronuncia le citazioni annotate.

Intervalli di confidenza al 95% di Wilson.

| Strato | Pronunce | Coppie vere | Trovate | False | Mancate | Precisione | Richiamo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Totale** | 64 | 270 | 254 | 0 | 16 | 1.000 (0.985–1.000) | 0.941 (0.906–0.963) |
| Sentenze | 32 | 205 | 189 | 0 | 16 | 1.000 (0.980–1.000) | 0.922 (0.877–0.951) |
| Ordinanze | 32 | 65 | 65 | 0 | 0 | 1.000 (0.944–1.000) | 1.000 (0.944–1.000) |
| Anni 1950 | 8 | 9 | 4 | 0 | 5 | 1.000 (0.510–1.000) | 0.444 (0.189–0.733) |
| Anni 1960 | 8 | 11 | 11 | 0 | 0 | 1.000 (0.741–1.000) | 1.000 (0.741–1.000) |
| Anni 1970 | 8 | 14 | 11 | 0 | 3 | 1.000 (0.741–1.000) | 0.786 (0.524–0.924) |
| Anni 1980 | 8 | 10 | 8 | 0 | 2 | 1.000 (0.676–1.000) | 0.800 (0.490–0.943) |
| Anni 1990 | 8 | 43 | 41 | 0 | 2 | 1.000 (0.914–1.000) | 0.953 (0.845–0.987) |
| Anni 2000 | 8 | 31 | 31 | 0 | 0 | 1.000 (0.890–1.000) | 1.000 (0.890–1.000) |
| Anni 2010 | 8 | 48 | 48 | 0 | 0 | 1.000 (0.926–1.000) | 1.000 (0.926–1.000) |
| Anni 2020 | 8 | 104 | 100 | 0 | 4 | 1.000 (0.963–1.000) | 0.962 (0.905–0.985) |
| 1956–1986 | 27 | 40 | 30 | 0 | 10 | 1.000 (0.886–1.000) | 0.750 (0.598–0.858) |
| 1987–2026 | 37 | 230 | 224 | 0 | 6 | 1.000 (0.983–1.000) | 0.974 (0.944–0.988) |

## Coppie false (trovate dall'estrattore, assenti nell'annotazione)


## Coppie mancate (annotate, non trovate dall'estrattore)

- 19570063 → 1957/59
- 19570063 → 1957/60
- 19580056 → 1957/3
- 19580056 → 1957/28
- 19580056 → 1958/53
- 19700051 → 1970/50
- 19790042 → 1966/63
- 19790042 → 1972/174
- 19850095 → 1977/16
- 19850095 → 1982/168
- 19900285 → 1964/66
- 19910047 → 1972/10
- 20200056 → 2010/278
- 20200056 → 2016/63
- 20200056 → 2016/110
- 20200056 → 2016/242