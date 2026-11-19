# Le altre corti: contesto e dati

> Documento di lavoro, 19/11/2026. Serve a decidere se e come costruire una rete tra la Corte costituzionale e altre quattro corti: Corte di cassazione, Consiglio di Stato, Corte europea dei diritti dell'uomo, Corte di giustizia dell'Unione europea. Richiesta di Umberto del 19/11: le corti differiscono per funzione, ambito, peso, composizione e forma delle decisioni, e i loro dati per natura e formato, quindi non si confrontano senza questo controllo.

**Stati.** *Fonte*: verificata sulla pagina indicata, letta il 19/11/2026. *Dati*: verificata sui file della Corte costituzionale. *Non verificato*: pagina non raggiungibile o informazione non trovata. Le citazioni testuali sono brevi e servono solo a documentare la fonte.

## 1. Le quattro corti a confronto

| | Corte di cassazione | Consiglio di Stato | Corte europea dei diritti dell'uomo | Corte di giustizia dell'UE |
| --- | --- | --- | --- | --- |
| Che cosa fa | Vertice della giurisdizione ordinaria; funzione "nomofilattica ed unificatrice": garantisce "l'esatta osservanza e l'uniforme interpretazione della legge" (art. 65 dell'ordinamento giudiziario). Giudica la legittimità, non i fatti. *Fonte* [CASS-1] | Giudice amministrativo d'appello (i TAR giudicano in primo grado) e organo consultivo del Governo; "organo di rilevanza costituzionale" (art. 100 Cost.). *Fonte* [CDS-1] | Applica la Convenzione europea dei diritti dell'uomo agli Stati che vi aderiscono (46). *Fonte* [EDU-1] | Interpreta il diritto dell'Unione; oltre il 60% delle cause sono rinvii pregiudiziali dei giudici nazionali; poi ricorsi per inadempimento, annullamento, impugnazioni. *Fonte* [CGUE-1] |
| Chi decide | Sezioni civili e penali (sette sezioni penali), Sezioni Unite; Ufficio del Massimario con 67 magistrati. Numero complessivo dei consiglieri *non verificato*. *Fonte* [CASS-2], [CASS-3] | Sei sezioni giurisdizionali (II–VII), collegi di cinque magistrati; Adunanza plenaria (Presidente più dodici magistrati); sezioni consultive. *Fonte* [CDS-1] | Giudice unico, comitati di tre giudici, camere, Grande Camera. Dimensione di camere e Grande Camera *non verificata*. *Fonte* [EDU-1] | 27 giudici e 11 avvocati generali; sezioni di 3 e 5 giudici, Grande Camera di 15; l'avvocato generale presenta conclusioni che i giudici non sono obbligati a seguire. *Fonte* [CGUE-1] |
| Come si identifica una decisione | Numero, data dell'udienza e del deposito, sezione (per esempio "Sentenza n. 39655 ud. 07/10/2026 - deposito del 11/11/2026"). Se la numerazione sia separata per civile e penale *non verificato*. Nessun ECLI italiano trovato. *Fonte* [CASS-1], [ECLI-IT] | Sezione, data, numero ("Consiglio di Stato, sezione V, 24 settembre 2026, n. 7058"), numero di registro generale. Nessun ECLI trovato. *Fonte* [CDS-2], [ECLI-IT] | Nome del caso ("X c. Italia"), data; numero di ricorso e formato ECLI *non verificati*. Lingue ufficiali: inglese e francese; le traduzioni italiane non sono ufficiali. *Fonte* [EDU-2], [EDU-3] | Numero di causa "C-numero/anno" (per esempio C-250/25), nomi delle parti (dal 2023 nomi fittizi nei rinvii che riguardano persone), data, ECLI nella forma EU:C:anno:numero; 24 lingue ufficiali, italiano compreso. *Fonte* [CGUE-2] |
| Dati pubblicati | Motore di ricerca SentenzeWeb: copertura, formati e accesso *non verificati* (pagina non raggiungibile per un errore di certificato). *Fonte* [CASS-1] | Ricerca dei provvedimenti dal 1908 in HTML e PDF; portale Open GA (dal 2024) con 436 dataset in CSV, JSON e ODS, in gran parte dati aggregati (ricorsi, esiti, provvedimenti per sezione e tipo). Se contengano singole decisioni *non verificato*. *Fonte* [CDS-2], [CDS-3] | Banca dati HUDOC: sentenze e decisioni di Grande Camera, camere e comitati, casi comunicati, pareri consultivi; le decisioni del giudice unico non sono pubblicate; quelle dei comitati solo da aprile 2010. API, esportazione massiva e licenza *non verificate*. *Fonte* [EDU-2] | CURIA (ricerca) e CELLAR dell'Ufficio delle pubblicazioni: endpoint SPARQL (`https://publications.europa.eu/webapi/rdf/sparql`) e accesso REST con formati PDF, HTML/XHTML, XML Formex, RDF. Licenza di riuso *non verificata* (pagine di EUR-Lex non raggiungibili). *Fonte* [CGUE-3] |
| Riuso | Solo uso personale; vietati distribuzione e riuso "anche con sistemi di Intelligenza Artificiale"; vietati gli "accessi massivi" con strumenti automatici. *Fonte* [CASS-4] | Decisioni protette dal diritto d'autore, uso non commerciale con indicazione della fonte, vietati gli "accessi massivi"; i dataset di Open GA sono in licenza CC BY 4.0. *Fonte* [CDS-3], [CDS-4] | *Non verificato*. Le traduzioni non ufficiali sono protette. *Fonte* [EDU-3] | *Non verificato*. |

## 2. Come le nomina la Corte costituzionale

*Dati* (`src/courts/sizing.py`, `reports/courts_sizing.json`): pronunce della Corte costituzionale che nominano ciascuna corte nel testo di base («Considerato in diritto» e dispositivo).

| Corte | Pronunce che la nominano | Con un identificativo di decisione vicino | Menzioni |
| --- | --- | --- | --- |
| Corte di cassazione | 3.172 | 1.349 | 8.810 |
| Consiglio di Stato | 1.053 | 369 | 2.910 |
| Corte di giustizia dell'UE | 442 | 230 | 1.760 |
| Corte europea dei diritti dell'uomo | 405 | 221 | 1.906 |

"Identificativo vicino" vuol dire soltanto che entro 160 caratteri compare un numero, un "c." o "contro", oppure un numero di causa: è una misura grezza, non un'estrazione. Molte menzioni sono generiche ("la giurisprudenza di legittimità", "il diritto vivente"), e non indicano una decisione.

## 3. Conseguenze per la rete tra corti

1. **Si può costruire in un solo verso.** I testi della Corte costituzionale sono in licenza CC BY-SA 3.0, e da lì si possono estrarre le citazioni alle altre corti. Il verso opposto (le altre corti che citano la Corte costituzionale) richiederebbe i loro dati. Per la Cassazione il riuso e l'accesso automatico sono vietati; per il Consiglio di Stato le decisioni non sono riusabili in blocco; per le due corti europee la licenza non è verificata. Una rete simmetrica tra corti non è quindi costruibile con dati aperti.
2. **Che cosa si confronta.** Con un solo verso, la rete descrive come la Corte costituzionale si riferisce a ciascuna corte, non che cosa producono le corti. Le differenze di funzione (legittimità, giustizia amministrativa, diritti della Convenzione, diritto dell'Unione) spiegano perché la Corte le nomina per ragioni diverse, e vanno dette prima di qualsiasi confronto.
3. **Ogni corte ha il suo modo di essere citata.** Numero e data per Cassazione e Consiglio di Stato, nome del caso per la Corte europea dei diritti dell'uomo, numero di causa per la Corte di giustizia. Nessuna ha un ECLI utilizzabile per le corti italiane. Serve un estrattore, e una validazione, per ogni corte; i conteggi tra corti si confrontano solo con il richiamo di ciascun estrattore.
4. **Riferimento generico o decisione precisa.** Per la Cassazione il riferimento generico al suo orientamento può avere un peso proprio, distinto dalla citazione di una sentenza. Il concetto (per esempio il "diritto vivente") va definito con una fonte letta prima di usarlo; oggi non c'è.

## 4. Da verificare prima di costruire la rete

- Copertura, formati e accesso di SentenzeWeb (Cassazione).
- Contenuto dei dataset di Open GA: se ci sono le singole decisioni o solo aggregati.
- Composizione delle formazioni della Corte europea dei diritti dell'uomo, formato ECLI e numeri di ricorso, licenza di HUDOC (manuale e regolamento in PDF non leggibili oggi).
- Licenza di riuso dei dati della Corte di giustizia (EUR-Lex, CELLAR).
- Struttura delle decisioni di ciascuna corte, e se esistono opinioni separate.
- Una definizione con fonte del "diritto vivente".

## Fonti lette il 19/11/2026

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
- [ECLI-IT] https://e-justice.europa.eu/topics/legislation-and-case-law/european-case-law-identifier-ecli/it_en (aggiornata al 13/10/2020: per l'Italia il coordinatore nazionale ECLI "has not yet been appointed")

Non raggiungibili: https://www.italgiure.giustizia.it/sncass/ (errore di certificato), le pagine di EUR-Lex sul riuso dei dati, i PDF del manuale di HUDOC e del regolamento della Corte europea.
