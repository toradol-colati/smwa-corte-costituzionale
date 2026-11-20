# Fonti del progetto

Raccolte e controllate il 10/11/2026 da Claude nel browser; riviste lo stesso giorno da Claude Code, che ha confrontato le deduzioni con i dati (sezione 0). Per ogni voce: riferimento, link, cosa contiene (solo quello che è stato controllato), uso nel progetto, stato della verifica.

**Stati.** *Letto*: testo o pagine indicate letti. *Abstract*: riferimento e abstract controllati, non il testo. *Scheda*: controllato solo che il riferimento esista; il contenuto viene da titolo o scheda. *[da verificare]*: non controllato.

**Sigle.** C = contesto istituzionale, B = base dati, L = letteratura e metodo.

**Regola.** Nella relazione si cita solo ciò che è stato letto, con le pagine. Le voci "abstract" o "scheda" si leggono prima di citarle. Non si citano tutte: il riferimento è il nucleo minimo qui sotto.

## Nucleo minimo per la relazione

| Ruolo | Fonte | Stato | Da fare |
| --- | --- | --- | --- |
| Contesto | Legge 87/1953, artt. 16–19, 23 e 27 | Letto (artt. 23 e 27 il 18/11/2026) | — |
| Contesto | Norme integrative 2008 (artt. 7, 17) e 2026 (artt. 9, 20) | Letto | — |
| Contesto | [B4] Pagina ufficiale "I Giudici costituzionali" | Letto | — |
| Contesto | [C4] Caravita 2021, estratto gratuito | Letto (pp. 2–8) | — |
| Contesto | [C5] Forum del Gruppo di Pisa 2021 | Letto (pagine indicate) | — |
| Dati | [B1] Portale open data della Corte | Letto | — |
| Dati | [B5] Dati quantitativi 2025 del Servizio studi | Letto | Confrontare i conteggi per tipo di giudizio |
| Lavori sulla Corte italiana | [L3] Agnoloni e Pagallo 2016 | Letto (pp. 139–151) | — |
| Lavori sulla Corte italiana | [L1–L2] Agnoloni e Pagallo 2015 | Abstract | Testo a pagamento (ACM, IOS Press): serve l'accesso della biblioteca |
| D1 | [L4] Lupu e Voeten 2012 | Letto (pp. 413–437) | — |
| D1 | [L11] Fowler et al. 2007 | Letto, manoscritto degli autori (pp. 1–18 del manoscritto) | Per citare le pagine della rivista serve la versione pubblicata |
| D1 | [L7] Frankenreiter 2017, risposta a Derlén e Lindholm | Letto per intero (pp. 687–694) | — |
| D2–D4 | [L16] Landes, Lessig e Solimine 1998 | Letto (pp. 271–293, 321–327) | — |
| D2–D4 | [L19] Frankenreiter 2017, Corte di giustizia UE | Letto, versione accettata (pp. 1–26 del manoscritto) | Per citare le pagine della rivista serve la versione pubblicata |
| Metodo | [L21] Uzzi et al. 2013, nullo che rispetta il tempo | Letto (materiali supplementari, pp. 3, 5) | — |
| Metodo | [L24] King e Zeng 2001, campionamento in D3 | Letto (pp. 140–144, 160) | — |
| Metodo | [L15] Black e Spriggs 2013, D1b | Abstract | Nessuna versione libera: cercare "10.1111/jels.12012" nel catalogo della biblioteca (Wiley Online Library) |
| Corso | [L27] Easley e Kleinberg, cap. 5, 14, 20 | Letti §14.5 (18/11/2026), cap. 5 e cap. 20 (20/11/2026); indice completo letto il 18/11/2026 | Per citare altri capitoli vanno letti |
| Corso | [L28] Barabási, *Network Science* | Indice dei capitoli 1–10 (titoli delle sezioni) letto il 18/11/2026; cap. 3, §3.8–3.10, letto il 20/11/2026 | Altre parti non lette: vanno lette prima di citarle |

Da leggere: L1–L2 (ACM, IOS Press) e L15 (Wiley), non ancora caricati. I PDF letti sono in `literature/`, esclusa da git. Il file caricato come Fowler et al. 2007 era un altro articolo (H. J. Fowler e altri, *International Journal of Climatology*, 2007): rinominato `WRONG_…`; al suo posto c'è il manoscritto degli autori dell'articolo giusto.

## 0. Cosa cambia nel progetto, con le verifiche sui dati

1. **Chi scrive le massime.** L'Annuario 2024 [C2] attribuisce la compilazione delle massime all'Ufficio del massimario; il Servizio studi fa analisi e documentazione. La pagina "Il progetto" del portale open data scrive invece "massime redatte dal Servizio studi". Si cita l'Annuario, più recente, segnalando la differenza.
2. **Fonte per completare l'anagrafica.** La pagina ufficiale "I Giudici costituzionali" [B4] riporta per ogni giudice dal 1956 provenienza, nomina o elezione, giuramento e cessazione. Conferma la cessazione di Spagnoli il 25/02/1995, non il 2005. Omonimi, con i periodi:
   - Aldo Sandulli (1957–1969) e Maria Alessandra Sandulli;
   - Nicola Reale (1968–1977) e Oronzo Reale (1977–1986);
   - Ettore Gallo (1982–1991) e Franco Gallo (2004–2013);
   - Annibale Marini (1997–2006) e Francesco Saverio Marini.

   M. A. Sandulli e F. S. Marini hanno giurato il 19/02/2025 [B5]; l'anagrafica scaricata indica il 18/02/2025 [da verificare].
