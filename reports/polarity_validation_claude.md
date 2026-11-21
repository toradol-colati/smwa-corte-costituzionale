# Polarità delle citazioni: validazione (Claude)

Generato da `src/polarity/evaluate.py`. Campione: tutti i contesti segnalati della metà di prova, mescolati con contesti della stessa metà che hanno una parola di distinzione ma non sono segnalati; annotati senza vedere l'etichetta. Unità: il contesto.

## In breve

Questo file misura quanto sono affidabili le regole che cercano le citazioni in cui la Corte prende le distanze da un proprio precedente. L'assistente ha letto i passi senza sapere che cosa avevano deciso le regole. La precisione è la quota di passi segnalati che sono davvero distinzioni; la soglia decisa prima era 0,80, e non è stata superata: le regole non sono state usate nelle analisi. Attenzione: chi ha letto i passi aveva anche scritto le regole.

- Precisione dei contesti segnalati: **28 su 37 = 0.757** (intervallo di Wilson 0.599–0.866); soglia fissata prima: 0,80. NON superata: niente analisi.
- Tra i 30 contesti non segnalati che hanno una parola di distinzione, le vere distinzioni sono 5 (0.167; 0.073–0.336): il lessico ne perde una parte, e altre forme sfuggono del tutto. La quota trovata è un limite inferiore.

| Regola | Contesti segnalati | Veri |
| --- | --- | --- |
| caso_diverso | 8 | 7 |
| non_affermato | 1 | 0 |
| non_pertinente | 21 | 19 |
| superamento | 7 | 2 |

L'annotatore (Claude) ha scritto anche le regole: l'annotazione non è indipendente. Il foglio per una persona è `data/validation/polarity_human_check.md`.