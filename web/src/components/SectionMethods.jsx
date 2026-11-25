import React, { useState } from 'react';
import { Badge, FigureBox, SectionHeader, StaticPngFigure, SubHeader, TabButton } from './UI';
import { fmtDec, fmtInt, fmtPct } from '../utils/format';

export function SectionMethods({ data }) {
  const [showAllTopics, setShowAllTopics] = useState(false);
  const { network, numbers, massime, api, sedute, topics, parametri } = data;

  const topicIds = Object.keys(topics.top_words).sort((a, b) => Number(a) - Number(b));
  const visibleTopics = showAllTopics ? topicIds : topicIds.slice(0, 10);
  const meanStab =
    topics.stability.reduce((acc, v) => acc + v, 0) / topics.stability.length;

  const preregRows = [
    [
      'D3, risultato principale',
      'Presente vs assente nel mandato; controlli self_drafted, classi di età, topic; 50 controlli/strato; SE cluster per redattore',
      'Calcolo esatto al posto di Breslow (1,03 → 1,00; self_drafted 3,01 → 5,47). Domanda invariata',
      'principale',
    ],
    [
      'D3, prove aggiuntive',
      '6 varianti di robustezza + modello completo',
      'Aggiunti controllo norma impugnata, parametri cost., diagnostica assenze e controllo 0,88',
      'esplorativo',
    ],
    [
      'D1, concentrazione e HITS',
      'Nullo stesso anno; HITS vs scambi Uzzi; criterio predittivo ≥2% riduzione devianza',
      'Aggiunto nullo stesso anno e tipo; ritirata lettura "conta chi ti cita" dopo verifica cluster HITS',
      'secondario',
    ],
    [
      'D2, giudici',
      '≥30 pronunce, finestra 10 anni, nullo citazioni casuali nello stesso anno',
      'Nullo cambiato in permutazione giudici (10.000×); applicata finestra 10 anni; aggiunta prova dal 1987',
      'esplorativo',
    ],
    [
      'D4, gruppi',
      'Effetto minimo 20%, potenza ≥0,80, correzione di Holm',
      'Nessuna modifica (generatore RNG dedicato)',
      'secondario',
    ],
    [
      'Polarità citazioni',
      'Soglia precisione 0,80 su test cieco, regola di arresto',
      'Nessuna modifica: 0,76 < 0,80 → nessuna analisi',
      'negativo',
    ],
    [
      'Sostituzione & Misure corso',
      'Non previste nel piano iniziale',
      'Aggiunte in seguito; sostituzione con regole fissate prima del lancio',
      'esplorativo',
    ],
    [
      'Qualità estrazione',
      'Precisione ≥0,95, richiamo ≥0,90 su ≥460 coppie',
      '342 coppie lette da Claude; correzione pre-1987 e secondo campione; manca lettura umana (36 pronunce)',
      'descrittivo',
    ],
  ];

  return (
    <section>
      <SectionHeader
        id="metodi"
        num="1"
        title="Dati, contesto giuridico e controllo di qualità"
        subtitle="Archivi open data della Corte (CC BY-SA 3.0, scaricati l'8/11/2026), estrazione citazioni, riconoscimento giudici, validazione SPARQL, topic LDA e parametri costituzionali."
      />

      <div className="prose-editorial text-sm">
        <p>
          Tutti i dati provengono dal portale open data della Corte costituzionale (
          <code className="font-mono text-xs">dati.cortecostituzionale.it</code>, scaricati
          l&apos;8/11/2026 con manifest SHA-256). Gli archivi XML coprono{' '}
          <strong>{fmtInt(network.nodes)} pronunce</strong> ({fmtInt(network.by_type.S.n)} sentenze
          e {fmtInt(network.by_type.O.n)} ordinanze, 1956–2026),{' '}
          <strong>{fmtInt(massime.massime)} massime</strong> e <strong>125 giudici</strong> (136
          righe anagrafiche meno 11 righe multi-nome). Sono state inoltre interrogate due API (
          <code className="font-mono text-xs">api_fetch.json</code>, {api.fetched_at.slice(0, 10)}):
          l&apos;endpoint SPARQL della Corte ({fmtInt(api.esiti_pronunce)} pronunce con esito dal
          2005, {fmtInt(api.esiti_rows)} righe esiti di cui {fmtInt(api.pronunce_illegittimita)} con
          illegittimità; {fmtInt(api.sedute_pronunce)} pronunce con sedute) e MediaWiki di Wikipedia
          in italiano ({fmtInt(api.wikipedia_pronunce)} pronunce citate in{' '}
          {fmtInt(api.wikipedia_pages)} voci).
        </p>
      </div>

      {/* Figure 1 e 2 originali PNG */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 my-6">
        <FigureBox
          num="Figura 1"
          title="Pronunce depositate per anno e tipo (1956–2026)"
          caption="Serie annuale di sentenze e ordinanze. Il picco del 1987–1989 corrisponde allo smaltimento delle cause arretrate."
          source="reports/figures/fig1_pronunce_per_anno.png"
        >
          <StaticPngFigure
            src="./figures/fig1_pronunce_per_anno.png"
            alt="Pronunce per anno e tipo"
          />
        </FigureBox>
        <FigureBox
          num="Figura 2"
          title="Fonte del nome del redattore per anno di deposito"
          caption="Fino alla pronuncia 286/1986 (5.678 pronunce) firmano tutti i giudici e si usa il relatore; dalla 287/1986 (23/12/1986) al 2001 il redattore sta nelle firme (8.349); dal 2002 nel campo strutturato (8.384)."
          source="reports/figures/fig2_fonte_redattore.png"
        >
          <StaticPngFigure
            src="./figures/fig2_fonte_redattore.png"
            alt="Fonte del redattore per anno"
          />
        </FigureBox>
      </div>

      {/* Estrazione e validazione citazioni */}
      <SubHeader id="qualita" title="Estrazione delle citazioni e controlli di qualità" badge="descrittivo" />
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 my-4">
        <div className="bg-white border border-rule rounded-sm p-4">
          <div className="text-xs font-mono uppercase tracking-wider text-muted mb-2">
            Flusso di estrazione nel testo di base
          </div>
          <table className="w-full text-xs">
            <tbody className="divide-y divide-zinc-100">
              <tr>
                <td className="py-1.5 text-zinc-700">Menzioni valide (tutto il testo)</td>
                <td className="py-1.5 text-right font-mono tabular-nums">{fmtInt(numbers.mentions_valid)}</td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Scartate (altre corti, reg. ord., senza anno)</td>
                <td className="py-1.5 text-right font-mono tabular-nums">{fmtInt(numbers.mentions_excluded)}</td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Errori (inesistenti o date successive)</td>
                <td className="py-1.5 text-right font-mono tabular-nums">{fmtInt(numbers.mentions_errors)}</td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Stessa data di deposito (tenute a parte)</td>
                <td className="py-1.5 text-right font-mono tabular-nums">{fmtInt(numbers.mentions_same_date)}</td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Testi non divisi (fallback testo intero)</td>
                <td className="py-1.5 text-right font-mono tabular-nums">
                  {fmtInt(numbers.split_failed)} ({fmtPct(numbers.split_failed_share)})
                </td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Tipo scritto diverso dal tipo reale</td>
                <td className="py-1.5 text-right font-mono tabular-nums">
                  {fmtPct(numbers.type_mismatch_share)}
                </td>
              </tr>
              <tr className="font-semibold">
                <td className="py-1.5 text-ink">Legami distinti nel testo di base (rete)</td>
                <td className="py-1.5 text-right font-mono tabular-nums text-primary">
                  {fmtInt(network.edges)}
                </td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Coppie nelle massime (già in base: {fmtPct(massime.share_also_in_base_text)})</td>
                <td className="py-1.5 text-right font-mono tabular-nums">
                  {fmtInt(massime.pairs_in_massime)} (+{fmtInt(massime.pairs_only_in_massime)})
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="bg-white border border-rule rounded-sm p-4">
          <div className="text-xs font-mono uppercase tracking-wider text-muted mb-2">
            Soglie preregistrate, validazione e controlli SPARQL
          </div>
          <table className="w-full text-xs">
            <tbody className="divide-y divide-zinc-100">
              <tr>
                <td className="py-1.5 text-zinc-700">Citazioni Round 1 (64 pron., 270 coppie)</td>
                <td className="py-1.5 text-right font-mono">P 1,000 · R 0,941 (pre-87: 0,750)</td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Citazioni Test 2 pre-1987 (48 pron., 72 coppie)</td>
                <td className="py-1.5 text-right font-mono">P 0,985 · R 0,917 (0,830–0,961)</td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Redattore collegato ad anagrafica (soglia ≥98%)</td>
                <td className="py-1.5 text-right font-mono text-ink font-semibold">99,84%</td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Collegio completo 11–15 (soglia ≥98%)</td>
                <td className="py-1.5 text-right font-mono text-ink font-semibold">98,85%</td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Relatore XML vs SPARQL (22.426 pron.)</td>
                <td className="py-1.5 text-right font-mono">97,12% (635/645 = 2 refusi)</td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">
                  Collegio vs sedute SPARQL ({sedute.anni[0]}–{sedute.anni[1]}, {fmtInt(sedute.pronunce)} pron.)
                </td>
                <td className="py-1.5 text-right font-mono">
                  {fmtPct(sedute.quota_collegio_presente_in_seduta)} in seduta ·{' '}
                  {fmtPct(sedute.quota_seduta_presente_in_collegio)} in collegio
                </td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Elenchi identici / collegio sottoinsieme seduta</td>
                <td className="py-1.5 text-right font-mono">
                  {fmtPct(sedute.pronunce_identiche)} / {fmtPct(sedute.collegio_sottoinsieme_seduta)}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Topic LDA & Parametri Costituzionali */}
      <SubHeader id="materia" title="Classificazione della materia: 20 temi LDA e parametri costituzionali" badge="descrittivo" />
      <div className="prose-editorial text-sm">
        <p>
          La materia di base è stimata con LDA su 46.126 massime (&gt;50 caratteri, vocabolario
          8.000 parole). Tra <em>k</em> ∈ {'{'}10, 20, 30, 40, 50, 60{'}'}, il picco di coerenza
          NPMI è a <strong>k = {topics.k}</strong> ({fmtDec(topics.coherence[String(topics.k)], 4)}).
          L&apos;accordo NMI è {fmtDec(topics.nmi_title, 3)} con i titoli delle massime dal 2015 e{' '}
          {fmtDec(topics.nmi_art, 3)} con l&apos;articolo costituzionale principale; la stabilità tra
          4 semi alternativi (Jaccard top 20) è bassa ({fmtDec(meanStab, 3)}). Restano senza materia{' '}
          {fmtInt(numbers.pronunce_without_topic)} pronunce ({fmtInt(numbers.without_topic_short_massime)}{' '}
          massime di rinvio ≤50 caratteri, {fmtInt(numbers.without_topic_no_massime)} senza massime
          di cui {fmtInt(numbers.without_topic_no_massime_2026)} del 2026). Come controllo fine, sono
          stati estratti gli articoli della Costituzione invocati nelle massime (
          <code className="font-mono text-xs">parametri.json</code>): {fmtInt(parametri.pronunce_with_article)}{' '}
          pronunce ({fmtPct(parametri.pronunce_with_massime_and_article_share)} di quelle con
          massime), {parametri.distinct_articles} articoli distinti, media{' '}
          {fmtDec(parametri.mean_articles_per_pronuncia, 2)} articoli/pronuncia.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 my-4">
        <div className="lg:col-span-2 bg-white border border-rule rounded-sm p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono uppercase tracking-wider text-muted">
              I 20 temi LDA (etichetta per lift dal 2015 e parole chiave)
            </span>
            <TabButton active={showAllTopics} onClick={() => setShowAllTopics(!showAllTopics)}>
              {showAllTopics ? 'Mostra primi 10' : 'Mostra tutti i 20'}
            </TabButton>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-rule text-left text-muted font-mono">
                  <th className="py-1.5 pr-2">ID</th>
                  <th className="py-1.5 pr-2">Etichetta (lift ≥15 mass., ≥10%)</th>
                  <th className="py-1.5 pr-2">Prime parole</th>
                  <th className="py-1.5 text-right">Lift</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100">
                {visibleTopics.map((id) => {
                  const det = topics.label_details[id];
                  return (
                    <tr key={id}>
                      <td className="py-1.5 pr-2 font-mono text-muted">{id}</td>
                      <td className="py-1.5 pr-2 font-medium text-ink">
                        {det.label || <span className="text-zinc-400 italic">senza etichetta</span>}
                      </td>
                      <td className="py-1.5 pr-2 text-zinc-600">
                        {topics.top_words[id].slice(0, 6).join(', ')}
                      </td>
                      <td className="py-1.5 text-right font-mono tabular-nums">
                        {det.lift > 0 ? fmtDec(det.lift, 1) : '—'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-white border border-rule rounded-sm p-4">
          <div className="text-xs font-mono uppercase tracking-wider text-muted mb-2">
            Top 10 articoli Costituzione invocati
          </div>
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-rule text-left text-muted font-mono">
                <th className="py-1.5">Art.</th>
                <th className="py-1.5 text-right">Quota pronunce</th>
                <th className="py-1.5 text-right">Principale (n)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100">
              {Object.entries(parametri.share_invoking_top).map(([art, share]) => (
                <tr key={art}>
                  <td className="py-1.5 font-mono font-medium text-ink">Art. {art}</td>
                  <td className="py-1.5 text-right font-mono tabular-nums">{fmtPct(share, 1)}</td>
                  <td className="py-1.5 text-right font-mono tabular-nums text-muted">
                    {parametri.main_article_top[art] ? fmtInt(parametri.main_article_top[art]) : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="mt-3 pt-2 border-t border-zinc-100 text-[11px] text-muted">
            Coerenza NPMI per k: {Object.entries(topics.coherence).map(([k, v]) => `${k}→${fmtDec(v, 3)}`).join(' · ')}
          </div>
        </div>
      </div>

      {/* Tabella preregistrazione */}
      <SubHeader id="prereg" title="Preregistrazione: deciso prima vs cambiato dopo" />
      <div className="overflow-x-auto bg-white border border-rule rounded-sm my-3">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-rule bg-zinc-50 text-left font-mono text-muted">
              <th className="p-2.5">Parte</th>
              <th className="p-2.5">Fissato prima</th>
              <th className="p-2.5">Cambiato o aggiunto dopo</th>
              <th className="p-2.5">Statuto</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100">
            {preregRows.map(([part, before, after, badge]) => (
              <tr key={part}>
                <td className="p-2.5 font-medium text-ink align-top">{part}</td>
                <td className="p-2.5 text-zinc-700 align-top">{before}</td>
                <td className="p-2.5 text-zinc-700 align-top">{after}</td>
                <td className="p-2.5 align-top">
                  <Badge type={badge} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