3. **Firma del solo Presidente e redattore.** Caravita [C4, p. 3]: le Norme integrative del 1956 prevedevano la firma di tutti i giudici; la modifica del 7 luglio 1987 all'art. 18 introduce la firma del Presidente e del redattore, decisa durante lo smaltimento dell'arretrato (p. 4). Nei dati il passaggio cade il 23/12/1986 (pronuncia 287/1986): la prassi ha preceduto la norma. Il testo della deliberazione non è stato letto [da verificare].
4. **Relatore sostituito.**
   - **Il confronto tra i campi regge.** Dal 2003 al 2020 i nostri dati danno 44 pronunce con relatore diverso dal redattore su 6.340; Panizza [C5, pp. 397–398] conta 41 casi su circa 6.350 nello stesso periodo.
   - **Il report ipotizzava che le 17 pronunce con più redattori fossero contate tra le "diverse": è falso.** Nei dati il campo relatore contiene gli stessi nomi del campo redattore, quindi nessuna delle 17 è tra i 93 casi.
   - **Formula di sostituzione nel testo** ("sostituito per la redazione", "che viene sostituito"): nei dati compare dal 2006, come scrive Caravita [C4, p. 2], in 41 pronunce dal 2006 al 2023. Sono meno dei casi con i campi diversi: la formula non è sempre usata. Va letta come conferma, non come conteggio.
   - **1987–2001.** Un confronto grezzo tra il campo relatore e il redattore nelle firme dà 475 differenze, di cui 124 nel 1988 e 56 nel 1989. Molte sono errori di grafia nel campo relatore ("Caianello" per Caianiello); il resto è compatibile con l'arretrato, quando ogni processo era affidato a due giudici [C1, p. 5]. Caravita conta 32 sostituzioni ufficiali nel 1988–1999. Il numero vero si saprà solo con l'abbinamento dei nomi all'anagrafica.
   - Una sostituzione è un indizio di dissenso, non una prova [C5, Ruotolo]; il relatore in minoranza spesso redige comunque [C7, pp. 14–15].
5. **Gli anni dell'arretrato** (1987–1989 circa). Nel 1987 ogni processo fu affidato a due giudici, i pendenti divisi in sei gruppi per materia, e le decisioni più che raddoppiarono [C1, p. 5]: nei dati 641 pronunce nel 1987 e 1.165 nel 1988, contro 300–400 negli anni prima. Caravita esclude questi anni dal calcolo delle sostituzioni [C5]. Da decidere: una variante di robustezza senza gli anni dell'arretrato, con gli anni fissati sulle fonti.
6. **Collegio integrato del giudizio Lockheed.** Sentenza senza numero, depositata il 2/8/1979, con giudici aggregati [B7]. **Non è nell'archivio scaricato**: il 1979 va dalla 1 alla 155 e nessun collegio menziona giudici aggregati. Va solo dichiarata come assente.
7. **Ammissibilità e forma.** Il programma 2026/27 [L29] chiede un'analisi originale con metodi del corso, individuale o in coppia, 70% del voto; non pone vincoli su tema o dati. Il corso è in inglese, quindi probabilmente anche la relazione [da chiedere]. Argomento per il docente: Easley e Kleinberg, §14.5 "Applications beyond the Web", pp. 415–417 [L27], presenta l'analisi hub/authority di Fowler e Jeon sulle sentenze della Corte Suprema USA.
8. **La lacuna va ristretta.** L'influenza dei singoli giudici misurata con le citazioni è studiata da tempo [L16–L18], anche in una corte con giudice relatore e senza dissenso pubblicato, la Corte di giustizia UE [L19]. La novità difendibile è più stretta: gli strati di redazione e collegio applicati alla Corte costituzionale italiana, e la memoria collegiale stimata sulle assenze dal collegio (D3).
9. **D1: una legge di potenza non prova una gerarchia.** Agnoloni e Pagallo riportano leggi di potenza [L2]; Frankenreiter [L7] osserva che le producono anche pratiche di citazione ripetitive, e che servono test formali. Sostiene la regola "un modello nullo per ogni statistica". Per stimare le distribuzioni: [L22]; per confrontare precedenti di età diverse: [L13].
10. **D3: campionare i non citati.** King e Zeng [L24]: campionare tutti gli eventi e una frazione dei non eventi è efficiente; le correzioni sono nel testo, da leggere prima di scegliere tra 50 e 100.
11. **D1b: durata del precedente.** Black e Spriggs [L15] definiscono il deprezzamento come variazione della frequenza di citazione con l'età, e trovano che l'effetto delle altre variabili dipende dall'età: l'età va nel modello, anche in interazione.
12. **Conteggi ufficiali per validare.** Il Servizio studi pubblica i "Dati quantitativi e di analisi" [B5, B6]. Per il 2025: 219 decisioni (190 sentenze, 29 ordinanze); i nostri dati danno 219 pronunce nel 2025 [conteggio di tipo e giudizio da confrontare].

## 1. Contesto istituzionale

