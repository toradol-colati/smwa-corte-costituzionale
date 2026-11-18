# Il contesto: come nasce una pronuncia e cosa registrano i dati

> Documento di lavoro. Serve prima a noi, per sapere cosa stiamo misurando; poi diventa la base dell'introduzione della relazione. Ogni affermazione ha una fonte e uno stato. I numeri sui dati vengono da `src/ingest/inspect_raw.py` (report in `reports/data_inspection.md`), sui file scaricati l'8/11/2026 (`data/raw/MANIFEST.csv`).

**Stati.** *Fonte*: verificata leggendo la fonte indicata. *Dati*: verificata sui file del portale. *Da verificare*: non ancora controllata su una fonte primaria.

## Perché serve

Una pronuncia della Corte costituzionale non è l'opera di un giudice. La decide un collegio, a maggioranza, in camera di consiglio; poi un giudice ne scrive la motivazione e il collegio ne approva il testo. Chi legge i campi dei dati senza sapere questo misura altro da ciò che crede: per esempio attribuisce al redattore una decisione del collegio. In più, come mostra la sezione 5, i dati non registrano le stesse cose in tutti i periodi.

## Fonti

**Lette per questo documento**
- [Legge 11 marzo 1953, n. 87](https://www.cortecostituzionale.it/documenti/filesDoc/Legge_11_marzo_1953_n_87.pdf), testo coordinato sul sito della Corte: artt. 16–19.
- [Norme integrative per i giudizi davanti alla Corte costituzionale](https://www.cortecostituzionale.it/documenti/download/pdf/norme_integrative_2026.pdf), testo del 2021 aggiornato al 12 marzo 2026: artt. 9 e 20.
- [Norme integrative del 7 ottobre 2008](https://www.cortecostituzionale.it/documenti/download/pdf/CC_Fonti_NORME_INTEGRATIVE%20_05032011.pdf): artt. 7 e 17.
- Portale open data della Corte: [Il progetto](https://dati.cortecostituzionale.it/Il_progetto/Il_progetto) (composizione, funzioni, flusso di lavoro), [I DTD](https://dati.cortecostituzionale.it/Scarica_i_dati/I_dtd/I_dtd), [ECLI](https://dati.cortecostituzionale.it/ECLI/ECLI).
- [Annuario 2025 della Corte, I giudici e gli assistenti di studio](https://www.cortecostituzionale.it/annuario2025/giudici-e-assistenti-di-studio.html).
- A. Rauti, [Le nuove "norme integrative" della Corte](https://www.forumcostituzionale.it/wordpress/images/stories/pdf/documenti_forum/paper/0168_rauti.pdf), Forum di Quaderni costituzionali: storia della regola sulle firme e lettura della sostituzione del relatore.

**Raccolte nel browser il 10/11/2026**: l'elenco completo, con lo stato di lettura di ogni voce, è in `docs/sources.md`. Qui sono citate con la sua sigla (per esempio [C4]). Le più usate: Caravita 2021 [C4] e il forum del Gruppo di Pisa 2021 [C5] sulla sostituzione del relatore; la relazione di Saja sul 1987 [C1]; l'elenco ufficiale dei giudici [B4]; l'Annuario 2024 [C2].

**Trovate ma non ancora lette**
- [Legge costituzionale 22 novembre 1967, n. 2](https://www.normattiva.it/eli/id/1967/11/25/067C0002/ORIGINAL), che ha ridotto il mandato da 12 a 9 anni.
- Costituzione, artt. 134–137.
- Sul relatore sostituito e il dissenso: M. Di Martino, [L'opinione dissenziente](https://iris.uniroma1.it/retrieve/e383532c-1eea-15e8-e053-a505fe0a3de9/DiMartino_opinione-dissenziente_2021.pdf) (2021); la [recensione di Ciommo](https://www.nomos-leattualitaneldiritto.it/wp-content/uploads/2022/06/6.-RECENSIONE-DI-CIOMMO.pdf) su Nomos (2022), che riporta uno studio con 87 casi di sostituzione; D. Tega su Quaderni costituzionali (2020).
- Regolamento generale della Corte e regolamento per l'ufficio studi e gli assistenti di studio.

## 1. La Corte in breve

| Affermazione | Fonte | Stato | Cosa cambia per i dati |
| --- | --- | --- | --- |
| 15 giudici: 5 nominati dal Presidente della Repubblica, 5 eletti dal Parlamento in seduta comune, 5 dalle supreme magistrature (3 Cassazione, 1 Consiglio di Stato, 1 Corte dei conti) | Portale, Il progetto | Fonte | Nell'anagrafica `Eletto_da` ha queste cinque voci (sezione 5) |
| Mandato di 9 anni dal giuramento. Fino al 1967 era di 12 anni | Portale, Il progetto; legge cost. 2/1967 | Fonte (9 anni); Dati (12 anni prima del 1967) | I 26 giudici che hanno giurato prima del 1967 hanno un mandato mediano di 11,8 anni, contro 9 dopo: le opportunità di D2 cambiano tra i due periodi |
| Il Presidente è eletto dalla Corte tra i suoi componenti a scrutinio segreto, per 3 anni o fino alla scadenza del mandato; designa un vicepresidente; determina l'ordine dei lavori, nomina i relatori e ha voto decisivo in caso di parità | Portale, Il progetto; legge 87/1953 art. 16 | Fonte | Il presidente cambia spesso: 84 grafie distinte nel campo `presidente` |
| Funzioni: legittimità delle leggi statali e regionali; conflitti di attribuzione tra poteri e tra enti; ammissibilità dei referendum abrogativi; accuse contro il Presidente della Repubblica | Portale, Il progetto | Fonte | Il campo `tipologia_giudizio` delle massime le distingue (sezione 4) |
| Giudici scelti tra magistrati delle giurisdizioni superiori, professori ordinari di materie giuridiche, avvocati con vent'anni di esercizio | Cost. art. 135 | Da verificare | La professione è scritta nelle note biografiche dell'anagrafica: base per D4 |
| Nei giudizi d'accusa si aggiungono sedici giudici aggregati | Cost. art. 135 | Da verificare | Le 3 pronunce classificate come giudizio d'accusa (ordinanze del 1992 e 1996) hanno collegi di soli giudici costituzionali. La sentenza Lockheed del 2/8/1979, senza numero e in composizione integrata [B7], non è nell'archivio |

## 2. Chi fa cosa in una pronuncia

| Ruolo | Cosa fa | Cosa non significa | Fonte e stato |
| --- | --- | --- | --- |
| Collegio | Delibera in camera di consiglio. Ne fanno parte i giudici presenti all'udienza o alla camera di consiglio di trattazione; servono almeno 11 giudici. Il voto è palese dentro la camera di consiglio: vota per primo il relatore, poi gli altri dal meno anziano per nomina, per ultimo il Presidente. Decide la maggioranza assoluta dei votanti; a parità prevale il voto del Presidente | Farne parte non vuol dire aver votato a favore: i voti non sono pubblicati e la Corte non pubblica opinioni dissenzienti | Fonte: legge 87/1953 art. 16; Norme integrative 2026 art. 20 |
| Presidente | Nomina uno o più giudici per l'istruzione e la relazione; dirige la discussione; affida la redazione a un giudice diverso dal relatore quando serve; firma | Non è l'autore della pronuncia | Fonte: Norme integrative 2026 artt. 9 e 20 |
| Relatore | Istruisce la causa e la riferisce al collegio; vota per primo | Non è detto che scriva la pronuncia, né che sia d'accordo con la decisione | Fonte: Norme integrative 2026 artt. 9 e 20 |
| Redattore | Scrive la sentenza o l'ordinanza dopo la votazione. Di regola è il relatore; il Presidente può affidare la redazione "ad altro o a più giudici" per indisponibilità o per altro motivo. Nei giudici comuni la stessa funzione si chiama giudice estensore | Non è chi decide: il testo è approvato dal collegio | Fonte: Norme integrative 2026 art. 20, commi 4–5 |
| Assistenti di studio | Vengono dalle magistrature o dalle università; aiutano i giudici nell'istruttoria e nella redazione delle pronunce | Non firmano: il loro contributo non compare nei dati | Fonte: Annuario 2025 |
| Cancelliere | Firma la pronuncia e ne riceve il deposito | — | Fonte: legge 87/1953 artt. 18–19 |
| Ufficio del massimario | Compila le massime e cura la raccolta ufficiale (il portale open data le attribuisce al Servizio studi, che fa analisi e documentazione) | Non sono giudici: materie e titoli delle massime sono una classificazione d'ufficio | Fonte: Annuario 2024 [C2]; portale, Il progetto |

**Le firme sono cambiate nel tempo.**
- La legge 87/1953 (art. 18) chiede ancora oggi la sottoscrizione "dei giudici e del cancelliere".
- Le Norme integrative dicono invece che firmano il Presidente e il giudice redattore. Rauti data questa regola a una modifica del 1987; la legge non è mai stata adeguata.
- Nei dati il passaggio è netto ma cade prima, a dicembre 1986:
  - fino alla pronuncia 286/1986 firmano tutti i giudici del collegio e il redattore non compare da nessuna parte;
  - dalla 287/1986, depositata il 23/12/1986, firmano il Presidente e il redattore.
- Caravita [C4, pp. 3–4] data la regola a una modifica delle Norme integrative del 7 luglio 1987, decisa durante lo smaltimento dell'arretrato. La prassi l'ha quindi preceduta di qualche mese. Il testo della deliberazione non è ancora stato letto.

**Relatore diverso dal redattore.**
- Con la firma del solo redattore, la sostituzione del relatore è diventata visibile.
- La dottrina la legge spesso come traccia di un dissenso del relatore, rimasto in minoranza, ma non è sempre così: la sostituzione può avvenire anche per indisponibilità (Rauti). Talvolta la pronuncia lo dichiara, come la sentenza 393/2006: "il Giudice relatore Giovanni Maria Flick, sostituito per la redazione della sentenza dal Giudice Alfonso Quaranta".
- Nei dati, dove i due campi sono compilati (8.384 pronunce, quasi tutte dal 2002), il redattore è diverso dal relatore in 93 casi.
- Dal 2016 ci sono 17 pronunce con più redattori; il relatore indicato è lo stesso gruppo di giudici, quindi non sono tra i 93 casi.
- **Il confronto regge.** Dal 2003 al 2020 i dati danno 44 casi su 6.340 pronunce; Panizza [C5] ne conta 41 su circa 6.350 nello stesso periodo.
- Dalla fine del 2006 l'epigrafe può dichiarare la sostituzione ("sostituito per la redazione"): nei dati succede in 41 pronunce dal 2006 al 2023, meno dei casi con i campi diversi. La formula conferma, ma non conta tutti i casi.
- Nel 1987–1989, gli anni dello smaltimento dell'arretrato, ogni processo era affidato a due giudici [C1]: lì relatore e redattore differiscono molto più spesso, e Caravita esclude questi anni dal conteggio delle sostituzioni [C5].

**La decisione ha due fasi.** Prima si vota la decisione, poi il collegio approva il testo scritto dal redattore.
- La data della decisione è quella della votazione (Norme integrative 2026, art. 20, comma 6).
- Prima dell'approvazione del testo, la deliberazione si può cambiare solo con il consenso unanime dei giudici che l'hanno presa (art. 20, comma 3).
- Secondo la dottrina citata da Rauti, in passato la Corte è tornata talvolta sulla prima decisione mentre il testo veniva scritto.

## 3. La vita di una pronuncia

1. **Atto che apre il giudizio**, iscritto in un registro della cancelleria (fonte: portale, Il progetto). I registri sono:
   - ordinanze di rimessione dei giudici comuni (R.O.);
   - ricorsi (R.R.);
   - conflitti tra poteri (R.C.P.);
   - conflitti tra enti (R.C.E.);
   - ammissibilità dei referendum (AM.REF.).

   Per questo nei testi "ordinanza n. X del AAAA" può indicare un atto del registro e non una pronuncia della Corte.
2. **Nomina del relatore** da parte del Presidente, e decreto che fissa l'udienza pubblica o la camera di consiglio (fonte: Norme integrative, art. 9; portale).
3. **Deliberazione** in camera di consiglio: è la data della decisione (fonte: Norme integrative, art. 20).
4. **Redazione** e approvazione del testo da parte del collegio (fonte: Norme integrative, art. 20).
5. **Deposito** in cancelleria: da qui chiunque può vedere la decisione (fonte: legge 87/1953, art. 19). Sui dati:
   - il numero della pronuncia segue l'ordine del deposito: 22 inversioni rispetto alla data di deposito, 1.134 rispetto alla data della decisione;
   - l'anno è quello del deposito in tutti i casi tranne un errore di data;
   - 220 pronunce sono decise a fine anno e numerate nell'anno dopo;
   - tra decisione e deposito passano 9 giorni in mediana.
6. **Pubblicazione** in Gazzetta Ufficiale, prima serie speciale (fonte: portale). La data di pubblicazione non è nei file.
7. **Massimazione** da parte dell'Ufficio del massimario. Nel 2026 il 73% delle pronunce ha già le massime; negli anni fino al 2025 tutte.

**Risposte alle domande della prima versione di questo documento**
- **Anno e numero:** si assegnano al deposito, non alla decisione (Dati). Il portale scrive che nell'ECLI c'è l'"anno decisione", ma nei file l'anno è sempre quello del deposito.
- **Quale data ordina le pronunce:** il deposito. È la data da cui una pronuncia esiste per chi la cita, e quella che segue la numerazione (Fonte e Dati). Proposta da confermare in `docs/decisions.md`.
- **Citazioni nello stesso giorno:** esistono. Una sonda grezza sulle citazioni trova 145 menzioni verso pronunce depositate lo stesso giorno, e 328 pronunce contengono l'espressione "in pari data". Esempio: la pronuncia 135/1970 cita l'ordinanza 134/1970, depositata lo stesso giorno (Dati). Non sono errori di estrazione.

## 4. Tipi di pronuncia, di giudizio e di esito

- **Pronuncia** (fonte: legge 87/1953, art. 18):
  - la sentenza giudica in via definitiva;
  - l'ordinanza è "succintamente motivata";
  - il decreto è un atto del Presidente.

  Nei file ci sono solo sentenze (11.735) e ordinanze (10.692), nessun decreto (Dati).
- **Giudizio**: il campo `tipologia_giudizio` delle massime c'è per tutte le pronunce tranne 8 (Dati):
  - in via incidentale: 17.052;
  - in via principale: 3.234;
  - conflitto tra enti: 1.026;
  - ammissibilità del conflitto tra poteri: 480;
  - conflitto tra poteri: 305;
  - ammissibilità del referendum: 153;
  - correzione di errori materiali: 140;
  - casi misti e residui.

  La categoria "correzione di errori materiali" serve direttamente alla variante di robustezza senza le ordinanze di correzione.
- **Esito**: non è un campo. Va letto nel dispositivo ("dichiara l'illegittimità…", "dichiara non fondata…", "dichiara la manifesta inammissibilità…", "ordina la restituzione degli atti…"). Da verificare quanto sia regolare la formula nei diversi decenni.

## 5. Dal concetto al campo

| Concetto | Dove sta nei file | Copertura e avvertenze (Dati) |
| --- | --- | --- |
| Anno e numero | `anno_pronuncia`, `numero_pronuncia`; `ecli` = `ECLI:IT:COST:anno:numero` | Tutte; nessun duplicato, nessun buco. L'anno è quello del deposito |
| Tipo di pronuncia | `tipologia_pronuncia` (S, O) | Tutte |
| Tipo di giudizio | `tipologia_giudizio`, solo nell'archivio delle massime | Tutte tranne 8 |
| Data della decisione | `data_decisione` (gg/mm/aaaa) | 3 vuote; 17 depositi precedenti alla decisione (errori) |
| Data del deposito | `data_deposito` | Tutte; una sola incoerente con l'anno (69/1982) |
| Presidente | `presidente`, solo cognome | Tutte |
| Relatore | `relatore_pronuncia`, nome e cognome | Quasi tutte, dal 1956 |
| Redattore | Tre periodi diversi (vedi sotto) | — |
| Collegio | `collegio`, testo libero ("composta dai signori: …") | Tutte. Formato cambiato nel tempo; da 11 a 15 giudici; rari errori di trascrizione nei nomi più vecchi |
| Fatto e diritto delle sentenze | `<testo>`, con i marcatori `<fatto>` e `<diritto>` che contengono solo il titolo | 11.693 sentenze su 11.735 |
| Motivazione delle ordinanze | dentro `<epigrafe>` ("Ritenuto che…", "Considerato che…"); `<testo>` è vuoto nel 96% dei casi | "Considerato che" compare nel 50% delle epigrafi: le altre formule vanno censite |
| Dispositivo e firme | `dispositivo`, dopo "per questi motivi" | Tutte |
| Massime e materia | archivio delle massime: `titolo` (voci separate da " - "), `testo`, `parametri`, `norme` | 46.658 massime; materia da normalizzare (5.363 prime voci distinte, formato maiuscolo fino al 2014) |
| Giudici | anagrafica: nome, `Eletto_da`, date di nomina, giuramento e cessazione, nota biografica | 125 giudici più 11 righe composte; 33 date di cessazione mancanti, un errore (Spagnoli, cessazione "2005" anziché 1995) |
| Data di pubblicazione in Gazzetta Ufficiale | non c'è | — |

**Il redattore: tre periodi.**

| Periodo | Cosa registrano i dati | Cosa possiamo dire |
| --- | --- | --- |
| 1956 – pronuncia 286/1986 | Solo il relatore (campo). Firmano tutti i giudici: il redattore non è scritto da nessuna parte | Il redattore non si osserva. Il relatore è l'approssimazione disponibile, se in quel periodo la redazione spettava di regola al relatore: da verificare, perché secondo la dottrina la regola specifica non c'era nelle Norme integrative del 1956 |
| 287/1986 – 2001 | Relatore nel campo; redattore solo nelle firme ("Il redattore: COGNOME"); campo `redattore_pronuncia` vuoto | Il redattore si estrae dal testo; i casi di relatore sostituito si vedono confrontando i due |
| 2002 – oggi | Relatore e redattore nei campi; dal 2016 anche più redattori ("A - B") | Diretto. Nell'anagrafica le coppie di redattori compaiono come righe a sé, da scartare |

## 6. Cosa misura davvero il progetto

| Si potrebbe credere di misurare | Si misura in realtà | Conseguenza |
| --- | --- | --- |
| L'influenza di un giudice | L'influenza delle pronunce di cui è stato redattore, decise e approvate dal collegio | Nei risultati si scrive "pronunce redatte da X" |
| Il redattore in tutto il periodo | Prima del 23/12/1986 solo il relatore | Deciso l'8/11/2026: nell'analisi principale il relatore approssima il redattore fino alla pronuncia 286/1986, dichiarandolo; D2 e D3 si rifanno sulle sole pronunce dal 1987 come variante di controllo |
| Che il redattore condividesse un precedente (D3) | Che sedesse nel collegio che lo ha deciso | D3 misura l'esposizione a un precedente, non l'adesione |
| Assenze rare dal collegio | Collegi con 11 o 12 giudici nel 17,6% delle pronunce | Le assenze sono frequenti: sono una fonte di variazione utile per identificare D3. Per distinguere un'assenza da un seggio vacante servono date di mandato complete |
| La scelta personale di citare un precedente | Una scelta del collegio, scritta dal redattore con i suoi assistenti di studio | Le citazioni sono della Corte; il redattore ne è il tramite |
| Redattori assegnati a caso | Il Presidente nomina i relatori, con criteri non pubblici | Se i relatori si specializzano per materia, la materia va controllata in D2 e D3 |
| La materia della pronuncia | La classificazione dell'Ufficio del massimario nei titoli delle massime | Da normalizzare e da dichiarare come tale. Alternativa: i parametri costituzionali, presenti nell'86% delle massime |
| Un grafo senza cicli | Pronunce depositate lo stesso giorno possono citarsi | Le citazioni tra pronunce dello stesso giorno si tengono a parte |

## 7. Domande ancora aperte

- Il testo della deliberazione del 7 luglio 1987 sulle firme: conferma che la prassi del dicembre 1986 l'ha preceduta?
- Prima del 1987 la redazione spettava sempre al relatore? Con quale regola?
- Il relatore viene scelto per competenza nella materia? Ci sono studi sui criteri del Presidente?
- Quanto pesa davvero il redattore sul testo e sulla scelta dei precedenti, e quanto gli assistenti di studio?
- Le citazioni tra pronunce dello stesso giorno vanno sempre dal numero più alto al più basso?
- Quali formule usano le ordinanze più vecchie al posto di "Considerato che"?

## 8. Introduzione per il lettore

Da scrivere alla fine di questa fase, partendo dalle sezioni 1, 2, 3 e 6: chi decide, chi scrive, cosa registrano i dati e cosa no.
