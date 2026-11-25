import React, { useState } from 'react';
import { Badge, FigureBox, SectionHeader, StaticPngFigure, SubHeader, TabButton } from './UI';
import { AgeingSurvivalChart, ConcentrationBarChart, DecadeOutChart } from './Charts';
import { fmtCI, fmtDec, fmtInt, fmtP, fmtPct, fmtPctCI, fmtPid } from '../utils/format';

export function SectionD1({ data }) {
  const [concView, setConcView] = useState('interactive');
  const [ageView, setAgeView] = useState('interactive');
  const [showTop20, setShowTop20] = useState(false);

  const { network, d1, extras, succession } = data;
  const cY = d1.concentration;
  const cT = d1.concentration_by_type;

  return (
    <section>
      <SectionHeader
        id="d1"
        num="3"
        title="D1 & D1b — Gerarchia dei precedenti, durata e sostituzione"
        subtitle="Concentrazione rispetto ai modelli nulli, test legge di potenza vs lognormale, replica di Agnoloni & Pagallo (2016), invecchiamento e passaggio di testimone."
        badge="secondario"
      />

      {/* Base rete */}
      <div className="prose-editorial text-sm">
        <p>
          La rete delle citazioni (<strong>{fmtInt(network.nodes)} nodi</strong>,{' '}
          <strong>{fmtInt(network.edges)} archi diretti</strong>, aciclica) ha densità verso il
          passato pari a {fmtDec(network.density_backward * 100, 3)}% e una componente debolmente
          connessa che copre l&apos;{fmtPct(network.wcc_largest_share)} delle pronunce (
          {fmtInt(network.isolates)} isolate). Le sentenze ricevono in media{' '}
          {fmtDec(network.by_type.S.in_mean, 1)} citazioni contro{' '}
          {fmtDec(network.by_type.O.in_mean, 1)} delle ordinanze; la catena più lunga conta{' '}
          {network.dag_longest_path} anelli e l&apos;età mediana delle citazioni è{' '}
          {fmtDec(network.citation_age_median, 2)} anni (solo il {fmtPct(network.share_age_over20)}{' '}
          supera i 20 anni).
        </p>
      </div>

      {/* Concentrazione: Tabella + Figura 4 */}
      <div className="overflow-x-auto bg-white border border-rule rounded-sm my-4">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-rule bg-zinc-50 text-left font-mono text-muted">
              <th className="p-2.5">Misura di concentrazione</th>
              <th className="p-2.5 text-right">Osservato</th>
              <th className="p-2.5 text-right">Nullo stesso anno (95%)</th>
              <th className="p-2.5 text-right">Nullo anno + tipo (95%)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100 font-mono tabular-nums">
            <tr>
              <td className="p-2.5 font-sans text-ink">Quota citazioni all&apos;1% più citato</td>
              <td className="p-2.5 text-right font-semibold text-primary">{fmtPct(cY.top1_share.observed)}</td>
              <td className="p-2.5 text-right text-muted">
                {fmtPct(cY.top1_share.null_mean)} ({fmtPctCI(cY.top1_share.null_lo, cY.top1_share.null_hi)})
              </td>
              <td className="p-2.5 text-right text-muted">
                {fmtPct(cT.top1_share.null_mean)} ({fmtPctCI(cT.top1_share.null_lo, cT.top1_share.null_hi)})
              </td>
            </tr>
            <tr>
              <td className="p-2.5 font-sans text-ink">Indice di Gini</td>
              <td className="p-2.5 text-right font-semibold text-primary">{fmtDec(cY.gini.observed)}</td>
              <td className="p-2.5 text-right text-muted">
                {fmtDec(cY.gini.null_mean)} ({fmtCI(cY.gini.null_lo, cY.gini.null_hi)})
              </td>
              <td className="p-2.5 text-right text-muted">
                {fmtDec(cT.gini.null_mean)} ({fmtCI(cT.gini.null_lo, cT.gini.null_hi)})
              </td>
            </tr>
            <tr>
              <td className="p-2.5 font-sans text-ink">Pronunce mai citate (sent. {fmtPct(cT.observed_by_type.never_cited_sentenze)} · ord. {fmtPct(cT.observed_by_type.never_cited_ordinanze)})</td>
              <td className="p-2.5 text-right font-semibold text-primary">{fmtPct(cY.never_cited.observed)}</td>
              <td className="p-2.5 text-right text-muted">
                {fmtPct(cY.never_cited.null_mean)} ({fmtPctCI(cY.never_cited.null_lo, cY.never_cited.null_hi)})
              </td>
              <td className="p-2.5 text-right text-muted">
                {fmtPct(cT.never_cited.null_mean)} ({fmtPctCI(cT.never_cited.null_lo, cT.never_cited.null_hi)})
              </td>
            </tr>
            <tr>
              <td className="p-2.5 font-sans text-ink">Massimo citazioni ricevute</td>
              <td className="p-2.5 text-right font-semibold text-primary">{fmtInt(cY.max.observed)}</td>
              <td className="p-2.5 text-right text-muted">
                {fmtDec(cY.max.null_mean, 1)} ({fmtInt(cY.max.null_lo)}–{fmtInt(cY.max.null_hi)})
              </td>
              <td className="p-2.5 text-right text-muted">
                {fmtDec(cT.max.null_mean, 1)} ({fmtInt(cT.max.null_lo)}–{fmtInt(cT.max.null_hi)})
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <FigureBox
        num="Figure 3–4 (D1)"
        title="Concentrazione delle citazioni rispetto ai modelli nulli e coda della distribuzione"
        caption="Confronto tra dato osservato e 1.000 repliche nulle. Il test di Clauset–Shalizi–Newman sulla coda (da xmin = 10, n = 2.807) preferisce la lognormale alla legge di potenza (R = −7,55, p < 0,001)."
        source="reports/d1_results.json · fig3_distribuzione_citazioni.png · fig4_concentrazione_vs_nullo.png"
        controls={
          <>
            <TabButton active={concView === 'interactive'} onClick={() => setConcView('interactive')}>
              Barre interattive
            </TabButton>
            <TabButton active={concView === 'png'} onClick={() => setConcView('png')}>
              Figure 3 &amp; 4 (PNG)
            </TabButton>
          </>
        }
      >
        {concView === 'interactive' ? (
          <ConcentrationBarChart d1={d1} />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <StaticPngFigure src="./figures/fig3_distribuzione_citazioni.png" alt="Distribuzione citazioni" />
            <StaticPngFigure src="./figures/fig4_concentrazione_vs_nullo.png" alt="Concentrazione vs nullo" />
          </div>
        )}
      </FigureBox>

      {/* Evoluzione per decennio e Top 20 */}
      <FigureBox
        num="Evoluzione storica"
        title="Numero medio di citazioni fatte per pronuncia, per decennio (1950–2020)"
        caption="La densità di richiami cresce di quattordici volte tra gli anni Cinquanta (1,0) e gli anni Venti (14,7)."
        source="reports/network_basic.json"
        controls={
          <TabButton active={showTop20} onClick={() => setShowTop20(!showTop20)}>
            {showTop20 ? 'Nascondi Top 20 pronunce' : 'Mostra Top 20 pronunce più citate'}
          </TabButton>
        }
      >
        <DecadeOutChart byDecade={network.by_decade_out} />
        {showTop20 && (
          <div className="mt-4 pt-3 border-t border-zinc-100 grid grid-cols-2 sm:grid-cols-4 md:grid-cols-5 gap-2 text-xs font-mono">
            {network.top20_cited.map((p, idx) => (
              <div key={p.pid} className="p-2 bg-paper border border-rule rounded-sm flex justify-between">
                <span>
                  {idx + 1}. {p.tipo === 'S' ? 'sent.' : 'ord.'} {fmtPid(p.pid)}
                </span>
                <strong className="text-primary">{p.in_deg}</strong>
              </div>
            ))}
          </div>
        )}
      </FigureBox>

      {/* HITS, PageRank e Replica Agnoloni & Pagallo */}
      <SubHeader id="hits" title="Autorevolezza (HITS), PageRank e replica di Agnoloni & Pagallo (2016)" badge="esplorativo" />
      <div className="prose-editorial text-sm">
        <p>
          Sulla rete completa, l&apos;1% più autorevole secondo HITS e l&apos;1% più citato
          condividono il <strong>{fmtPct(d1.rete_completa.top1_overlap)}</strong> delle pronunce,
          contro il {fmtPct(d1.rete_completa.top1_overlap_null.mean)} atteso sotto scambi alla Uzzi.
          Il controllo per comunità (<code className="font-mono text-xs">extras.json</code>) mostra
          che questo non prova che &laquo;conta chi ti cita&raquo;: il{' '}
          <strong>{fmtPct(extras.hits_communities.authority_hits.top1_share_largest_community)}</strong>{' '}
          del top 1% HITS cade in un unico filone (comunità 0,{' '}
          {fmtInt(extras.hits_communities.authority_hits.largest_community_size)} pronunce, anno
          mediano {extras.hits_communities.authority_hits.largest_community_median_year}, che
          concentra il {fmtPct(extras.hits_communities.authority_mass_in_largest_community)} della
          massa di authority), mentre il top 1% per citazioni è distribuito su{' '}
          {extras.hits_communities.citazioni.communities_in_top1} filoni. Inoltre il{' '}
          {fmtPct(d1.rete_completa.share_auth_zero)} delle pronunce ha authority pari a zero.
          PageRank fa l&apos;opposto e premia le pronunce antiche (anno mediano top 1%:{' '}
          {extras.hits_communities.pagerank.median_year_top1}).
        </p>
        <p>
          Sul perimetro di Agnoloni e Pagallo (sentenze in via incidentale fino al 2014:{' '}
          {fmtInt(d1.replica_agnoloni_pagallo.nodes)} nodi), solo{' '}
          <strong>{d1.replica_agnoloni_pagallo.top30_auth_in_top30_cited} su 30</strong> delle prime
          pronunce per HITS sono tra le prime 30 per citazioni. Nel test predittivo out-of-sample
          (stima ≤2010, prova 2011–2025), aggiungere l&apos;authority HITS{' '}
          <strong>peggiora</strong> la devianza del{' '}
          {fmtPct(Math.abs(d1.prediction.reduction), 2)} (IC 95%:{' '}
          {fmtPctCI(Math.abs(d1.prediction.reduction_hi), Math.abs(d1.prediction.reduction_lo), 2)}
          ), mancando il criterio preregistrato (riduzione ≥2%).
        </p>
      </div>

      <FigureBox
        num="Figura 6 (D1)"
        title="Sovrapposizione anno per anno tra l'1% più autorevole (HITS) e l'1% più citato"
        caption="Serie storica dal 1966 (soglia di 1.000 pronunce) al 2026; a destra il punto grigio mostra l'intervallo atteso sotto scambi alla Uzzi sulla rete 2026."
        source="reports/d1_results.json · fig6_authority_vs_citazioni.png"
      >
        <StaticPngFigure
          src="./figures/fig6_authority_vs_citazioni.png"
          alt="Autorevolezza HITS vs citazioni"
        />
      </FigureBox>

      {/* D1b: Invecchiamento e Sostituzione */}
      <SubHeader id="d1b" title="D1b — Durata e sostituzione dei precedenti" badge="secondario" />
      <FigureBox
        num="Figura 5 (D1b)"
        title="Frequenza di citazione relativa per età e sopravvivenza Kaplan–Meier"
        caption="Picco a 1 anno (5,76×), dimezzamento in 3 anni, discesa sotto la scelta uniforme dopo 9 anni. Mediana Kaplan–Meier: 6 anni (19 sentenze, 1 ordinanza); il 13,4% delle pronunce con almeno 30 anni resta citato."
        source="reports/d1_results.json · fig5_invecchiamento.png"
        controls={
          <>
            <TabButton active={ageView === 'interactive'} onClick={() => setAgeView('interactive')}>
              Interattivo (61 punti / KM)
            </TabButton>
            <TabButton active={ageView === 'png'} onClick={() => setAgeView('png')}>
              Figura 5 (PNG)
            </TabButton>
          </>
        }
      >
        {ageView === 'interactive' ? (
          <AgeingSurvivalChart d1={d1} />
        ) : (
          <StaticPngFigure src="./figures/fig5_invecchiamento.png" alt="Curva invecchiamento" />
        )}
      </FigureBox>

      <div className="bg-white border border-rule rounded-sm p-4 my-4 text-sm">
        <div className="flex items-center gap-2 mb-2">
          <span className="font-semibold text-ink">Verifica della sostituzione dei precedenti</span>
          <Badge type="esplorativo" />
        </div>
        <p className="text-zinc-700 leading-relaxed mb-3">
          Su <strong>{fmtInt(succession.precedents)} precedenti</strong> (1970–2010, ≥5 citazioni
          entro 4 anni), le citazioni medie per fascia d&apos;età decadono da{' '}
          {fmtDec(succession.p_citations_by_age['0-3'])} (0–3 anni) a{' '}
          {fmtDec(succession.p_citations_by_age['4-7'])} (4–7),{' '}
          {fmtDec(succession.p_citations_by_age['8-11'])} (8–11) e{' '}
          {fmtDec(succession.p_citations_by_age['12-15'])} (12–15). Nella finestra 4–15 anni
          (escludendo chi cita ancora il precedente), i {fmtInt(succession.successors)} successori
          ricevono in media <strong>{fmtDec(succession.later_window.successors_mean, 1)}</strong>{' '}
          citazioni contro <strong>{fmtDec(succession.later_window.controls_mean, 1)}</strong> dei
          controlli appaiati (stesso anno, tipo, tema) e{' '}
          {fmtDec(succession.later_window.p_itself_mean, 1)} del precedente: rapporto{' '}
          <strong>{fmtDec(succession.later_window.ratio_successors_controls)}</strong> (IC 95%:{' '}
          {fmtCI(succession.later_window.ratio_lo, succession.later_window.ratio_hi)}). Verdetto
          secondo regola preregistrata: <strong>{succession.reading.verdict}</strong>, con la
          cautela che i dati non separano il passaggio di testimone dall&apos;importanza intrinseca
          dei successori.
        </p>
      </div>
    </section>
  );
}
