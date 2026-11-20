# Le altre corti: contesto e dati

> Documento di lavoro, 19/11/2026. Serve a decidere se e come costruire una rete tra la Corte costituzionale e altre quattro corti: Corte di cassazione, Consiglio di Stato, Corte europea dei diritti dell'uomo, Corte di giustizia dell'Unione europea. Richiesta di Umberto del 19/11: le corti differiscono per funzione, ambito, peso, composizione e forma delle decisioni, e i loro dati per natura e formato, quindi non si confrontano senza questo controllo.

**Stati.** *Fonte*: verificata sulla pagina indicata, letta il 19/11/2026. *Dati*: verificata sui file della Corte costituzionale. *Non verificato*: pagina non raggiungibile o informazione non trovata. Le citazioni testuali sono brevi e servono solo a documentare la fonte.

## 1. Le quattro corti a confronto

| | Corte di cassazione | Consiglio di Stato | Corte europea dei diritti dell'uomo | Corte di giustizia dell'UE |
| --- | --- | --- | --- | --- |
| Che cosa fa | Vertice della giurisdizione ordinaria; funzione "nomofilattica ed unificatrice": garantisce "l'esatta osservanza e l'uniforme interpretazione della legge" (art. 65 dell'ordinamento giudiziario). Giudica la legittimità, non i fatti. *Fonte* [CASS-1] | Giudice amministrativo d'appello (i TAR giudicano in primo grado) e organo consultivo del Governo; "organo di rilevanza costituzionale" (art. 100 Cost.). *Fonte* [CDS-1] | Giudica sulla Convenzione europea dei diritti dell'uomo, a cui aderiscono 46 Stati (*Fonte* [EDU-1]); la descrizione attuale delle sue competenze *non verificata* | Interpreta il diritto dell'Unione; oltre il 60% delle cause sono rinvii pregiudiziali dei giudici nazionali; poi ricorsi per inadempimento, annullamento, impugnazioni. *Fonte* [CGUE-1] |
| Chi decide | Sezioni civili e penali (sette sezioni penali), Sezioni Unite; Ufficio del Massimario con 67 magistrati. Numero complessivo dei consiglieri *non verificato*. *Fonte* [CASS-2], [CASS-3] | Sei sezioni giurisdizionali (II–VII), collegi di cinque magistrati; Adunanza plenaria (Presidente più dodici magistrati); sezioni consultive. *Fonte* [CDS-1] | Giudice unico, comitati di tre giudici, camere di sette giudici, Grande Camera di diciassette. *Fonte* [EDU-1], [EDU-4] | 27 giudici e 11 avvocati generali; sezioni di 3 e 5 giudici, Grande Camera di 15; l'avvocato generale presenta conclusioni che i giudici non sono obbligati a seguire. *Fonte* [CGUE-1] |
| Come si identifica una decisione | Numero, data dell'udienza e del deposito, sezione (per esempio "Sentenza n. 39655 ud. 07/10/2026 - deposito del 11/11/2026"). Se la numerazione sia separata per civile e penale *non verificato*. Nessun ECLI italiano trovato. *Fonte* [CASS-1], [ECLI-IT] | Sezione, data, numero ("Consiglio di Stato, sezione V, 24 settembre 2026, n. 7058"), numero di registro generale. Nessun ECLI trovato. *Fonte* [CDS-2], [ECLI-IT] | Nome del caso ("X c. Italia"), data; numero di ricorso e formato ECLI *non verificati*. Lingue ufficiali: inglese e francese; le traduzioni italiane non sono ufficiali. *Fonte* [EDU-2], [EDU-3] | Numero di causa "C-numero/anno" (per esempio C-250/25), nomi delle parti (dal 2023 nomi fittizi nei rinvii che riguardano persone), data, ECLI nella forma EU:C:anno:numero; 24 lingue ufficiali, italiano compreso. *Fonte* [CGUE-2] |
| Dati pubblicati | Motore di ricerca SentenzeWeb: copertura, formati e accesso *non verificati* (pagina non raggiungibile per un errore di certificato). *Fonte* [CASS-1] | Ricerca dei provvedimenti con un filtro per anno dal 1908 (quanto testo ci sia per ogni anno *non verificato*) e collegamenti a file HTML e PDF; portale Open GA (dal 2024) con 436 dataset in CSV, JSON e ODS, in gran parte dati aggregati (ricorsi, esiti, provvedimenti per sezione e tipo). Se contengano singole decisioni *non verificato*. *Fonte* [CDS-2], [CDS-3] | Banca dati HUDOC: sentenze e decisioni di Grande Camera, camere e comitati, casi comunicati, pareri consultivi; le decisioni del giudice unico non sono pubblicate; quelle dei comitati solo da aprile 2010. Gli elenchi dei risultati si esportano in CSV o Excel, i documenti si scaricano uno per uno; nessuna API, nessun accesso in blocco e nessuna licenza trovati nel manuale e nelle FAQ. *Fonte* [EDU-2], [EDU-5] | CURIA (ricerca) e CELLAR dell'Ufficio delle pubblicazioni: endpoint SPARQL (`https://publications.europa.eu/webapi/rdf/sparql`) e accesso REST con formati PDF, HTML/XHTML, XML Formex, RDF; EUR-Lex offre anche un servizio web agli utenti registrati. Fanno fede solo le versioni pubblicate nella Raccolta della giurisprudenza. *Fonte* [CGUE-3], [EURLEX] |
| Riuso | Solo uso personale; vietati distribuzione e riuso "anche con sistemi di Intelligenza Artificiale"; vietati gli "accessi massivi" con strumenti automatici. *Fonte* [CASS-4] | Decisioni protette dal diritto d'autore, uso non commerciale con indicazione della fonte, vietati gli "accessi massivi"; i dataset di Open GA sono in licenza CC BY 4.0. *Fonte* [CDS-3], [CDS-4] | Condizioni di riuso *non trovate*. Le traduzioni non ufficiali sono protette. *Fonte* [EDU-3] | Documenti di EUR-Lex riutilizzabili, "unless otherwise specified", a fini commerciali e non (decisione 2011/833/UE); metadati di pubblico dominio (CC0). *Fonte* [EURLEX] |

## 2. Come le nomina la Corte costituzionale

*Dati* (`src/courts/sizing.py`, `reports/courts_sizing.json`): pronunce della Corte costituzionale che nominano ciascuna corte nel testo di base («Considerato in diritto» e dispositivo). Conteggi rifatti il 20/11/2026: il 19/11 i nomi completi si cercavano solo con l'iniziale minuscola dopo "Corte" o "Consiglio", e per esempio "Corte di Giustizia" sfuggiva (Corte di giustizia: 472 pronunce invece di 442).

| Corte | Pronunce che la nominano | Con un identificativo di decisione vicino | Menzioni |
| --- | --- | --- | --- |
| Corte di cassazione | 3.175 | 1.349 | 8.816 |
| Consiglio di Stato | 1.058 | 372 | 2.921 |
| Corte di giustizia dell'UE | 472 | 239 | 1.849 |
| Corte europea dei diritti dell'uomo | 408 | 222 | 1.911 |

"Identificativo vicino" vuol dire soltanto che entro 160 caratteri compare un numero, un "c." o "contro", oppure un numero di causa: è una misura grezza, non un'estrazione. Molte menzioni sono generiche ("la giurisprudenza di legittimità", "il diritto vivente"), e non indicano una decisione.

## 3. Conseguenze per la rete tra corti

1. **Il verso Corte costituzionale → altre corti si può costruire; quello opposto dipende dalla corte.** I testi della Corte costituzionale sono in licenza CC BY-SA 3.0, e da lì si possono estrarre le citazioni alle altre corti. Il verso opposto (le altre corti che citano la Corte costituzionale) richiede i loro dati. Per la Cassazione riuso e accesso automatico sono vietati, e per il Consiglio di Stato le decisioni non sono riusabili in blocco: per le due corti italiane una rete simmetrica non si può costruire con dati aperti. Per la Corte di giustizia i documenti di EUR-Lex sono riutilizzabili e i metadati sono in CC0, quindi quel verso è possibile in principio. Per la Corte europea dei diritti dell'uomo le condizioni di riuso non sono state trovate.
2. **Che cosa si confronta.** Con un solo verso, la rete descrive come la Corte costituzionale si riferisce a ciascuna corte, non che cosa producono le corti. Le differenze di funzione (legittimità, giustizia amministrativa, diritti della Convenzione, diritto dell'Unione) spiegano perché la Corte le nomina per ragioni diverse, e vanno dette prima di qualsiasi confronto.
3. **Ogni corte ha il suo modo di essere citata.** Numero e data per Cassazione e Consiglio di Stato, nome del caso per la Corte europea dei diritti dell'uomo, numero di causa per la Corte di giustizia. Nessuna ha un ECLI utilizzabile per le corti italiane. Serve un estrattore, e una validazione, per ogni corte; i conteggi tra corti si confrontano solo con il richiamo di ciascun estrattore.
4. **Riferimento generico o decisione precisa.** Per la Cassazione il riferimento generico al suo orientamento può avere un peso proprio, distinto dalla citazione di una sentenza. Il concetto (per esempio il "diritto vivente") va definito con una fonte letta prima di usarlo; oggi non c'è.

## 4. Verifiche aperte: stato al 20/11/2026

| Verifica | Stato | Conseguenza |
| --- | --- | --- |
| Dati del Consiglio di Stato su Open GA | *Fonte* [CDS-5]: il dataset "CDS - Sentenze" ha una riga per sentenza (sezione, numero del provvedimento, numero di ricorso, data di pubblicazione, esito, oggetto, numero di componenti del collegio) per il 2017–2026, in licenza CC BY 4.0, senza testi | Le sentenze del Consiglio di Stato citate dalla Corte si possono verificare (esistenza di numero, anno e sezione) solo dal 2017; prima no |
| Riuso dei testi della Corte europea dei diritti dell'uomo | *Fonte* [EDU-6]: riproduzione ammessa con l'indicazione della fonte, gratuita, per uso privato o per informazione ed educazione legate all'attività della Corte; ogni altro uso chiede un permesso scritto. Nessuna licenza per l'accesso in blocco | Nessuno scaricamento in blocco da HUDOC: gli identificativi si verificano solo a mano, su un campione |
| Formato ECLI e numeri di ricorso della Corte europea dei diritti dell'uomo | *Non verificato* | Non serve per costruire la rete: la Corte costituzionale la cita per nome del caso e data |
| Corte di giustizia: metadati di CELLAR | *Fonte* [EURLEX] (19/11): metadati CC0 | I numeri di causa citati si possono verificare con i metadati, anche in automatico |
| SentenzeWeb (Cassazione) | Non più necessario | Le condizioni d'uso vietano accessi massivi e riuso con sistemi di intelligenza artificiale [CASS-4]: nessuna verifica automatica degli identificativi della Cassazione, solo controlli a mano |
| Struttura delle decisioni e opinioni separate | *Non verificato* | Resta un limite del confronto tra corti; non serve per estrarre le citazioni |
| Definizione con fonte del "diritto vivente" | *Non verificato* | Il concetto non si usa: i riferimenti generici a una corte si contano come tali, senza qualificarli |

## 5. Che cosa è già stato visto dei dati

`src/courts/sizing.py` (19/11) ha contato, su tutte le pronunce e per decennio, quante nominano ciascuna corte (sezione 2), e ha fissato la divisione delle pronunce in due metà, sviluppo e prova (seed 20261123, `data/interim/courts_split.csv`). Conseguenze: le regole degli estrattori si scrivono leggendo solo la metà di sviluppo, e la metà di prova resta mai letta; ma l'andamento per decennio è già noto, quindi ogni ipotesi sull'andamento nel tempo è esplorativa.

## Fonti lette il 19/11/2026 (e il 20/11/2026, dove indicato)

- [CASS-1] https://www.cortedicassazione.it e https://www.cortedicassazione.it/it/le_funzioni_della_corte.page
- [CASS-2] https://www.cortedicassazione.it/it/organizzazione_delle_attivita.page
- [CASS-3] https://www.cortedicassazione.it/it/massimario.page
- [CASS-4] https://www.cortedicassazione.it/it/note_legali.page
- [CDS-1] https://www.giustizia-amministrativa.it/web/guest/funzioni-della-giustizia-amministrativa
- [CDS-2] https://www.giustizia-amministrativa.it/web/guest/provvedimenti-cds e la home page del sito
- [CDS-3] https://openga.giustizia-amministrativa.it (home, /about, /dataset)
- [CDS-4] https://www.giustizia-amministrativa.it/web/guest/condizioni-di-utilizzo
- [EDU-1] https://www.echr.coe.int/web/echr/how-the-court-works
- [EDU-2] https://www.echr.coe.int/web/echr/hudoc-database
- [EDU-3] https://www.echr.coe.int/web/echr/rules-of-court e https://www.echr.coe.int/case-law-translations
- [CGUE-1] https://curia.europa.eu/site/jcms/d2_5391/en/about-the-court-of-justice
- [CGUE-2] https://curia.europa.eu/site/jcms/d2_5132/en/case-names-and-citations
- [CGUE-3] https://op.europa.eu/en/web/cellar e le sue pagine sui dati
- [EDU-4] Regolamento della Corte europea dei diritti dell'uomo, edizione del 15 settembre 2025 (PDF), art. 1 (definizioni di camera e Grande Camera)
- [EDU-5] Manuale di HUDOC (ottobre 2022) e FAQ (gennaio 2026), PDF
- [EURLEX] https://eur-lex.europa.eu/content/legal-notice/legal-notice.html (note legali e politica di riuso)
- [CDS-5] https://openga.giustizia-amministrativa.it/dataset/cds-sentenze e la pagina della risorsa 2017–2024 con il dizionario dei dati (20/11/2026)
- [EDU-6] https://www.echr.coe.int/copyright-and-disclaimer (20/11/2026)
- [ECLI-IT] https://e-justice.europa.eu/topics/legislation-and-case-law/european-case-law-identifier-ecli/it_en (aggiornata al 13/10/2020: per l'Italia il coordinatore nazionale ECLI "has not yet been appointed")

Non raggiungibili: https://www.italgiure.giustizia.it/sncass/ (errore di certificato) e le pagine di EUR-Lex sul riuso dei dati collegati (`data-reuse`), sostituite dalle note legali. I PDF della Corte europea sono stati letti estraendone il testo.
