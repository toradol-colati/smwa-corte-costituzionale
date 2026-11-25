import React from 'react';
import { ScientificFigure, ScientificTable, SectionTitle, SubTitle } from './UI';
import { fmtCI, fmtDec, fmtInt, fmtP, fmtPct } from '../utils/format';

export function AbstractSection({ data }) {
  const { network, d1, d2, d3, d4, succession } = data;
  const sat = d3.primary.coef.sat_not_drafted;
  const selfD = d3.primary.coef.self_drafted;
  const selfNorm = d3.variants['controllo per norma impugnata in comune (esplorativo)'].coef.self_drafted;

  return (
    <section id="abstract" className="scroll-mt-20 my-8 py-5 px-5 sm:px-6 bg-white border border-rule">
      <div className="font-mono text-[11px] uppercase tracking-widest text-muted mb-3">
        Abstract strutturato
      </div>
      <div className="space-y-2.5 text-[0.92rem] leading-relaxed text-zinc-800">
        <p>
          <strong className="text-ink">Contesto.</strong> Nell&apos;ordinamento costituzionale
          italiano il precedente non è formalmente vincolante, eppure la Corte costituzionale cita
          sistematicamente le proprie decisioni passate. Non è ancora noto se nella giurisprudenza
          costituzionale italiana l&apos;autorità di un precedente dipenda dai giudici che lo hanno
          redatto e deciso, oppure appartenga esclusivamente alla Corte come istituzione.
        </p>
        <p>
          <strong className="text-ink">Metodi.</strong> Abbiamo costruito la rete completa delle
          citazioni interne su tutte le {fmtInt(network.nodes)} pronunce depositate tra il 1956 e il
          2026 ({fmtInt(network.edges)} legami diretti verso il passato), incrociandola con il
          giudice redattore e la composizione del collegio decidente (125 giudici). Ogni misura è
          confrontata con modelli nulli che preservano l&apos;ordine temporale. L&apos;endpoint
          primario, fissato prima di ispezionare i risultati, è l&apos;odds ratio di citazione per i
          precedenti decisi da un collegio in cui il redattore sedeva senza averli scritti, stimato
          via regressione logistica condizionata esatta sulle assenze dal collegio.
        </p>
        <p>
          <strong className="text-ink">Risultati.</strong> Sull&apos;endpoint primario non emerge
          alcun effetto della partecipazione collegiale: odds ratio {fmtDec(sat.or)} (intervallo di
          confidenza al 95%: {fmtCI(sat.lo, sat.hi)}; <em>p</em> = {fmtP(sat.p)};{' '}
          {fmtInt(d3.primary.strata)} pronunce, {fmtInt(d3.primary.cases)} citazioni). In analisi
          esplorativa, il redattore cita invece molto più spesso i precedenti scritti da sé (odds
          ratio {fmtDec(selfD.or)}; {fmtCI(selfD.lo, selfD.hi)}), effetto che scende a{' '}
          {fmtDec(selfNorm.or)} ({fmtCI(selfNorm.lo, selfNorm.hi)}) controllando per identità della
          disposizione impugnata. Le citazioni sono concentrate (l&apos;1% più citato raccoglie il{' '}
          {fmtPct(d1.concentration.top1_share.observed)} contro il{' '}
          {fmtPct(d1.concentration.top1_share.null_mean)} atteso), decadono rapidamente (picco a 1
          anno, dimezzamento in 3 anni) e vengono in parte sostituite dai successori (+
          {fmtPct(succession.later_window.ratio_successors_controls - 1, 0)} nella finestra 4–15
          anni). Su {d2.permutazione_anno.judges_tested} giudici valutati singolarmente, dopo
          correzione di Holm solo {d2.permutazione_anno.sig_holm_above} superano l&apos;atteso e{' '}
          {d2.permutazione_anno.sig_holm_below} stanno sotto; l&apos;omofilia per organo di nomina è
          nulla (<em>p</em> = {fmtP(d4.organo.p_holm)}) e per provenienza resta sotto la soglia del
          20% (+{fmtPct(d4.provenienza.excess_over_null)}).
        </p>
        <p>
          <strong className="text-ink">Conclusione.</strong> La Corte costruisce precedenti
          concentrati ma di vita breve, la cui autorità non circola attraverso la semplice
          partecipazione al collegio decidente; l&apos;impronta individuale emerge solo attraverso
          il redattore ed è in larga parte riconducibile alla continuità sulle stesse questioni.
        </p>
      </div>
    </section>
  );
}

