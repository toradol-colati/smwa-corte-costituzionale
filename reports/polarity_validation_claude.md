# Le citazioni in cui la Corte prende le distanze da un precedente: controllo delle regole (letto da Claude)

Prodotto da `src/polarity/evaluate.py`. Le regole cercano nel testo, intorno a una citazione, le frasi con cui la Corte dice che un proprio precedente non si applica o non va seguito (`src/polarity/lexicon.py`). Ogni passo controllato è il pezzo di testo intorno a una citazione (il "contesto").

## In breve

Questo file controlla le regole che cercano le citazioni in cui la Corte prende le distanze da un proprio precedente. La quota di passi segnalati che sono davvero distinzioni sta sotto la soglia decisa prima (0,80): per questo le regole non sono state usate nelle analisi. Il controllo, inoltre, l'ha fatto chi aveva scritto le regole.

**Il campione.** Tutti i passi segnalati dalle regole nella metà dei dati tenuta da parte per la prova, mescolati con passi della stessa metà che contengono una parola tipica delle distinzioni ma che le regole non hanno segnalato. Chi ha letto i passi non sapeva quali erano stati segnalati.

- **Precisione** (quanti dei passi segnalati sono davvero distinzioni): **28 su 37 = 0,757**; intervallo al 95%, calcolato con il metodo di Wilson: 0,599–0,866. La soglia decisa prima era 0,80: non superata, quindi le regole non sono state usate nelle analisi.
- Tra i 30 passi non segnalati che contengono una parola tipica delle distinzioni, le vere distinzioni sono 5 (0,167; intervallo 0,073–0,336). Quindi le regole ne perdono una parte; e altre distinzioni, scritte senza quelle parole, sfuggono del tutto. Quante distinzioni le regole perdono davvero non si può misurare: questo numero dà solo un minimo.

**I passi segnalati, regola per regola**

| Regola | Che cosa cerca | Passi segnalati | Di cui distinzioni vere |
| --- | --- | --- | --- |
| `caso_diverso` | il caso di oggi è diverso da quello deciso allora ("a differenza di quanto deciso", "non è assimilabile a quella esaminata") | 8 | 7 |
| `non_affermato` | il precedente non ha detto quello che gli si attribuisce ("la sentenza non ha affermato") | 1 | 0 |
| `non_pertinente` | il richiamo al precedente non è pertinente ("il richiamo non è conferente") | 21 | 19 |
| `superamento` | la Corte cambia orientamento ("superare il precedente", "mutamento di giurisprudenza") | 7 | 2 |

**Attenzione.** Chi ha letto i passi (Claude) aveva anche scritto le regole: il controllo non è indipendente. Il foglio per il controllo di una persona è `data/validation/polarity_human_check.md`.