**Fonti della Corte**
- [C1] Saja, F. (1988). *La giustizia costituzionale nel 1987*. Relazione alla conferenza stampa, 8/2/1988. [PDF](https://giurcost.org/contents/giurcost//cronache/19880208_Saja.pdf). Modifiche alle Norme integrative del 1° ottobre 1987; ogni processo affidato a due giudici; sei gruppi di lavoro per materia (p. 5); decisi quasi tutti i ricorsi in via principale e i conflitti pendenti fino al 1986 (p. 24). Uso: anni dell'arretrato. *Letto (pp. 5, 6, 24).*
- [C2] Corte costituzionale, Annuario 2024, "L'Istituzione e i suoi uffici". [pagina](https://cortecostituzionale.it/annuario2024/istituzione-e-uffici.html). Ufficio del massimario: compila le massime; Servizio studi: analisi e documentazione. *Letto.*
- [C3] Legge costituzionale 22 novembre 1967, n. 2. [Normattiva](https://www.normattiva.it/eli/id/1967/11/25/067C0002/ORIGINAL). Uso: durata del mandato. *Non letto [da verificare].*

**Relatore, redattore e dissenso**
- [C4] Caravita, B. (2021). *Ai margini della dissenting opinion. Lo "strano caso" della sostituzione del relatore nel giudizio costituzionale*. Giappichelli. [estratto](https://www.giappichelli.it/media/catalog/product/excerpt/9788892138216.pdf). Formula di sostituzione in epigrafe dalla fine del 2006 (p. 2); firma di tutti i giudici nel 1956 e modifica del 7/7/1987 (p. 3); limitazione decisa durante l'arretrato (p. 4); Norme 2008, art. 17, prima un "gentlemen's agreement" (pp. 5–6); 87 casi ufficiali dal 1988, contati dall'autore (p. 7); 53 giudici coinvolti (p. 8). *Letto (estratto, pp. 2–8).*
- [C5] Forum "Sull'introduzione dell'opinione dissenziente nel giudizio di costituzionalità", *Rivista del Gruppo di Pisa*, 1/2021. [PDF](https://iris.uniroma1.it/retrieve/e383532c-1eea-15e8-e053-a505fe0a3de9/DiMartino_opinione-dissenziente_2021.pdf). Caravita, pp. 386–389: 87 casi 1988–2020, 75 su 12.930 escludendo l'arretrato (0,6%); Marcenò, pp. 394–395: la sostituzione è l'unico modo in cui il dissenso traspare; Panizza, pp. 397–398: 41 casi 2003–2020 su circa 6.350, per tipo di giudizio; Ruotolo, pp. 404–405: indizio, non prova. *Letto (pagine indicate).*
- [C6] Di Ciommo, I. P. (2022). Recensione a Caravita 2021. *Nomos*, 1-2022. [PDF](https://www.nomos-leattualitaneldiritto.it/wp-content/uploads/2022/06/6.-RECENSIONE-DI-CIOMMO.pdf). Cita la norma come "art. 20, comma 4": è la numerazione delle Norme del 2021, mentre nel 2008 era l'art. 17 (verificato da Claude Code sui due testi). *Letto.*
- [C7] Pesole, L. (2022). "Riflettendo sulla recente riproposizione della questione dell'opinione dissenziente". *Costituzionalismo.it*, 2/2022. [PDF](https://costituzionalismo.it/wp-content/uploads/2-2022-1.-Pesole.pdf). Relatore diverso dal redattore come segno che il voto del relatore non è prevalso (p. 13); il relatore spesso redige comunque (pp. 14–15); discussione del 2002 sul dissenso (p. 25). *Letto (pagine indicate).*

**Il precedente nella giurisprudenza costituzionale**
- [C8] Treves, G. (a cura di) (1971). *La dottrina del precedente nella giurisprudenza della Corte costituzionale*. Torino. [SBN](https://www.sardegnacultura.it/en/search/IT%5CICCU%5CSBL%5C0371552). *Scheda; editore [da verificare].*
- [C9] MacCormick, N., Summers, R. S. (a cura di) (1997). *Interpreting Precedents: A Comparative Study*. Ashgate. [editore](https://www.routledge.com/Interpreting-Precedents-A-Comparative-Study/MacCormick-Summers/p/book/9781138270244). *Scheda; capitolo sull'Italia [da verificare].*
- [C10] Tega, D. (2020). *La Corte nel contesto*. Bononia University Press. DOI 10.30682/sg304. [PDF](https://cris.unibo.it/retrieve/e1dcb335-e087-7715-e053-1705fe0a6cc9/%5bd%5d%202020%20-%20La%20Corte%20nel%20contesto%20TEGA%20-%20Interno.pdf). "Ri-accentramento" dal 2011, più chiaro dal 2014 (pp. 11, 24); catene di autocitazione, per esempio 221/2015 ripresa da 262/2015 e 45, 95, 204/2016 (p. 36). Uso: possibile rottura temporale in D1; esempi per l'estrattore. *Letto in parte.*

**Studi empirici sulla Corte e sui suoi giudici**
- [C11] Pederzoli, P. (2008). *La Corte costituzionale*. Il Mulino. [scheda](https://cris.unibo.it/handle/11585/63174). Profili e carriere dei giudici. Uso: D4. *Abstract.*
- [C12] Barsotti, V., Carozza, P. G., Cartabia, M., Simoncini, A. (2015). *Italian Constitutional Justice in Global Context*. OUP. [scheda](https://scholarship.law.nd.edu/law_books/253). Uso: riferimento in inglese. *Scheda.*
- [C13] Breton, A., Fraschini, A. (2003). "The Independence of the Italian Constitutional Court". *Constitutional Political Economy*, 14(4), 319–333. [Springer](https://link.springer.com/article/10.1023/B:COPE.0000003861.45073.45). *Scheda.*
- [C14] Fiorino, N., Padovano, F., Sgarra, G. (2007). "The Determinants of Judiciary Independence: Evidence from the Italian Constitutional Court (1956–2002)". *JITE*, 163(4), 683–705. [RePEc](https://ideas.repec.org/a/mhr/jinste/urnsici0932-4569(200712)1634_683tdojie_2.0.tx_2-k.html). Provenienza dalla magistratura ed età associate a una Corte più indipendente. Uso: D4. *Abstract.*
- [C15] Dalla Pellegrina, L., Garoupa, N. (2013). "Choosing between the government and the regions". *European Journal of Political Research*, 52, 558–580. [scheda](https://scholarship.law.tamu.edu/facscholar/636). Uso: come altri legano le decisioni ai giudici senza dissenso pubblicato. *Scheda [da leggere].*
- [C16] Garoupa, N., Grembi, V. (2015). "Judicial Review and Political Partisanship". *International Review of Law and Economics*, 43, 32–45. [scheda](https://research.cbs.dk/en/publications/judicial-review-and-political-partisanship-moving-from-consensual/). 972 giudizi in via principale, 1985–2005. Uso: D4. *Abstract.*

## 2. I dati

- [B1] Corte costituzionale, pagina "Open data". [pagina](https://www.cortecostituzionale.it/contenuti/rapporti-cittadini/open-data). Quattro archivi, formati XML, JSON e CSV; "circa 18.000" pronunce, dato non aggiornato. *Letto.* Licenza (CC BY-SA 3.0) e schema verificati da Claude Code sul portale dati.cortecostituzionale.it l'8/11.
- [B2] Aliprandi, S. (2014). "Italian Constitutional Court opendata". Blog. [post](https://openisfree.blogspot.com/2014/01/italian-constitutional-court-opendata.html). Storia del portale; non istituzionale. *Letto.*
- [B3] Ordinanza n. 436/1993, versione di stampa. [pagina](https://www.cortecostituzionale.it/stampa-pdf-pronuncia/1993/436). Campo redattore vuoto, firma "Il redattore: VASSALLI"; collegio di 12. *Letto.*
- [B4] Corte costituzionale, "I Giudici costituzionali". [pagina](https://www.cortecostituzionale.it/contenuti/composizione/giudici-costituzionali). Provenienza, nomina o elezione, giuramento, cessazione per ogni giudice; Nicola Reale prorogato nel collegio Lockheed fino al 2/8/1979. Uso: completare l'anagrafica, D4. *Letto.*
- [B5] Servizio studi (R. Nevola, G. Verrengia, a cura di) (2026). *Dati quantitativi e di analisi della giurisprudenza costituzionale 2025*. [PDF](https://www.cortecostituzionale.it/annuario2025/pdf/Dati_quantitativi_e_di_analisi_giurisprudenza_costituzionale_2025.pdf). 219 decisioni per tipo di giudizio (pp. 5–6); collegio di 11 giudici al 1° gennaio 2025 (pp. 19–20); serie dal 2011. *Letto.*
- [B6] Stessa serie: [2024](https://giurcost.org/contents/giurcost//cronache/Dati_quantitativi_e_di_analisi_2024.pdf), [2018](https://www.cortecostituzionale.it/documenti/composizione/risorsePaginaPresidenteLattanzi/relazione2018/dati_quantitativi_analisi.pdf), [statistiche 2013](https://www.cortecostituzionale.it/documenti/relazioni_annuali/stat2013.pdf). *Non aperti.*
- [B7] Sentenza del giudizio d'accusa Lockheed, 2/8/1979. [giurcost](https://giurcost.org/decisioni/1979/0000s-79.html). Senza numero, composizione integrata. Non è nell'archivio scaricato. *Metadati letti.*
- [B8] Agnoloni, T., et al. (2017). "Linking European Case Law: BO-ECLI Parser". In *Legal Knowledge and Information Systems*, IOS Press, 113–118. DOI 10.3233/978-1-61499-838-9-113. [PDF](https://iris.unito.it/retrieve/e27ce42d-9a04-2581-e053-d805fe0acbaa/FAIA302-0113.pdf). Estrattore open source di riferimenti giurisprudenziali, con estensione italiana; non riporta precisione né richiamo. Uso: secondo estrattore da confrontare, non sostituisce le coppie annotate. *Letto; funzionamento sul testo italiano [da verificare provandolo].*
- [B9] Bacci, L., et al. (2019). "Linkoln project at the Italian Senate". IOS Press, 149–158. [scheda](https://iris.cnr.it/handle/20.500.14243/426219). Estrattore di riferimenti normativi. *Abstract.*

## 3. Lavori precedenti e metodo

**La rete della Corte costituzionale italiana**
- [L1] Agnoloni, T., Pagallo, U. (2015). "The case law of the Italian constitutional court, its power laws, and the web of scholarly opinions". *ICAIL 2015*, 151–155. DOI 10.1145/2746090.2746108. [scheda](https://iris.unito.it/handle/2318/1728348). *Abstract.*
- [L2] Agnoloni, T., Pagallo, U. (2015). "The power laws of the Italian Constitutional Court, and their relevance for legal scholars". IOS Press (JURIX 2015 [da verificare]). DOI 10.3233/978-1-61499-609-5-1. [scheda](https://iris.cnr.it/handle/20.500.14243/357030). *Abstract.*
- [L3] Agnoloni, T., Pagallo, U. (2016). "The Case Law of the Italian Constitutional Court between Network Theory and Philosophy of Information". *Informatica e diritto*, XLII annata, vol. XXV, n. 1, pp. 139–151. [testo](http://www.ittig.cnr.it/EditoriaServizi/AttivitaEditoriale/InformaticaEDiritto/IeD_2016_01_AgnoloniPagallo.pdf). Il titolo è in inglese; l'indice IRIS lo riporta in italiano. *Letto per intero, 10/11/2026.*
  - Dati: gli open data XML della Corte, rilasciati nel 2013, con 19.312 pronunce (tab. 2, p. 142), di cui il 78,6% in via incidentale.
  - Estrazione: il parser *Prudence*, adattato alla giurisprudenza costituzionale (p. 140). Validato su 60 pronunce distribuite nel tempo, con 1.294 riferimenti annotati a mano: precisione 98,4%, richiamo 91,7% (tab. 1, p. 141). Unità di misura: il singolo riferimento, non la coppia di pronunce; nessuna stratificazione per decennio o per tipo dichiarata.
  - Rete: solo le pronunce in via incidentale, 16.320 nodi e 41.858 archi (tab. 4, p. 142). Per le misure di importanza tolgono le ordinanze (p. 143).
  - Distribuzione dei gradi: legge di potenza con α = 2,414, adattata sulla scala log-log, da cui deducono che la rete "suggerisce" proprietà scale free (p. 143). Nessun test formale e nessun confronto con altre distribuzioni.
  - Authority e citazioni: la tab. 5 ordina le prime 30 pronunce per citazioni ricevute e il testo dice "the same ranking holds with respect to the authority score" (p. 144), sulla rete delle pronunce in via incidentale, per tutto il periodo. Nella tab. 5 i valori di authority crescono esattamente con le citazioni (pronunce con 36 citazioni hanno la stessa authority, 0,00140829).
  - Giudici: i nodi "potrebbero" essere annotati con i giudici (p. 141), ma l'analisi non lo fa. Non ci sono strati di redazione o collegio e non ci sono modelli nulli (verificato sul testo: nessuna occorrenza).
  - Nelle conclusioni i passi successivi sono l'evoluzione nel tempo e il confronto con la dottrina (p. 151), non i giudici.
  - Uso: conferma la lacuna rispetto a questo lavoro; è il confronto per estrattore, dimensione della rete e risultato su authority e citazioni (D1).

**Precedente senza stare decisis: corti europee**
- [L4] Lupu, Y., Voeten, E. (2012). "Precedent in International Courts: A Network Analysis of Case Citations by the European Court of Human Rights". *British Journal of Political Science*, 42(2), 413–439. DOI 10.1017/S0007123411000433. *Letto, 10/11/2026.*
  - Teoria: anche senza stare decisis una corte cita i precedenti per persuadere chi deve applicare le sue decisioni (pp. 413–421).
  - Dati: 7.319 sentenze fino al 2006 con 35.963 citazioni. Tolte le pronunce isolate restano 6.172 nodi. Tolte anche le sentenze ripetitive di livello 3 (casi seriali, come la durata dei processi italiani) restano 2.222 sentenze e 16.863 citazioni (p. 424). È l'analogo delle nostre ordinanze ripetitive.
  - Distribuzioni delle citazioni simili a quelle della Corte Suprema USA, mostrate in scala log-log senza test (pp. 425–426). Le pronunce recenti hanno meno citazioni ricevute solo perché sono nella rete da meno tempo (p. 427): è la censura.
  - Misura: hub score "iniziale", calcolato al momento della pubblicazione. Poiché i punteggi calano quando la rete cresce, controllano per il numero di pronunce già nella rete (pp. 428, 430). Modello Tobit, errori standard raggruppati per paese (p. 430, nota 72).
  - Validazione delle authority: nessun dato esterno; la confrontano con i livelli di importanza assegnati dalla Corte e con le sentenze di Grande Camera (p. 428).
  - Comunità: metodo di Newman (igraph), interpretate con articoli della Convenzione e parole chiave, poi un logit multinomiale. Le comunità seguono la materia giuridica, non il paese (pp. 434–437).
  - Uso: D1 (hub e authority nel tempo, censura, esclusione dei casi seriali); validazione delle comunità con le massime.
- [L5] Derlén, M., Lindholm, J. (2014). "Goodbye van Gend en Loos, Hello Bosman?". *European Law Journal*, 20(5), 667–687. *Scheda.*
- [L6] Derlén, M., Lindholm, J. (2015). "Characteristics of Precedent". *German Law Journal*, 16(5). *Scheda.*
- [L7] Frankenreiter, J. (2017). "Network Analysis and the Use of Precedent in the Case Law of the CJEU – A Reply to Derlén and Lindholm". *German Law Journal*, 18(3), 687–694. DOI 10.1017/S2071832200022112. *Letto per intero, 10/11/2026.*
  - Manca una teoria che dica come un uso "accettabile" o "inaccettabile" del precedente si vedrebbe nella rete (pp. 689–690).
  - Una legge di potenza non prova un uso consapevole: anche citare per eco i casi precedenti sullo stesso tema la produce (p. 690).
  - Senza test formali e senza una "regione critica" i confronti restano soggettivi (p. 691).
  - Le misure di rete servono come variabili in altri studi, dopo averle validate, per esempio confrontando l'authority con una codifica manuale (pp. 692–693). Tra gli esempi: se l'importanza di una pronuncia dipenda dal giudice che l'ha scritta e se cambi quando il giudice lascia la corte (p. 693). È la nostra D2.
- [L8] Šadl, U., Olsen, H. P. (2017). "Can quantitative methods complement doctrinal legal studies?". *Leiden Journal of International Law*, 30(2), 327–349. *Abstract.*
- [L9] Coupette, C. (2019). *Juristische Netzwerkforschung*. Mohr Siebeck, open access. [Zenodo](https://zenodo.org/record/2617115). Tribunale costituzionale federale tedesco. *Scheda.*

**Misure di importanza ed età**
- [L10] Kleinberg, J. M. (1999). "Authoritative sources in a hyperlinked environment". *Journal of the ACM*, 46(5), 604–632. *Scheda.*
- [L11] Fowler, J. H., Johnson, T. R., Spriggs II, J. F., Jeon, S., Wahlbeck, P. J. (2007). "Network Analysis and the Law: Measuring the Legal Importance of Precedents at the U.S. Supreme Court". *Political Analysis*, 15(3), 324–346. DOI 10.1093/pan/mpm011. Letto sul manoscritto degli autori ([PDF](https://pdodds.w3.uvm.edu/files/papers/others/everything/fowler2007a.pdf)): le pagine sotto sono quelle del manoscritto. *Letto, 10/11/2026.*
  - Dati: 26.681 opinioni di maggioranza, 1791–2005; citazioni da Shepard's (pp. 4–5).
  - La centralità per autovettore sottostima le pronunce recenti, perché le pronunce non ancora citate valgono zero: la citazione dipende dal tempo (p. 7).
  - Hub e authority di Kleinberg; poiché solo l'ordine è significativo e la rete cresce, usano il rango percentile di ogni pronuncia in ogni anno (pp. 8–10).
  - Le authority non coincidono con il conteggio delle citazioni: R² = 0,226 nella regressione dell'*Inward Relevance* (rango percentile annuo dell'authority) sul numero di citazioni ricevute (p. 13). Il testo non dice su quale unità sia stimata la regressione, né se il numero di citazioni sia cumulato all'anno: da controllare sulla versione pubblicata, insieme alle pagine della rivista. Le pronunce più autorevoli sono più vecchie (età mediana 64 anni) di quelle con hub più alto (36) (p. 12).
  - Validazione: le misure dell'anno precedente prevedono le citazioni future della stessa Corte, delle corti d'appello e delle corti statali; regressione binomiale negativa per pronuncia-anno, con variabile dipendente ritardata ed età ed età² (pp. 14–17).
  - Uso: D1. È il confronto per il risultato di Agnoloni e Pagallo (authority uguale alle citazioni) e il modello per calcolare le authority anno per anno e validarle.
- [L12] Fowler, J. H., Jeon, S. (2008). "The authority of Supreme Court precedent". *Social Networks*, 30(1), 16–30. Citato dal libro di testo. *Scheda.*
- [L13] Mariani, M. S., Medo, M., Zhang, Y.-C. (2016). "Identification of milestone papers through time-balanced network centrality". *Journal of Informetrics*, 10(4), 1207–1223. [arXiv](https://www.arxiv.org/abs/1608.08414). *Scheda.*

**Durata del precedente (D1b)**
- [L14] Landes, W. M., Posner, R. A. (1976). "Legal Precedent: A Theoretical and Empirical Analysis". *Journal of Law and Economics*, 19(2), 249–307. *Scheda.*
- [L15] Black, R. C., Spriggs, J. F. (2013). "The Citation and Depreciation of U.S. Supreme Court Precedent". *Journal of Empirical Legal Studies*, 10(2), 325–358. DOI 10.1111/jels.12012. Calo dell'81–85% tra il primo e il ventesimo anno; secondo una recensione su JOTWELL, 6.299 decisioni dal 1946 al 2004. *Abstract; nessuna versione libera trovata il 10/11/2026.*

**Influenza e citazioni dei giudici (D2–D4)**
- [L16] Landes, W. M., Lessig, L., Solimine, M. E. (1998). "Judicial Influence: A Citation Analysis of Federal Courts of Appeals Judges". *Journal of Legal Studies*, 27(2), 271–332. DOI 10.1086/468022. *Letto (pp. 271–293, 321–327), 10/11/2026.*
  - Limiti delle citazioni come misura di influenza, elencati dagli autori (pp. 272–276). Fra questi:
    - le citazioni crescono con la durata del mandato;
    - le opinioni le scrivono spesso i clerk, i "ghost writers";
    - le autocitazioni vanno tenute a parte;
    - il "lusso" della citazione gratuita.
  - Dati: 205 giudici con almeno 6 anni di servizio, 3.442 osservazioni giudice-anno, più di 740.000 citazioni, autocitazioni escluse (pp. 277–279, 285). Esclusi i giudici con meno di 6 anni, perché le osservazioni non bastano per stimarli, e i due Gibson, omonimi non distinguibili (p. 277, nota 16).
  - Perché non bastano citazioni per anno o per opinione: favoriscono chi ha servito più a lungo, penalizzano chi è più produttivo, ignorano il deprezzamento (pp. 279–280).
  - Modello: logaritmo delle citazioni annue per giudice, con un effetto fisso per giudice, anni di servizio e il loro quadrato, controlli sulla domanda di citazioni (pp. 281–284).
  - Classifiche: non dare peso a differenze piccole di rango (p. 288). Il giudice mediano non si distingue, al 5%, da quelli tra il 54° e il 145° posto (p. 293).
  - Le autocitazioni sono associate positivamente all'influenza (pp. 321–323).
  - Tra le ricerche future propongono le reti tra giudici: citazioni per età, sesso, preferenze politiche, esperienza (p. 326).
  - Uso: D2 (opportunità, mandato, deprezzamento, soglia minima di pronunce, cautela sui ranghi) e D4 (le reti tra giudici simili).
- [L17] Kosma, M. N. (1998). "Measuring the Influence of Supreme Court Justices". *Journal of Legal Studies*, 27(2), 333–372. *Scheda.*
- [L18] Choi, S. J., Gulati, G. M. (2008). "Bias in Judicial Citations". *Journal of Legal Studies*, 37(1), 87–130. *Scheda.*
- [L19] Frankenreiter, J. (2017). "The Politics of Citations at the ECJ – Policy Preferences of E.U. Member State Governments and the Citation Behavior of Judges at the European Court of Justice". *Journal of Empirical Legal Studies*, 14(4), 813–857. DOI 10.1111/jels.12165. Letto sulla versione accettata (WashU Scholarly Repository; SSRN 2778818): le pagine sotto sono quelle del manoscritto. *Letto, 10/11/2026.*
  - Contesto: alla Corte di giustizia il giudice relatore redige la sentenza anche se non è d'accordo; le deliberazioni sono segrete e non ci sono opinioni dissenzienti; il Presidente assegna le cause, che quindi non sono assegnate a caso (pp. 5–6).
  - Attribuzione: tutte le citazioni di una sentenza sono attribuite al relatore. È un'ipotesi dichiarata e motivata con il carico di lavoro, che lascia poco tempo per discutere le citazioni degli altri (pp. 10–11).
  - Disegno: un'osservazione per ogni citazione possibile, cioè ogni documento precedente, che il nuovo documento può citare o no. Sono 12.412.768 osservazioni, con lo 0,134% di citazioni realizzate. Esclusi i precedenti pubblicati meno di 180 giorni prima e le coppie di giudici dello stesso paese (pp. 10, 15).
  - Modello: logit sui dati completi; differenza di tempo con un polinomiale di quinto grado; controllo per stessa materia; errori standard raggruppati per relatore, 59 gruppi, citando Cameron e Miller (pp. 17–19).
  - Il problema dell'assegnazione non casuale: se giudici simili ricevono cause simili, citano giudici simili anche solo per ragioni giuridiche (pp. 19–21).
  - La soluzione: confrontare le citazioni della sentenza con quelle delle conclusioni dell'Avvocato generale nello stesso caso (pp. 22–26).
  - Risultato: i giudici citano di più i giudici nominati da governi con preferenze simili sull'integrazione europea; l'effetto è piccolo in assoluto, perché le citazioni sono rare (pp. 18, 25–26).
  - Uso: è il disegno più vicino a D3, con un'osservazione per citazione possibile, strati e cluster per redattore. Mostra il problema dell'assegnazione non casuale. Da noi non c'è un Avvocato generale: le assenze dal collegio fanno da variazione esterna.

**Modelli nulli e inferenza**
- [L20] Karrer, B., Newman, M. E. J. (2009). "Random graph models for directed acyclic networks". arXiv:0907.4346 ([PDF](https://arxiv.org/pdf/0907.4346)); Physical Review E 80, 046110 [da verificare]. *Letto (arXiv pp. 1–5, 10), 11/11/2026.*
  - Modello G(n,m): parte dalla sequenza ordinata di citazioni ricevute e fatte di ogni nodo; gli archi vanno solo da nodi successivi a nodi precedenti; l'abbinamento è uniforme tra quelli possibili (pp. 2, 5). Il modello G(n,p) assegna a ogni coppia un numero di archi di Poisson (p. 10).
  - Conserva gradi in entrata, gradi in uscita e ordine nel tempo; **non** conserva la distribuzione dell'età delle citazioni. Per questo il nullo principale è lo scambio alla Uzzi [L21], e Karrer e Newman è la variante.
- [L21] Uzzi, B., et al. (2013). "Atypical combinations and scientific impact". *Science*, 342, 468–472. Materiali supplementari, p. 5: scambi di citazioni ammessi solo tra classi con lo stesso anno di origine e destinazione. Uso: nullo che rispetta il tempo. *Letto (SOM pp. 3, 5).*
- [L22] Clauset, A., Shalizi, C. R., Newman, M. E. J. (2009). "Power-law distributions in empirical data". *SIAM Review*, 51(4), 661–703. *Scheda.*
- [L23] Broido, A. D., Clauset, A. (2019). "Scale-free networks are rare". *Nature Communications*, 10, 1017. *Scheda.*
- [L24] King, G., Zeng, L. (2001). "Logistic Regression in Rare Events Data". *Political Analysis*, 9(2), 137–163. [PDF](https://gking.harvard.edu/files/0s.pdf). *Letto (pp. 140–144, 160), 10/11/2026.*
  - Gli eventi (gli 1) sono più informativi dei non eventi; campionare tutti gli eventi e una frazione casuale dei non eventi è un disegno efficiente (pp. 140–142).
  - Quanti non eventi: l'informazione per ogni zero in più cala quando gli zeri superano gli uni, quindi raramente servono più di "due a cinque volte" tanti zeri quanti uni. Pratica consigliata: partire da un numero pari e aggiungere zeri finché gli intervalli non sono abbastanza stretti (pp. 142–143).
  - Correzione: con il campionamento sugli esiti, nel logit i coefficienti delle variabili restano consistenti; va corretta solo la costante (correzione a priori, p. 144; dimostrazione in appendice B, eq. 29, p. 160). Condizioni: selezione casuale e indipendente di uni e zeri, e nessuna selezione diversa sulle variabili esplicative nei due gruppi (p. 142).
  - Uso per D3: il logit condizionato non ha costante, perché ogni pronuncia che cita è uno strato. Quindi gli odds ratio non richiedono correzione, purché i non citati siano estratti a caso tra i disponibili, senza filtrare sulle variabili del modello.

- [L25] Cameron, A. C., Miller, D. L. (2015). "A Practitioner's Guide to Cluster-Robust Inference". *Journal of Human Resources*, 50(2), 317–372. *Scheda.*
- [L26] Holm, S. (1979). "A simple sequentially rejective multiple test procedure". *Scandinavian Journal of Statistics*, 6(2), 65–70. *Scheda.*

**Corso**
- [L27] Easley, D., Kleinberg, J. (2010). *Networks, Crowds, and Markets*. CUP, cap. 14. Indice completo dei 24 capitoli letto il 18/11/2026 sulla [pagina degli autori](https://www.cs.cornell.edu/home/kleinber/networks-book/), per la mappa del programma. [capitolo](https://www.cs.cornell.edu/home/kleinber/networks-book/networks-book-ch14.pdf). §14.5, pp. 415–417: Fowler e Jeon sulla Corte Suprema USA. *Letto.* Cap. 5, *Positive and Negative Relationships*, pp. 119–152, letto il 20/11/2026 ([capitolo](https://www.cs.cornell.edu/home/kleinber/networks-book/networks-book-ch05.pdf)): proprietà dell'equilibrio strutturale per grafi completi con legami positivi e negativi, un triangolo è equilibrato se ha tre legami positivi o uno solo (§5.1, p. 122); teorema dell'equilibrio di Harary, due gruppi contrapposti (§5.2, p. 124); fiducia e sfiducia tra gli utenti di Epinions formano un grafo orientato, e lì le previsioni dell'equilibrio possono non valere (§5.3, p. 128); equilibrio debole (§5.4, p. 130); reti non complete, con due definizioni equivalenti (§5.5, pp. 134–135). Cap. 20, *The Small-World Phenomenon*, pp. 611–644, letto il 20/11/2026 ([capitolo](https://www.cs.cornell.edu/home/kleinber/networks-book/networks-book-ch20.pdf)): il fenomeno del piccolo mondo è l'abbondanza di cammini brevi nelle reti sociali (p. 611); la chiusura triadica riduce il numero di persone raggiungibili in pochi passi, e il modello di Watts e Strogatz mostra che pochi legami casuali bastano per avere insieme molti triangoli chiusi e cammini brevi (§20.2, pp. 612–616). Le pagine sono quelle della versione completa messa in rete dagli autori.
- [L28] Barabási, A.-L. (2016). *Network Science*. CUP. *Indicato nel programma.* [Versione online](http://networksciencebook.com/). Il 18/11/2026 è stato letto l'indice dei capitoli 1–10, con i titoli delle sezioni, per la mappa in `docs/course_mapping.md`. Il 20/11/2026 è stato letto il cap. 3, *Random Networks*, nelle parti §3.8 *Small Worlds* (in una rete casuale la distanza media è circa ln N / ln⟨k⟩, eq. 3.19: "piccolo" vuol dire proporzionale a ln N), §3.9 *Clustering Coefficient* (in una rete casuale il coefficiente di clustering è ⟨k⟩/N, eq. 3.21; nelle reti reali è molto più alto che in una rete casuale con gli stessi nodi e legami; per il calcolo le reti orientate sono rese non orientate, immagine 3.13), box 3.9 *Watts-Strogatz Model* (distanze brevi e clustering alto insieme) e §3.10 *Summary*. L'edizione online non ha numeri di pagina: si citano sezione, equazione e box.
- [L29] Ca' Foscari, Social Media and Web Analytics [EM1421], programma 2026/27. [pagina](https://www.unive.it/data/course/790312/programma). Corso in inglese; orale con teoria (30%) e progetto (70%), individuale o in coppia. *Letto.* Riletto il 18/11/2026 ("programma definitivo", ultima modifica 26/06/2026): sei voci senza sotto-argomenti, risultati di apprendimento, prerequisiti, i due libri di testo senza capitoli.

## 4. Non trovato o da verificare
- Agnoloni e Pagallo, testi integrali: periodo, numero di pronunce, metodo di estrazione, risultati.
- Anzon, *Il valore del precedente nel giudizio sulle leggi* (1995): scheda affidabile non trovata.
- Elenco ufficiale delle sostituzioni del relatore: non esiste; i casi si trovano in epigrafi e firme [C4].
- Pagina "pronunce redatte" per giudice sul sito della Corte: da provare nel browser come controllo dell'abbinamento redattore-anagrafica.
- Studi sui singoli giudici in altre corti costituzionali europee (Germania, Spagna): non cercati in modo sistematico.
- Testo della deliberazione del 7/7/1987 sulle firme.