export function SectionIntroduction() {
  return (
    <section className="article-prose">
      <SectionTitle id="introduzione" num="1" title="Introduzione" />
      <p>
        Le reti di citazioni giurisprudenziali sono studiate come indicatori empirici della
        formazione dell&apos;autorità giuridica nella Corte suprema degli Stati Uniti (Fowler et
        al., 2007), nella Corte europea dei diritti dell&apos;uomo (Lupu e Voeten, 2012) e nella
        Corte di giustizia dell&apos;Unione europea (Frankenreiter, 2017b). Sulla Corte
        costituzionale italiana, l&apos;unico studio di rete precedente (Agnoloni e Pagallo, 2016) ha
        analizzato le sole pronunce in via incidentale (16.320 nodi), proponendo una distribuzione a
        legge di potenza mediante ispezione grafica e sostenendo la coincidenza tra le prime 30
        pronunce per citazioni e per punteggio di autorevolezza HITS, senza confronti con modelli
        nulli né analisi sui giudici. Come mostrato da Frankenreiter (2017a), una distribuzione a
        coda pesante può derivare da abitudini citazionali ripetitive e non dimostra di per sé una
        gerarchia deliberata dei precedenti.
      </p>
      <p>
        Parallelamente, la letteratura sul peso individuale dei giudici (Landes, Lessig e Solimine,
        1998; Frankenreiter, 2017b) evidenzia due ostacoli strutturali nelle corti collegiali prive
        di opinioni dissenzienti: le citazioni crescono con la durata del mandato e
        l&apos;assegnazione non casuale dei relatori da parte del Presidente può indurre
        autocitazioni per sola contiguità di materia. Restava dunque aperto se, nella Corte
        costituzionale italiana, l&apos;autorità dei precedenti dipenda dalle persone che li hanno
        redatti e decisi, e in particolare se un giudice citi più spesso i precedenti decisi da
        collegi di cui faceva parte.
      </p>
      <p className="pl-4 border-l-2 border-primary italic font-serif text-ink my-5">
        Domanda di ricerca: «In un ordinamento in cui il precedente non vincola, la Corte
        costituzionale costruisce comunque una gerarchia di precedenti? E quanto di quell&apos;autorità
        passa attraverso i giudici che redigono e decidono le pronunce?»
      </p>
      <p>
        L&apos;obiettivo primario dello studio è stimare se aver partecipato al collegio decidente di
        un precedente aumenti la probabilità che lo stesso giudice lo citi quando redige una nuova
        pronuncia (<strong>D3</strong>). Gli obiettivi secondari valutano la concentrazione delle
        citazioni, la replicabilità dei risultati su HITS e legge di potenza e la durata dei
        precedenti (<strong>D1</strong> e <strong>D1b</strong>), le differenze tra singoli redattori
        durante e dopo il mandato (<strong>D2</strong>) e l&apos;omofilia citazionale per organo di
        nomina e provenienza professionale (<strong>D4</strong>).
      </p>
    </section>
  );
}

