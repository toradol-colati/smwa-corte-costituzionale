import React, { useState } from 'react';
import { Badge, FigureBox, SectionHeader, StaticPngFigure, SubHeader, TabButton } from './UI';
import { AbsencesBarChart, ForestPlotD3 } from './Charts';
import { fmtCI, fmtDec, fmtInt, fmtP, fmtPct } from '../utils/format';

export function SectionD3({ data }) {
  const [figMode, setFigMode] = useState('interactive'); // 'interactive' | 'png'
  const { d3, d3Abs, d3Full, numbers } = data;
  const sat = d3.primary.coef.sat_not_drafted;
  const selfD = d3.primary.coef.self_drafted;
  const selfNorm = d3.variants['controllo per norma impugnata in comune (esplorativo)'].coef.self_drafted;
  const selfParam = d3.variants['materia fine: parametri costituzionali (esplorativo)'].coef.self_drafted;

  const fullCheckRows = [
    { label: '0. Modello completo base', obj: d3Full.baseline },
    { label: '1. Classi età trimestrali (primi 2 anni)', obj: d3Full.v1_fine_young_ages },
    { label: '2a. Citanti fino al 2000', obj: d3Full.v2_period['fino al 2000'] },
    { label: '2b. Citanti dal 2001', obj: d3Full.v2_period['dal 2001'] },
    { label: '3a. Solo sentenze che citano', obj: d3Full.v3_type.sentenze },
    { label: '3b. Solo ordinanze che citano', obj: d3Full.v3_type.ordinanze },
    { label: '4. Norma impugnata + parametri cost.', obj: d3Full.v4_norme_param },
    { label: '5a. Campione controlli (seed +1)', obj: d3Full.v5_seeds['seed+1'] },
    { label: '5b. Campione controlli (seed +2)', obj: d3Full.v5_seeds['seed+2'] },
  ];

  return (
    <section>
      <SectionHeader
        id="d3"
        num="2"
        title="D3 — Memoria collegiale: aver partecipato non conta, aver scritto sì"
        subtitle="Regressione logistica condizionata esatta (strato = pronuncia che cita, 50 controlli casuali, errori standard raggruppati per redattore)."
        badge="principale"
      />

      <div className="prose-editorial text-sm">
        <p>
          L&apos;endpoint primario del progetto confronta, dentro ciascuna delle{' '}
          <strong>{fmtInt(d3.primary.strata)} pronunce</strong> che citano (redatte da{' '}
          {d3.primary.clusters} giudici; {fmtInt(d3.primary.cases)} citazioni, di cui{' '}
          {fmtInt(d3.primary.cases_absent)} a precedenti decisi in assenza del redattore), la
          probabilità di citare un precedente deciso da un collegio in cui il redattore sedeva senza
          averlo scritto rispetto a un precedente dello stesso periodo deciso in sua assenza. L&apos;odds
          ratio è <strong>{fmtDec(sat.or)}</strong> (IC 95%: {fmtCI(sat.lo, sat.hi)}, <em>p</em> ={' '}
          {fmtP(sat.p)}): i dati escludono effetti superiori al +9% o inferiori all&apos;−8%. La
          sensibilità su cinque semi indipendenti di campionamento dei controlli resta tra{' '}
          {fmtDec(Math.min(...d3.seed_sensitivity_or))} e {fmtDec(Math.max(...d3.seed_sensitivity_or))}.
        </p>
        <p>
          Al contrario, un precedente redatto dallo stesso giudice ha un odds ratio di{' '}
          <strong>{fmtDec(selfD.or)}</strong> (IC 95%: {fmtCI(selfD.lo, selfD.hi)},{' '}
          <em>esplorativo</em>). Il {fmtPct(d3.norme_descrittive.self_drafted.cases_same_article)}{' '}
          di queste citazioni condivide esattamente la stessa disposizione impugnata, contro il{' '}
          {fmtPct(d3.norme_descrittive.sat_not_drafted.cases_same_article)} per i precedenti in cui
          sedeva nel collegio e il {fmtPct(d3.norme_descrittive.absent.cases_same_article)} per
          quelli decisi in assenza. Controllando per norma impugnata in comune, l&apos;effetto scende
          a <strong>{fmtDec(selfNorm.or)}</strong> ({fmtCI(selfNorm.lo, selfNorm.hi)}): una riduzione
          del {fmtPct(numbers.d3_self_drafted_scale.excess_reduction, 0)} sull&apos;eccesso sopra 1
          ({fmtPct(numbers.d3_self_drafted_scale.log_reduction, 0)} su scala logaritmica). Con i
          soli parametri costituzionali scende a {fmtDec(selfParam.or)} ({fmtCI(selfParam.lo, selfParam.hi)}).
        </p>
      </div>

      <FigureBox
        num="Figure 7–8 (D3)"
        title="Effetto di collegio su tutte le 15 specificazioni e contrasto con l'auto-redazione"
        caption="Modello principale (rosso) e prove di robustezza/sottogruppi (grigio/blu). L'asterisco (*) indica la mancata convergenza della sola classe 10–15 anni nelle ordinanze (zero casi su 121 controlli), senza impatto sui coefficienti principali."
        source="reports/d3_results.json · fig7_d3_memoria_collegiale.png · fig8_d3_redatto_vs_collegio.png"
        controls={
          <>
            <TabButton active={figMode === 'interactive'} onClick={() => setFigMode('interactive')}>
              Interattivo (JSON)
            </TabButton>
            <TabButton active={figMode === 'png'} onClick={() => setFigMode('png')}>
              Figure originali (PNG)
            </TabButton>
          </>
        }
      >
        {figMode === 'interactive' ? (
          <ForestPlotD3 d3={d3} />
        ) : (
          <div className="space-y-4">
            <StaticPngFigure
              src="./figures/fig7_d3_memoria_collegiale.png"
              alt="D3 memoria collegiale - forest plot"
            />
            <StaticPngFigure
              src="./figures/fig8_d3_redatto_vs_collegio.png"
              alt="D3 redatto vs collegio"
            />
          </div>
        )}
      </FigureBox>

      {/* Diagnostica assenze */}
      <SubHeader id="assenze" title="Diagnostica delle assenze dal collegio" badge="descrittivo" />
      <div className="prose-editorial text-sm">
        <p>
          Poiché l&apos;identificazione del risultato principale poggia sulle assenze (tasso globale{' '}
          <strong>{fmtPct(d3Abs.absence_rate)}</strong> su {fmtInt(d3Abs.pairs)} coppie
          giudice–pronuncia in attività), sono state verificate distribuzione, bilanciamento e
          concentrazione. La dipendenza da tipo di giudizio, articolo costituzionale e tema è minima
          (V di Cramér ≤ {fmtDec(d3Abs.by.decade.cramers_v, 3)}). Solo lo{' '}
          {fmtPct(d3Abs.collegio_quality.absent.share_collegio_under_11)} dei precedenti in assenza
          ha collegi con meno di 11 giudici riconosciuti; {d3Abs.spread_by_drafter.drafters_with_absent_cases}{' '}
          su {d3Abs.spread_by_drafter.drafters} redattori citano almeno un precedente deciso in
          assenza (i primi 5 raccolgono il {fmtPct(d3Abs.spread_by_drafter.top5_share_absent_cases, 1)}).
        </p>
      </div>

      <FigureBox
        num="Diagnostica D3.1"
        title="Tasso di assenza per decennio, tipo di giudizio, parametro costituzionale e tema"
        caption="Barre da zero; la linea tratteggiata rossa indica la media globale del 6,3%."
        source="reports/d3_absences.json"
      >
        <AbsencesBarChart d3Abs={d3Abs} />
      </FigureBox>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 my-4">
        <div className="bg-white border border-rule rounded-sm p-4">
          <div className="text-xs font-mono uppercase tracking-wider text-muted mb-2">
            Bilanciamento covariate nei controlli (max |SMD| = {fmtDec(d3Abs.balance.max_abs_smd, 3)})
          </div>
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-rule text-left font-mono text-muted">
                <th className="py-1.5">Covariata</th>
                <th className="py-1.5 text-right">Presente</th>
                <th className="py-1.5 text-right">Assente</th>
                <th className="py-1.5 text-right">SMD</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100">
              {Object.entries(d3Abs.balance.covariates).map(([k, c]) => (
                <tr key={k}>
                  <td className="py-1.5 text-zinc-700">{c.label}</td>
                  <td className="py-1.5 text-right font-mono tabular-nums">
                    {k === 'cited_year' ? fmtDec(c.mean_present, 1) : fmtDec(c.mean_present, 3)}
                  </td>
                  <td className="py-1.5 text-right font-mono tabular-nums">
                    {k === 'cited_year' ? fmtDec(c.mean_absent, 1) : fmtDec(c.mean_absent, 3)}
                  </td>
                  <td className="py-1.5 text-right font-mono tabular-nums">{fmtDec(c.smd, 3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="bg-white border border-rule rounded-sm p-4">
          <div className="text-xs font-mono uppercase tracking-wider text-muted mb-2">
            Distribuzione della dimensione del collegio riconosciuto
          </div>
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-rule text-left font-mono text-muted">
                <th className="py-1.5">Giudici nel collegio</th>
                <th className="py-1.5 text-right">Pronunce</th>
                <th className="py-1.5 text-right">Quota</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100">
              {Object.entries(d3Abs.collegio_size.distribution).map(([sz, n]) => (
                <tr key={sz}>
                  <td className="py-1.5 font-mono">
                    {sz} {Number(sz) < 11 ? <span className="text-amber-700">(sotto quorum)</span> : ''}
                  </td>
                  <td className="py-1.5 text-right font-mono tabular-nums">{fmtInt(n)}</td>
                  <td className="py-1.5 text-right font-mono tabular-nums">
                    {fmtPct(n / data.network.nodes, 2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Controllo 0,88 nel modello completo */}
      <SubHeader id="d3-full" title="Secondo confronto (modello completo) e spiegazione dello 0,88" badge="esplorativo" />
      <div className="prose-editorial text-sm">
        <p>
          Confrontando i precedenti decisi durante il mandato con quelli di pari età decisi prima
          dell&apos;arrivo del giudice ({fmtInt(d3Full.baseline.strata)} strati,{' '}
          {fmtInt(d3Full.baseline.cases)} citazioni), i primi risultano citati meno sia da presenti (
          <strong>{fmtDec(d3Full.baseline.sat_not_drafted.or)}</strong>;{' '}
          {fmtCI(d3Full.baseline.sat_not_drafted.lo, d3Full.baseline.sat_not_drafted.hi)}) sia da
          assenti (<strong>{fmtDec(d3Full.baseline.in_mandate_absent.or)}</strong>;{' '}
          {fmtCI(d3Full.baseline.in_mandate_absent.lo, d3Full.baseline.in_mandate_absent.hi)}), con
          rapporto presente/assente pari a{' '}
          <strong>{fmtDec(d3Full.baseline.ratio_present_absent.or)}</strong>. Le cinque prove
          preregistrate mostrano che lo 0,88 non dipende dalla granularità dell&apos;età (0,87 con
          classi trimestrali), ma scompare controllando per norma impugnata e parametri
          costituzionali (sale a <strong>{fmtDec(d3Full.v4_norme_param.sat_not_drafted.or)}</strong>,
          sopra la soglia decisionale di {fmtDec(d3Full.half_threshold, 3)}).
        </p>
      </div>

      <div className="overflow-x-auto bg-white border border-rule rounded-sm my-3">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-rule bg-zinc-50 text-left font-mono text-muted">
              <th className="p-2.5">Specificazione (modello completo)</th>
              <th className="p-2.5 text-right">Presente (IC 95%)</th>
              <th className="p-2.5 text-right">Assente (IC 95%)</th>
              <th className="p-2.5 text-right">Rapporto Pres/Ass</th>
              <th className="p-2.5 text-right">≥ 0,935?</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100">
            {fullCheckRows.map(({ label, obj }) => (
              <tr key={label} className={obj.reaches_half ? 'bg-blue-50/30' : ''}>
                <td className="p-2.5 font-medium text-ink">{label}</td>
                <td className="p-2.5 text-right font-mono tabular-nums">
                  {fmtDec(obj.sat_not_drafted.or)} ({fmtCI(obj.sat_not_drafted.lo, obj.sat_not_drafted.hi)})
                </td>
                <td className="p-2.5 text-right font-mono tabular-nums">
                  {fmtDec(obj.in_mandate_absent.or)} ({fmtCI(obj.in_mandate_absent.lo, obj.in_mandate_absent.hi)})
                </td>
                <td className="p-2.5 text-right font-mono tabular-nums">
                  {fmtDec(obj.ratio_present_absent.or)} ({fmtCI(obj.ratio_present_absent.lo, obj.ratio_present_absent.hi)})
                </td>
                <td className="p-2.5 text-right font-mono">
                  {obj.reaches_half ? 'sì' : 'no'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
