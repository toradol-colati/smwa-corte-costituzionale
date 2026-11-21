"""Adds a short plain-language introduction ("In breve") to the reports written by the analysis scripts, right after
their first paragraph, so that each file says what it contains and how to read it. Run after the scripts that write
these reports (they overwrite the files); running it twice changes nothing.
Usage: .venv/bin/python src/report/plain_intros.py
"""
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VALID = "Il quadro di tutti i controlli, spiegato, è in `reports/validation.md`."
INTROS = {
    "data_inspection.md": "Questo file è il primo controllo fatto sui file scaricati dal portale, prima di qualsiasi analisi: com'è fatto ogni file, "
        "quanto è completo anno per anno, se i dati sono coerenti tra loro. Le cose più importanti che ne sono uscite: la numerazione delle "
        "pronunce non ha buchi né doppioni; il nome di chi ha scritto la pronuncia c'è solo dal dicembre 1986; l'elenco ufficiale dei giudici "
        "ha date mancanti o sbagliate. Le tabelle sono prodotte da un programma e usano i nomi tecnici dei campi, spiegati in "
        "`docs/data_schema.md` e `docs/context.md`.",
    "judges_quality.md": "Questo file dice quanto bene il programma ha riconosciuto i giudici: chi ha scritto ciascuna pronuncia e chi "
        "sedeva nel collegio, collegando i nomi all'elenco ufficiale dei giudici. Le due soglie decise prima (98% per entrambe le cose) "
        "sono superate. Per le pronunce fino alla 286/1986 il nome di chi ha scritto non c'è: al suo posto si usa il relatore.",
    "sparql_reconciliation.md": "Questo file confronta i file scaricati con una seconda fonte ufficiale della Corte, la sua banca dati "
        "interrogabile con il linguaggio SPARQL, per scoprire errori nei file. Il risultato principale: il relatore coincide quasi sempre, e "
        "quasi tutte le differenze sono due errori di grafia nei file (\"Caianello\" per Caianiello, \"Capolozza\" per Capalozza), poi "
        "corretti. Le tabelle usano i nomi tecnici della banca dati.",
    "topics.md": "Questo file descrive come è stata ricavata la materia di ogni pronuncia, con le prove fatte per scegliere il numero di "
        "temi e per controllarli. I temi vanno d'accordo con i titoli delle massime e con gli articoli della Costituzione invocati, molto "
        "più che per caso; però cambiano parecchio ripetendo il calcolo, e alcuni raccolgono formule ricorrenti di scrittura più che una "
        "materia. Per questo la materia serve come controllo nei confronti, non come classificazione precisa.",
    "d3_results.md": "Questo file contiene i numeri di D3, il risultato principale del lavoro: un giudice cita di più i precedenti decisi "
        "da collegi in cui sedeva, rispetto a quelli decisi mentre era in carica ma assente? La risposta è no: il numero che lo misura "
        "(l'odds ratio) vale 1, cioè nessuna differenza, e resta vicino a 1 in tutte le prove. Il giudice cita molto di più, invece, le "
        "pronunce che ha scritto lui. Le tabelle spiegano riga per riga che cosa è stato provato; la lettura completa è nella relazione, "
        "sezione 3.4.",
    "validation_round1.md": "Questo file è la prima misura dell'affidabilità del programma che trova le citazioni, fatta prima di "
        "correggerlo. Il programma non trovava mai citazioni sbagliate, ma nelle pronunce fino al 1986 perdeva troppe citazioni vere: lì "
        "il richiamo stava sotto la soglia decisa prima (0,90). Per questo il programma è stato corretto. " + VALID,
    "validation_test.md": "Questo file rifà il calcolo sul primo campione dopo la correzione del programma. Non è una misura indipendente, "
        "perché la correzione è stata scritta guardando gli errori di questo stesso campione: serve solo a controllare che la correzione "
        "non abbia rotto altro, cioè che non abbia aggiunto citazioni sbagliate. " + VALID,
    "validation_test2.md": "Questo file misura l'affidabilità del programma che trova le citazioni su un secondo campione, mai visto prima, "
        "di pronunce fino alla 286/1986, dopo la correzione. Precisione e richiamo superano le soglie decise prima (0,95 e 0,90), ma il "
        "campione è piccolo: il limite inferiore dell'intervallo del richiamo resta sotto 0,90. " + VALID,
    "polarity_validation_claude.md": "Questo file controlla le regole che cercano le citazioni in cui la Corte prende le distanze da un "
        "proprio precedente. La quota di passi segnalati che sono davvero distinzioni sta sotto la soglia decisa prima (0,80): per questo "
        "le regole non sono state usate nelle analisi. Il controllo, inoltre, l'ha fatto chi aveva scritto le regole.",
}


def add(name, text):
    """Insert the introduction, or replace it if the text has changed. Returns what was done."""
    p = REPO / "reports" / name
    s = p.read_text(encoding="utf-8")
    head = "\n## In breve\n\n"
    if head in s:
        a = s.index(head) + len(head)
        b = s.index("\n\n", a) if "\n\n" in s[a:] else len(s)
        if s[a:b] == text:
            return "already there"
        p.write_text(s[:a] + text + s[b:], encoding="utf-8")
        return "updated"
    first = s.index("\n\n", s.index("\n\n") + 2)  # end of the paragraph after the title
    p.write_text(s[:first] + "\n" + head + text + s[first:], encoding="utf-8")
    return "added"


if __name__ == "__main__":
    for name, text in INTROS.items():
        print(name, add(name, text))