export function SectionMethods({ data }) {
  const { network, numbers, massime, api, sedute, topics, parametri } = data;
  const meanStab = topics.stability.reduce((a, b) => a + b, 0) / topics.stability.length;

  return (
    <section className="article-prose">
      <SectionTitle id="metodi" num="2" title="Metodi" />

      <SubTitle id="metodi-dati" num="2.1" title="Dati, fonti e contesto istituzionale" />
      <p>
        I dati provengono dal portale open data della Corte costituzionale (
        <code className="font-mono text-xs">dati.cortecostituzionale.it</code>, licenza CC BY-SA
        3.0), scaricati l&apos;8 novembre 2026 con registrazione dell&apos;impronta SHA-256 in{' '}
        <code className="font-mono text-xs">data/raw/MANIFEST.csv</code>. Gli archivi XML coprono{' '}
        <strong>{fmtInt(network.nodes)} pronunce</strong> ({fmtInt(network.by_type.S.n)} sentenze e{' '}
        {fmtInt(network.by_type.O.n)} ordinanze, dal 1956 al {numbers.last_year.last_deposit}, senza
        buchi né doppioni di numerazione), <strong>{fmtInt(massime.massime)} massime</strong>{' '}
        redatte dall&apos;Ufficio del massimario e <strong>125 giudici</strong> (136 righe
        anagrafiche escluse 11 righe multi-nome). Attraverso API sono stati integrati gli esiti dal
        2005 ({fmtInt(api.esiti_pronunce)} pronunce, {fmtInt(api.esiti_rows)} righe dispositivo) e i
        verbali di seduta dal 2004 ({fmtInt(api.sedute_pronunce)} pronunce) dall&apos;endpoint
        SPARQL della Corte, nonché i rimandi da Wikipedia in italiano ({fmtInt(api.wikipedia_pronunce)}{' '}
        pronunce in {fmtInt(api.wikipedia_pages)} voci).
      </p>
      <p>
        Ogni pronuncia è decisa dal collegio (da 11 a 15 giudici; quorum 11 ex art. 16 legge
        87/1953) in camera di consiglio senza voto pubblico né opinioni dissenzienti; il redattore
        stende le motivazioni approvate dal collegio. Per questo si parla sempre di &laquo;pronunce
        redatte da X&raquo;, mai di &laquo;decisioni di X&raquo;. L&apos;ispezione dei testi ha
        rivelato tre regimi temporali per il redattore (Figura 2): fino alla pronuncia 286/1986
        (5.678 pronunce) firmano tutti i giudici e il redattore non è indicato (si usa il relatore
        come approssimazione dichiarata); dalla 287/1986 (depositata il 23/12/1986) al 2001 il
        redattore compare solo nelle firme (8.349 pronunce); dal 2002 è nel campo strutturato (8.384
        pronunce). Poiché l&apos;anagrafica ufficiale contiene 33 date di cessazione mancanti e
        diversi errori (Appendice B), il periodo &laquo;in attività&raquo; di ciascun giudice è
        definito dalla sua prima all&apos;ultima presenza in un collegio.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 my-6">
        <ScientificFigure
          id="fig-1"
          label="Figura 1"
          caption="Numero annuo di pronunce depositate dalla Corte costituzionale per tipologia (sentenze e ordinanze), 1956–2026 (n = 22.427)."
        >
          <img
            src="./figures/fig1_pronunce_per_anno.png"
            alt="Pronunce depositate per anno e tipo"
            loading="lazy"
            className="w-full h-auto"
          />
        </ScientificFigure>
        <ScientificFigure
          id="fig-2"
          label="Figura 2"
          caption="Quota annuale di pronunce per sorgente del nome del redattore: approssimazione via relatore fino alla 286/1986, firma testuale (1987–2001) e campo strutturato (dal 2002)."
        >
          <img
            src="./figures/fig2_fonte_redattore.png"
            alt="Sorgente del nome del redattore per anno"
            loading="lazy"
            className="w-full h-auto"
          />
        </ScientificFigure>
      </div>

      <SubTitle id="metodi-reti" num="2.2" title="Costruzione delle reti" />
      <p>
        L&apos;analisi integra cinque strutture di rete definite sugli stessi dati (Tabella 1). La
        rete delle citazioni è un grafo diretto aciclico (DAG) ordinato per data di deposito; le
        misure prive di significato su DAG (reciprocità, componenti fortemente connesse, clustering
        diretto) sono escluse per disegno. La rete di co-sitting è usata esclusivamente a fini
        descrittivi e di controllo dei dati, poiché tra giudici coevi è quasi completa.
      </p>

      <ScientificTable
        id="tab-1"
        label="Tabella 1"
        title="Definizione formale di nodi, archi, direzione e peso per ciascuna rete costruita."
        note="Le citazioni tra pronunce depositate lo stesso giorno (268 menzioni) sono registrate separatamente e tenute fuori dal grafo aciclico."
      >
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-zinc-800 text-left font-mono text-muted">
              <th className="p-2">Rete</th>
              <th className="p-2">Nodi</th>
              <th className="p-2">Arco</th>
              <th className="p-2">Direzione</th>
              <th className="p-2">Peso</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100">
            <tr>
              <td className="p-2 font-medium text-ink">Citazioni</td>
              <td className="p-2">Pronunce (22.427)</td>
              <td className="p-2">A cita B nel testo di base</td>
              <td className="p-2">Diretto (verso il passato)</td>
              <td className="p-2">Non pesato (coppia distinta)</td>
            </tr>
            <tr>
              <td className="p-2 font-medium text-ink">Redazione (bipartita)</td>
              <td className="p-2">Giudici e pronunce</td>
              <td className="p-2">Il giudice ha redatto la pronuncia</td>
              <td className="p-2">Non diretto</td>
              <td className="p-2">Non pesato</td>
            </tr>
            <tr>
              <td className="p-2 font-medium text-ink">Collegio (affiliazione)</td>
              <td className="p-2">Giudici e pronunce</td>
              <td className="p-2">Il giudice sedeva nel collegio</td>
              <td className="p-2">Non diretto</td>
              <td className="p-2">Non pesato</td>
            </tr>
            <tr>
              <td className="p-2 font-medium text-ink">Influenza tra giudici</td>
              <td className="p-2">Giudici (122)</td>
              <td className="p-2">Pronunce redatte da A citano B</td>
              <td className="p-2">Diretto (A → B)</td>
              <td className="p-2">Numero di citazioni</td>
            </tr>
            <tr>
              <td className="p-2 font-medium text-ink">Co-sitting (proiezione)</td>
              <td className="p-2">Giudici (123)</td>
              <td className="p-2">A e B nel medesimo collegio</td>
              <td className="p-2">Non diretto</td>
              <td className="p-2">Pronunce decise insieme</td>
            </tr>
          </tbody>
        </table>
      </ScientificTable>

      <SubTitle id="metodi-estrazione" num="2.3" title="Estrazione citazioni, classificazione della materia e controlli di qualità" />
      <p>
        Le citazioni sono estratte nel <em>testo di base</em> («Considerato in diritto» +
        dispositivo nelle sentenze; «Considerato che» + dispositivo nelle ordinanze; fallback al
        testo intero in {fmtInt(numbers.split_failed)} testi non divisibili,{' '}
        {fmtPct(numbers.split_failed_share)}), escludendo il «Ritenuto in fatto» per non attribuire
        alla Corte le citazioni delle parti. Su {fmtInt(numbers.mentions_valid)} menzioni valide
        (scartate {fmtInt(numbers.mentions_excluded)} menzioni di altre corti o atti di rimessione e{' '}
        {fmtInt(numbers.mentions_errors)} errori) si ottengono {fmtInt(network.edges)} archi
        distinti. Il controllo sulle note editoriali delle massime rileva{' '}
        {fmtInt(massime.pairs_in_massime)} coppie, già presenti nel testo di base al{' '}
        {fmtPct(massime.share_also_in_base_text)}.
      </p>
      <p>
        Per il controllo della materia è stato stimato un modello LDA su 46.126 massime (&gt;50
        caratteri, vocabolario 8.000 parole), scegliendo con regola preregistrata{' '}
        <strong>k = {topics.k} temi</strong> (massima coerenza NPMI{' '}
        {fmtDec(topics.coherence['20'], 4)}; NMI {fmtDec(topics.nmi_title, 3)} con i titoli dal
        2015, {fmtDec(topics.nmi_art, 3)} con gli articoli costituzionali; stabilità media Jaccard{' '}
        {fmtDec(meanStab, 3)}; {fmtInt(numbers.pronunce_without_topic)} pronunce senza tema). Come
        controllo fine, sono stati estratti i {parametri.distinct_articles} articoli costituzionali
        invocati nelle massime (copertura {fmtPct(parametri.pronunce_with_massime_and_article_share)},
        pesati con <em>ln(N/n)</em>; dettagli in Appendice C). Le soglie di qualità e gli esiti
        della validazione sono riassunti in Tabella 2.
      </p>

      <ScientificTable
        id="tab-2"
        label="Tabella 2"
        title="Soglie di qualità preregistrate, esiti della validazione interna e controlli esterni SPARQL."
        note="Le letture di riferimento delle citazioni (342 coppie in totale) sono state prodotte da Claude sui soli passi con parole chiave; il foglio per la validazione umana indipendente (36 pronunce) è pronto ma non ancora compilato."
      >
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-zinc-800 text-left font-mono text-muted">
              <th className="p-2">Controllo</th>
              <th className="p-2 text-right">Soglia</th>
              <th className="p-2 text-right">Esito misurato (IC 95%)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100 font-mono tabular-nums">
            <tr>
              <td className="p-2 font-sans text-ink">Citazioni — Round 1, dal 1987 (37 pron., 230 coppie)</td>
              <td className="p-2 text-right">P ≥0,95 · R ≥0,90</td>
              <td className="p-2 text-right">P 1,000 (0,983–1,000) · R 0,974 (0,944–0,988)</td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Citazioni — Round 1, fino al 1986 (27 pron., 40 coppie)</td>
              <td className="p-2 text-right">P ≥0,95 · R ≥0,90</td>
              <td className="p-2 text-right text-primary">P 1,000 · R 0,750 (sotto soglia → corretto)</td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Citazioni — Test 2 indipendente, ≤1986 (48 pron., 72 coppie)</td>
              <td className="p-2 text-right">P ≥0,95 · R ≥0,90</td>
              <td className="p-2 text-right">P 0,985 (0,920–0,997) · R 0,917 (0,830–0,961)</td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Collegamento redattore ad anagrafica giudici</td>
              <td className="p-2 text-right">≥98,0%</td>
              <td className="p-2 text-right">99,84%</td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Collegio riconosciuto per intero (11–15 giudici)</td>
              <td className="p-2 text-right">≥98,0%</td>
              <td className="p-2 text-right">98,85% (257 pronunce incomplete)</td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Accordo relatore XML vs SPARQL (22.426 pronunce)</td>
              <td className="p-2 text-right">controllo esterno</td>
              <td className="p-2 text-right">97,12% (635/645 scarti = 2 refusi corretti)</td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Collegio XML vs sedute SPARQL (2004–2026, {fmtInt(sedute.pronunce)} pron.)</td>
              <td className="p-2 text-right">controllo esterno</td>
              <td className="p-2 text-right">
                {fmtPct(sedute.quota_collegio_presente_in_seduta)} in seduta · {fmtPct(sedute.quota_seduta_presente_in_collegio)} in collegio
              </td>
            </tr>
          </tbody>
        </table>
      </ScientificTable>

      <SubTitle id="metodi-statistica" num="2.4" title="Analisi statistica, modelli nulli e preregistrazione" />
      <p>
        Tutte le stime riportano intervalli di confidenza al 95% e un termine di confronto nullo
        (1.000 repliche per D1 e D4, 10.000 per D2, con semi fissi; livello di significatività α =
        0,05 a due code). Per <strong>D3 (endpoint primario)</strong> si stima una regressione
        logistica condizionata con calcolo esatto della verosimiglianza: dentro ciascuna pronuncia
        che cita si confrontano tutti i precedenti citati decisi durante il mandato del redattore
        con 50 precedenti non citati estratti a caso (King e Zeng, 2001), controllando per
        auto-redazione, classi d&apos;età e somiglianza coseno dei temi, con errori standard
        raggruppati per redattore. L&apos;identificazione separa la presenza dall&apos;età sfruttando
        le assenze dal collegio. Per <strong>D1</strong> si confrontano concentrazione (vs bersagli
        casuali nello stesso anno, e in variante esplorativa stesso anno e tipo), coda della
        distribuzione (Clauset, Shalizi e Newman, 2009), HITS/PageRank (vs scambi alla Uzzi et al.,
        2013) e capacità predittiva out-of-sample (stima ≤2010, prova 2011–2025; criterio ≥2%
        riduzione devianza). Per <strong>D2</strong> (giudici con ≥30 pronunce, finestra 10 anni,
        senza autocitazioni) si applica la permutazione dei redattori per anno con correzione di
        Holm; per <strong>D4</strong> la permutazione degli attributi per decennio di ingresso
        (soglia di potenza ≥0,80 per effetto minimo del 20%). La Tabella 3 distingue ciò che è stato
        fissato prima dei risultati da ciò che è stato modificato o aggiunto dopo.
      </p>

      <ScientificTable
        id="tab-3"
        label="Tabella 3"
        title="Stato di preregistrazione delle analisi e modifiche intervenute dopo l'ispezione dei risultati."
        note="Le modifiche successive al 18/11/2026 sono tracciate nella storia git; le scelte del 16/11/2026 sono registrate in docs/decisions.md."
      >
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-zinc-800 text-left font-mono text-muted">
              <th className="p-2">Analisi</th>
              <th className="p-2">Fissato prima dei risultati</th>
              <th className="p-2">Modificato o aggiunto dopo</th>
              <th className="p-2">Statuto</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100">
            <tr>
              <td className="p-2 font-medium text-ink">D3 (principale)</td>
              <td className="p-2">Presente vs assente nel mandato; 50 controlli/strato; SE cluster</td>
              <td className="p-2">Calcolo esatto al posto dell&apos;approssimazione di Breslow</td>
              <td className="p-2 font-mono text-primary">principale</td>
            </tr>
            <tr>
              <td className="p-2 font-medium text-ink">D3 (varianti)</td>
              <td className="p-2">6 prove di robustezza + modello completo</td>
              <td className="p-2">Controllo norma impugnata, parametri cost., assenze, controllo 0,88</td>
              <td className="p-2 font-mono text-accent">esplorativo</td>
            </tr>
            <tr>
              <td className="p-2 font-medium text-ink">D1 / D1b</td>
              <td className="p-2">Nullo stesso anno; HITS vs Uzzi; previsione ≥2%; Kaplan–Meier</td>
              <td className="p-2">Nullo anno+tipo; verifica sostituzione precedenti</td>
              <td className="p-2 font-mono text-muted">secondario / espl.</td>
            </tr>
            <tr>
              <td className="p-2 font-medium text-ink">D2</td>
              <td className="p-2">≥30 pronunce, finestra 10 anni, nullo citazioni casuali</td>
              <td className="p-2">Nullo cambiato in permutazione giudici (10.000×)</td>
              <td className="p-2 font-mono text-accent">esplorativo</td>
            </tr>
            <tr>
              <td className="p-2 font-medium text-ink">D4</td>
              <td className="p-2">Effetto minimo 20%, potenza ≥0,80, Holm</td>
              <td className="p-2">Nessuna modifica</td>
              <td className="p-2 font-mono text-muted">secondario</td>
            </tr>
            <tr>
              <td className="p-2 font-medium text-ink">Polarità</td>
              <td className="p-2">Soglia precisione ≥0,80 su test cieco, regola d&apos;arresto</td>
              <td className="p-2">Nessuna modifica: arresto applicato (0,76 &lt; 0,80)</td>
              <td className="p-2 font-mono text-amber-800">negativo</td>
            </tr>
          </tbody>
        </table>
      </ScientificTable>
    </section>
  );
}
