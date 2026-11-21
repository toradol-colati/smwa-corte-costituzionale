# Il contesto: come nasce una pronuncia e che cosa registrano i dati

> Documento di lavoro. Serve a sapere che cosa si sta misurando prima di misurarlo, ed è la base delle spiegazioni della relazione. Ogni affermazione ha una fonte e uno stato. I numeri sui dati vengono da `src/ingest/inspect_raw.py` (risultati in `reports/data_inspection.md`), sui file scaricati l'8/11/2026 (`data/raw/MANIFEST.csv`).

**Che cosa vogliono dire gli stati.** *Fonte*: verificato leggendo la fonte indicata. *Dati*: verificato sui file del portale. *Da verificare*: non ancora controllato su una fonte originale.

## Perché serve questo documento

Una pronuncia della Corte costituzionale non è l'opera di un solo giudice. La decide il collegio, a maggioranza, in camera di consiglio (la riunione riservata dei giudici); poi un giudice ne scrive le motivazioni e il collegio approva il testo. Chi legge i dati senza sapere questo misura altro da ciò che crede: per esempio attribuisce a chi ha scritto una decisione che è del collegio. In più, come mostra la sezione 5, i dati non registrano le stesse cose in tutti i periodi.

## Le fonti

**Lette per questo documento**
- [Legge 11 marzo 1953, n. 87](https://www.cortecostituzionale.it/documenti/filesDoc/Legge_11_marzo_1953_n_87.pdf), la legge che regola il funzionamento della Corte, nel testo aggiornato sul sito della Corte: articoli 16–19; articoli 23 e 27 letti il 18/11/2026.
- [Norme integrative per i giudizi davanti alla Corte costituzionale](https://www.cortecostituzionale.it/documenti/download/pdf/norme_integrative_2026.pdf), cioè le regole di procedura che la Corte si dà da sola, testo del 2021 aggiornato al 12 marzo 2026: articoli 9 e 20.
- [Norme integrative del 7 ottobre 2008](https://www.cortecostituzionale.it/documenti/download/pdf/CC_Fonti_NORME_INTEGRATIVE%20_05032011.pdf): articoli 7 e 17.
- Costituzione, articolo 127 (letto il 21/11/2026 sul testo di Wikisource).
- Portale open data della Corte: [Il progetto](https://dati.cortecostituzionale.it/Il_progetto/Il_progetto) (composizione della Corte, funzioni, flusso di lavoro), [I DTD](https://dati.cortecostituzionale.it/Scarica_i_dati/I_dtd/I_dtd) (la descrizione ufficiale della struttura dei file), [ECLI](https://dati.cortecostituzionale.it/ECLI/ECLI) (il codice europeo che identifica ogni decisione).
- [Annuario 2025 della Corte, I giudici e gli assistenti di studio](https://www.cortecostituzionale.it/annuario2025/giudici-e-assistenti-di-studio.html).
- A. Rauti, [Le nuove "norme integrative" della Corte](https://www.forumcostituzionale.it/wordpress/images/stories/pdf/documenti_forum/paper/0168_rauti.pdf), Forum di Quaderni costituzionali: la storia della regola sulle firme e come leggere la sostituzione del relatore.

**Raccolte il 10/11/2026.** L'elenco completo, con che cosa è stato letto di ciascuna, è in `docs/sources.md`; qui sono citate con la loro sigla (per esempio [C4]). Le più usate: Caravita 2021 [C4] e il forum del Gruppo di Pisa 2021 [C5] sulla sostituzione del relatore; la relazione del presidente Saja sul 1987 [C1]; l'elenco ufficiale dei giudici [B4]; l'Annuario 2024 [C2].

**Trovate ma non ancora lette**
- [Legge costituzionale 22 novembre 1967, n. 2](https://www.normattiva.it/eli/id/1967/11/25/067C0002/ORIGINAL), che ha ridotto il mandato dei giudici da 12 a 9 anni.
- Costituzione, articoli 134–137.
- Sul relatore sostituito e sul dissenso: M. Di Martino, [L'opinione dissenziente](https://iris.uniroma1.it/retrieve/e383532c-1eea-15e8-e053-a505fe0a3de9/DiMartino_opinione-dissenziente_2021.pdf) (2021); la [recensione di Ciommo](https://www.nomos-leattualitaneldiritto.it/wp-content/uploads/2022/06/6.-RECENSIONE-DI-CIOMMO.pdf) su Nomos (2022), che riporta uno studio con 87 casi di sostituzione; D. Tega su Quaderni costituzionali (2020).
- Il regolamento generale della Corte e il regolamento per l'ufficio studi e gli assistenti di studio.

## 1. La Corte in breve

| Che cosa | Fonte | Stato | Che cosa cambia per i dati |
| --- | --- | --- | --- |
| I giudici sono 15: 5 nominati dal Presidente della Repubblica, 5 eletti dal Parlamento in seduta comune, 5 dalle supreme magistrature (3 dalla Cassazione, 1 dal Consiglio di Stato, 1 dalla Corte dei conti) | Portale, Il progetto | Fonte | Nell'elenco dei giudici il campo `Eletto_da` ha queste cinque voci (sezione 5) |
| Il mandato dura 9 anni dal giuramento. Fino al 1967 durava 12 anni | Portale, Il progetto; legge costituzionale 2/1967 | Fonte (9 anni); Dati (12 anni prima del 1967) | I 26 giudici che hanno giurato prima del 1967 sono rimasti in carica 11,8 anni in mediana (metà più a lungo, metà meno), contro 9 dopo: in D2 i giudici dei due periodi hanno avuto opportunità diverse di scrivere pronunce |
| Il Presidente della Corte è eletto dai giudici tra di loro, con voto segreto, per 3 anni o fino alla fine del suo mandato di giudice. Sceglie un vicepresidente, decide l'ordine dei lavori, nomina i relatori e, se i voti sono pari, il suo voto decide | Portale, Il progetto; legge 87/1953 art. 16 | Fonte | Il Presidente cambia spesso: il campo `presidente` ha 84 grafie diverse |
| Che cosa fa la Corte: giudica se le leggi dello Stato e delle Regioni rispettano la Costituzione; risolve i conflitti di competenza tra poteri dello Stato e tra Stato e Regioni; decide se un referendum per abrogare una legge si può fare; giudica le accuse contro il Presidente della Repubblica | Portale, Il progetto | Fonte | Il campo `tipologia_giudizio` delle massime distingue questi casi (sezione 4) |
| I giudici sono scelti tra magistrati delle corti superiori, professori ordinari di materie giuridiche e avvocati con almeno vent'anni di professione | Costituzione art. 135 | Da verificare | La professione è scritta nella breve biografia di ogni giudice nell'elenco ufficiale: è la base della provenienza usata in D4 |
| Quando la Corte giudica un'accusa contro il Presidente della Repubblica si aggiungono sedici giudici | Costituzione art. 135 | Da verificare | Le 3 pronunce classificate come giudizio d'accusa (ordinanze del 1992 e 1996) hanno collegi di soli giudici costituzionali. La sentenza Lockheed del 2/8/1979, senza numero e decisa con i giudici aggiunti [B7], non è nell'archivio |

## 2. Chi fa che cosa in una pronuncia

| Ruolo | Che cosa fa | Che cosa non vuol dire | Fonte e stato |
| --- | --- | --- | --- |
| Collegio | Decide in camera di consiglio. Ne fanno parte i giudici presenti all'udienza o alla camera di consiglio in cui la causa è trattata; servono almeno 11 giudici. Dentro la camera di consiglio il voto è palese: vota per primo il relatore, poi gli altri dal più giovane di nomina al più anziano, per ultimo il Presidente. Decide la maggioranza assoluta dei votanti; se i voti sono pari prevale quello del Presidente | Far parte del collegio non vuol dire aver votato a favore: i voti non sono pubblicati e la Corte non pubblica opinioni dissenzienti | Fonte: legge 87/1953 art. 16; Norme integrative 2026 art. 20 |
| Presidente | Nomina uno o più giudici per studiare la causa e riferirla; dirige la discussione; se serve, affida la scrittura a un giudice diverso dal relatore; firma | Non è l'autore della pronuncia | Fonte: Norme integrative 2026 artt. 9 e 20 |
| Relatore | Studia la causa e la presenta al collegio; vota per primo | Non è detto che scriva la pronuncia, né che sia d'accordo con la decisione | Fonte: Norme integrative 2026 artt. 9 e 20 |
| Redattore | Scrive la sentenza o l'ordinanza dopo il voto. Di regola è il relatore; il Presidente può affidare la scrittura "ad altro o a più giudici", se il relatore non è disponibile o per altro motivo. Nei tribunali ordinari la stessa figura si chiama giudice estensore | Non è chi decide: il testo è approvato dal collegio | Fonte: Norme integrative 2026 art. 20, commi 4–5 |
| Assistenti di studio | Vengono dalle magistrature o dalle università; aiutano i giudici a studiare le cause e a scrivere le pronunce | Non firmano: il loro contributo non compare nei dati | Fonte: Annuario 2025 |
| Cancelliere | Firma la pronuncia e ne riceve il deposito | — | Fonte: legge 87/1953 artt. 18–19 |
| Legge impugnata (norma oggetto) e parametro | Chi porta una questione alla Corte deve indicare "le disposizioni della legge o dell'atto avente forza di legge dello Stato o di una Regione, viziate da illegittimità costituzionale" (la legge impugnata) e "le disposizioni della Costituzione o delle leggi costituzionali, che si assumono violate" (il parametro). Se dà ragione, la Corte dichiara illegittime le disposizioni "nei limiti dell'impugnazione". Nei dati: i campi `norme/norma` e `parametri/parametro` delle massime, compilati da un ufficio della Corte | Due pronunce con la stessa legge impugnata decidono questioni sulla stessa disposizione, ma non per forza la stessa questione: possono cambiare il parametro, il giudice che ha sollevato la questione o gli argomenti | Fonte: legge 87/1953 artt. 23 e 27; descrizione ufficiale dei file delle massime. Dati: almeno una legge impugnata in una massima nel 96,6% delle pronunce che hanno massime |
| Distinzione o distacco da un precedente | Definizione nostra, per il lavoro sulla polarità: la pronuncia che cita dice che il precedente non è pertinente, che riguardava un caso diverso, che non è un precedente sulla stessa questione o che non ha affermato ciò che gli si attribuisce, oppure lo supera (cambio di orientamento) | Non è un dissenso tra giudici, che nei dati non esiste, né una critica: per lo più la Corte dice soltanto che quel precedente non si applica al caso | Dati: le regole sono in `src/polarity/lexicon.py`; la prova del 18/11/2026 non ha superato la soglia (`reports/polarity_validation_claude.md`), quindi la categoria non è usata nelle analisi |
| Ufficio del massimario | Scrive le massime (i riassunti dei principi stabiliti da ogni pronuncia) e cura la raccolta ufficiale. Il portale le attribuisce al Servizio studi, che fa analisi e documentazione | Non sono giudici: le materie e i titoli delle massime sono una classificazione dell'ufficio | Fonte: Annuario 2024 [C2]; portale, Il progetto |

**Le firme sono cambiate nel tempo.**
- La legge 87/1953 (articolo 18) chiede ancora oggi la firma "dei giudici e del cancelliere".
- Le Norme integrative dicono invece che firmano il Presidente e il giudice che ha scritto la pronuncia. Rauti fa risalire questa regola a una modifica del 1987; la legge non è mai stata adeguata.
- Nei dati il passaggio è netto, ma cade prima, a dicembre 1986:
  - fino alla pronuncia 286/1986 firmano tutti i giudici del collegio, e il nome di chi ha scritto non compare da nessuna parte;
  - dalla 287/1986, depositata il 23/12/1986, firmano il Presidente e chi ha scritto.
- Caravita [C4, pp. 3–4] fa risalire la regola a una modifica delle Norme integrative del 7 luglio 1987, decisa mentre la Corte smaltiva le cause arretrate. Nella pratica la Corte ha quindi cominciato qualche mese prima. Il testo della modifica non è ancora stato letto.

**Quando chi scrive non è il relatore.**
- Da quando firma solo chi scrive, si vede anche quando il relatore è stato sostituito.
- Gli studiosi lo leggono spesso come segno che il relatore era in minoranza, ma non è sempre così: la sostituzione può avvenire anche perché il relatore non è disponibile (Rauti). Talvolta la pronuncia lo dice, come la sentenza 393/2006: "il Giudice relatore Giovanni Maria Flick, sostituito per la redazione della sentenza dal Giudice Alfonso Quaranta".
- Nei dati, dove sono compilati sia il relatore sia chi ha scritto (8.384 pronunce, quasi tutte dal 2002), i due sono diversi in 93 casi.
- Dal 2016 ci sono 17 pronunce scritte da più giudici; il relatore indicato è lo stesso gruppo, quindi non sono tra i 93 casi.
- **Il confronto con uno studio torna.** Dal 2003 al 2020 i dati danno 44 casi su 6.340 pronunce; Panizza [C5] ne conta 41 su circa 6.350 nello stesso periodo.
- Dalla fine del 2006 l'intestazione può dire che il relatore è stato "sostituito per la redazione": nei dati succede in 41 pronunce dal 2006 al 2023, meno dei casi con i due nomi diversi. La formula conferma la sostituzione, ma non segnala tutti i casi.
- Nel 1987–1989, gli anni dello smaltimento dell'arretrato, ogni causa era affidata a due giudici [C1]: lì relatore e redattore sono diversi molto più spesso, e Caravita esclude questi anni dal conteggio delle sostituzioni [C5].

**La decisione ha due tempi.** Prima si vota la decisione, poi il collegio approva il testo scritto dal redattore.
- La data della decisione è quella del voto (Norme integrative 2026, art. 20, comma 6).
- Prima che il testo sia approvato, la decisione si può cambiare solo se sono d'accordo tutti i giudici che l'hanno presa (art. 20, comma 3).
- Secondo gli studiosi citati da Rauti, in passato la Corte è tornata talvolta sulla prima decisione mentre il testo veniva scritto.

## 3. La vita di una pronuncia

1. **L'atto che apre il giudizio**, scritto in un registro della cancelleria (fonte: portale, Il progetto). I registri sono:
   - le ordinanze con cui un giudice, durante una causa, porta una questione alla Corte (R.O.);
   - i ricorsi diretti (R.R.);
   - i conflitti tra poteri dello Stato (R.C.P.);
   - i conflitti tra Stato e Regioni (R.C.E.);
   - l'ammissibilità dei referendum (AM.REF.).

   Per questo nei testi "ordinanza n. X del AAAA" può indicare un atto di un registro e non una pronuncia della Corte.
2. **La nomina del relatore** da parte del Presidente, e il decreto che fissa l'udienza pubblica o la camera di consiglio (fonte: Norme integrative, art. 9; portale).
3. **La decisione** in camera di consiglio: è la data della decisione (fonte: Norme integrative, art. 20).
4. **La scrittura** e l'approvazione del testo da parte del collegio (fonte: Norme integrative, art. 20).
5. **Il deposito** in cancelleria: da qui chiunque può conoscere la decisione (fonte: legge 87/1953, art. 19). Che cosa dicono i dati:
   - il numero della pronuncia segue l'ordine del deposito: è fuori ordine 22 volte rispetto alla data del deposito, 1.134 volte rispetto alla data della decisione;
   - l'anno è quello del deposito in tutti i casi tranne un errore di data;
   - 220 pronunce sono decise a fine anno e numerate nell'anno dopo;
   - tra la decisione e il deposito passano 9 giorni o meno per metà delle pronunce.
6. **La pubblicazione** sulla Gazzetta Ufficiale, prima serie speciale (fonte: portale). La data di pubblicazione non è nei file.
7. **Le massime**, scritte dall'Ufficio del massimario. Del 2026 il 73% delle pronunce ha già le massime; fino al 2025 tutte.

**Risposte alle domande della prima versione di questo documento**
- **Anno e numero** si assegnano al deposito, non alla decisione (Dati). Il portale scrive che nel codice ECLI c'è l'"anno decisione", ma nei file l'anno è sempre quello del deposito.
- **Quale data mette in ordine le pronunce.** Il deposito: è la data da cui una pronuncia esiste per chi la vuole citare, ed è quella che segue la numerazione (Fonte e Dati).
- **Citazioni tra pronunce dello stesso giorno.** Esistono. Un primo controllo trova 145 menzioni di pronunce depositate lo stesso giorno, e 328 pronunce contengono l'espressione "in pari data". Per esempio la pronuncia 135/1970 cita l'ordinanza 134/1970, depositata lo stesso giorno (Dati). Non sono errori di estrazione; nella rete sono tenute da parte.

## 4. Tipi di pronuncia, di giudizio e di esito

- **Tipi di pronuncia** (fonte: legge 87/1953, art. 18):
  - la sentenza decide in via definitiva;
  - l'ordinanza è "succintamente motivata", cioè ha una motivazione breve;
  - il decreto è un atto del Presidente.

  Nei file ci sono solo sentenze (11.735) e ordinanze (10.692), nessun decreto (Dati).
- **Giudizio in via incidentale**: la questione è sollevata da un giudice durante una causa (fonte: legge 87/1953, art. 23). **Giudizio in via principale**: il Governo impugna una legge regionale, oppure una Regione impugna una legge dello Stato o di un'altra Regione, entro sessanta giorni dalla pubblicazione (fonte: Costituzione, art. 127, letto il 21/11/2026 sul testo di Wikisource).
- **Tipo di giudizio nei dati**: il campo `tipologia_giudizio` delle massime c'è per tutte le pronunce tranne 8 (Dati):
  - in via incidentale: 17.052;
  - in via principale: 3.234;
  - conflitto tra Stato e Regioni (o tra Regioni): 1.026;
  - ammissibilità di un conflitto tra poteri dello Stato: 480;
  - conflitto tra poteri dello Stato: 305;
  - ammissibilità di un referendum: 153;
  - correzione di errori materiali: 140;
  - casi misti e altri.

  La categoria "correzione di errori materiali" serve per una delle prove di robustezza: il calcolo rifatto senza queste ordinanze.
- **Esito**: non è un campo dei dati. Va letto nel dispositivo ("dichiara l'illegittimità…", "dichiara non fondata…", "dichiara la manifesta inammissibilità…", "ordina la restituzione degli atti…"). È da verificare quanto la formula sia regolare nei diversi decenni.

## 5. Dal concetto al campo dei dati

| Concetto | Dove sta nei file | Copertura e avvertenze (Dati) |
| --- | --- | --- |
| Anno e numero | `anno_pronuncia`, `numero_pronuncia`; `ecli` = `ECLI:IT:COST:anno:numero` | Tutte; nessun doppione, nessun buco. L'anno è quello del deposito |
| Tipo di pronuncia | `tipologia_pronuncia` (S per sentenza, O per ordinanza) | Tutte |
| Tipo di giudizio | `tipologia_giudizio`, solo nell'archivio delle massime | Tutte tranne 8 |
| Data della decisione | `data_decisione` (gg/mm/aaaa) | 3 vuote; 17 depositi con una data precedente alla decisione (errori) |
| Data del deposito | `data_deposito` | Tutte; una sola non coerente con l'anno (69/1982) |
| Presidente | `presidente`, solo il cognome | Tutte |
| Relatore | `relatore_pronuncia`, nome e cognome | Quasi tutte, dal 1956 |
| Chi ha scritto (redattore) | Tre periodi diversi (vedi sotto) | — |
| Collegio | `collegio`, testo libero ("composta dai signori: …") | Tutte. Il formato cambia nel tempo; da 11 a 15 giudici; rari errori di trascrizione nei nomi più vecchi |
| Fatto e diritto delle sentenze | `<testo>`, con i marcatori `<fatto>` e `<diritto>` che contengono solo il titolo | 11.693 sentenze su 11.735 |
| Motivazione delle ordinanze | Dentro `<epigrafe>` ("Ritenuto che…", "Considerato che…"); `<testo>` è vuoto nel 96% dei casi | Con gli spazi uniformati, "Considerato che" compare nel 96% delle ordinanze (prima di uniformarli sembrava il 50%) |
| Dispositivo e firme | `dispositivo`, dopo "per questi motivi" | Tutte |
| Massime e materia | Archivio delle massime: `titolo` (voci separate da " - "), `testo`, `parametri`, `norme` | 46.658 massime; le materie scritte nei titoli andrebbero uniformate (5.363 prime voci diverse, tutte maiuscole fino al 2014); per questo la materia si ricava dai temi (relazione, sezione 2.7) |
| Giudici | Elenco ufficiale: nome, `Eletto_da`, date di nomina, giuramento e fine mandato, breve biografia | 125 giudici più 11 righe che uniscono più giudici; 33 date di fine mandato mancanti, un errore (Spagnoli: "2005" invece di 1995) |
| Data di pubblicazione in Gazzetta Ufficiale | Non c'è | — |

**Chi ha scritto la pronuncia: tre periodi.**

| Periodo | Che cosa registrano i dati | Che cosa si può dire |
| --- | --- | --- |
| Dal 1956 alla pronuncia 286/1986 | Solo il relatore (in un campo). Firmano tutti i giudici: chi ha scritto non è indicato da nessuna parte | Chi ha scritto non si conosce. Si usa il relatore al suo posto, che va bene se allora di regola scriveva il relatore: è da verificare, perché secondo gli studiosi le Norme integrative del 1956 non avevano una regola apposita |
| Dalla 287/1986 al 2001 | Il relatore nel campo; chi ha scritto solo nelle firme ("Il redattore: COGNOME"); il campo `redattore_pronuncia` è vuoto | Chi ha scritto si ricava dal testo; confrontando i due nomi si vedono i casi di relatore sostituito |
| Dal 2002 a oggi | Relatore e redattore nei campi; dal 2016 anche più redattori ("A - B") | Si legge direttamente. Nell'elenco dei giudici le coppie di redattori compaiono come righe a sé, da scartare |

## 6. Che cosa misura davvero il progetto

| Si potrebbe credere di misurare | In realtà si misura | Conseguenza |
| --- | --- | --- |
| L'influenza di un giudice | L'influenza delle pronunce che ha scritto, decise e approvate dal collegio | Nei risultati si scrive "pronunce redatte da X" |
| Chi ha scritto, in tutto il periodo | Prima del 23/12/1986 solo il relatore | Deciso l'8/11/2026: fino alla pronuncia 286/1986 il relatore prende il posto di chi ha scritto, e lo si dichiara; D2 e D3 si rifanno sulle sole pronunce dal 1987 come prova di controllo |
| Che chi scrive condividesse un precedente (D3) | Che sedesse nel collegio che lo ha deciso | D3 misura l'esposizione a un precedente, non l'adesione |
| Collegi quasi sempre completi | Il 70,4% delle pronunce ha meno di 15 giudici, e il 17,6% ne ha 11 o 12: in media ci sono 14,6 giudici in carica, 13,7 nel collegio e 0,9 assenti (`reports/d3_absences.json`) | Le assenze sono frequenti: rendono possibile il confronto di D3 tra presenti e assenti |
| La scelta personale di citare un precedente | Una scelta del collegio, scritta dal redattore con i suoi assistenti di studio | Le citazioni sono della Corte; chi scrive ne è il tramite |
| Relatori assegnati a caso | Il Presidente nomina i relatori, con criteri non pubblici | Se i relatori si specializzano per materia, in D2 e D3 bisogna tener conto della materia |
| La materia della pronuncia | La classificazione dell'Ufficio del massimario nei titoli delle massime | Va uniformata e dichiarata come tale. In alternativa: gli articoli della Costituzione invocati, presenti nell'86% delle massime (usati nelle prove della relazione, sezioni 3.4 e 3.5) |
| Una rete senza cicli | Pronunce depositate lo stesso giorno possono citarsi a vicenda | Le citazioni tra pronunce dello stesso giorno si tengono da parte |

## 7. Domande ancora aperte

- Il testo della modifica del 7 luglio 1987 sulle firme conferma che la pratica del dicembre 1986 l'ha preceduta?
- Prima del 1987 scriveva sempre il relatore? Con quale regola?
- Il Presidente sceglie i relatori per competenza nella materia? Ci sono studi sui suoi criteri?
- Quanto pesa davvero chi scrive sul testo e sulla scelta dei precedenti, e quanto gli assistenti di studio?
- Le citazioni tra pronunce dello stesso giorno vanno sempre dal numero più alto al più basso?
- Quali formule usano le ordinanze più vecchie al posto di "Considerato che"?

## 8. Il contesto per chi legge la relazione

Le sezioni 1, 2, 3 e 6 di questo documento (chi decide, chi scrive, che cosa registrano i dati e che cosa no) sono riassunte nella relazione: nei "Chiarimenti di base" della Parte I e nella sezione 1.3 della Parte II.
