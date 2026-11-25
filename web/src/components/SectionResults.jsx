import React, { useState } from 'react';
import { ScientificFigure, ScientificTable, SectionTitle, SubTitle, SwitchBtn } from './UI';
import {
  AbsencesBarChart,
  AgeingSurvivalChart,
  ConcentrationBarChart,
  CourtsDecadeChart,
  D2JudgeChart,
  ForestPlotD3,
} from './Charts';
import { fmtCI, fmtDec, fmtInt, fmtP, fmtPct, fmtPctCI, fmtPid } from '../utils/format';

const D2_SPECS = [
  { key: 'permutazione_anno', label: 'Anno', strataKey: 'anno' },
  { key: 'permutazione_anno_tipo', label: 'Anno + Tipo', strataKey: 'anno_tipo' },
  { key: 'permutazione_anno_tipo_materia', label: 'Anno + Tipo + Materia', strataKey: 'anno_tipo_materia' },
  { key: 'permutazione_anno_tipo_parametro', label: 'Anno + Tipo + Parametro', strataKey: 'anno_tipo_parametro' },
  { key: 'permutazione_anno_dal_1987', label: 'Solo dal 1987', strataKey: null },
];

export function SectionResults({ data }) {
  const [d2SpecKey, setD2SpecKey] = useState('permutazione_anno');
  const {
    network,
    d1,
    d2,
    d2Strata,
    d3,
    d3Abs,
    d3Full,
    d4,
    succession,
    extras,
    course,
    cositting,
    polarity,
    courts,
    numbers,
  } = data;

  const sat = d3.primary.coef.sat_not_drafted;
  const selfD = d3.primary.coef.self_drafted;
  const selfNorm = d3.variants['controllo per norma impugnata in comune (esplorativo)'].coef.self_drafted;
  const selfParam = d3.variants['materia fine: parametri costituzionali (esplorativo)'].coef.self_drafted;

  const d2Spec = d2[d2SpecKey];
  const d2Meta = D2_SPECS.find((s) => s.key === d2SpecKey);
  const d2StrataInfo = d2Meta?.strataKey ? d2Strata[d2Meta.strataKey] : null;

  const fullRows = [
    ['0. Modello completo base', d3Full.baseline],
    ['1. Classi età trimestrali (primi 2 anni)', d3Full.v1_fine_young_ages],
    ['2a. Citanti fino al 2000', d3Full.v2_period['fino al 2000']],
    ['2b. Citanti dal 2001', d3Full.v2_period['dal 2001']],
    ['3a. Solo sentenze che citano', d3Full.v3_type.sentenze],
    ['3b. Solo ordinanze che citano', d3Full.v3_type.ordinanze],
    ['4. Norma impugnata + parametri cost.', d3Full.v4_norme_param],
    ['5a. Campione controlli (seed +1)', d3Full.v5_seeds['seed+1']],
    ['5b. Campione controlli (seed +2)', d3Full.v5_seeds['seed+2']],
  ];

  return (
    <section className="article-prose">
      <SectionTitle id="risultati" num="3" title="Risultati" />

      {/* 3.1 D3 */}
      <SubTitle
        id="risultati-d3"
        num="3.1"
        title="Endpoint primario: memoria collegiale e auto-redazione (D3)"
        status="principale"
      />
      <p>
        Nel modello principale ({fmtInt(d3.primary.strata)} pronunce che citano,{' '}
        {d3.primary.clusters} giudici, {fmtInt(d3.primary.cases)} citazioni, di cui{' '}
        {fmtInt(d3.primary.cases_absent)} a precedenti decisi in assenza del redattore), la
        partecipazione al collegio senza aver redatto il precedente presenta un odds ratio di{' '}
        <strong>{fmtDec(sat.or)}</strong> (IC 95%: {fmtCI(sat.lo, sat.hi)}; <em>p</em> ={' '}
        {fmtP(sat.p)}; Figura 3). La stima rimane compresa tra{' '}
        {fmtDec(Math.min(...d3.seed_sensitivity_or))} e{' '}
        {fmtDec(Math.max(...d3.seed_sensitivity_or))} su cinque campioni indipendenti di controlli e
        non si discosta da 1 in nessuna delle quattordici varianti di robustezza e sottogruppo
        (inclusa l&apos;esclusione delle autocitazioni: 0,99; sole pronunce dal 1987: 1,01; testo
        intero: 0,99; note delle massime: 0,99).
      </p>
      <p>
        Nello stesso modello, i precedenti redatti dallo stesso giudice presentano un odds ratio di{' '}
        <strong>{fmtDec(selfD.or)}</strong> (IC 95%: {fmtCI(selfD.lo, selfD.hi)}; <em>p</em> &lt;
        0,001; esplorativo), più elevato nelle ordinanze (9,83) rispetto alle sentenze (3,53) e fino
        al 2000 (8,74) rispetto al periodo successivo (3,64). Il{' '}
        {fmtPct(d3.norme_descrittive.self_drafted.cases_same_article)} dei precedenti auto-citati
        riguarda la stessa disposizione impugnata, contro il{' '}
        {fmtPct(d3.norme_descrittive.sat_not_drafted.cases_same_article)} dei precedenti decisi in
        collegio e il {fmtPct(d3.norme_descrittive.absent.cases_same_article)} di quelli decisi in
        assenza. Introducendo il controllo per disposizione impugnata in comune, l&apos;odds ratio
        dell&apos;auto-redazione scende a <strong>{fmtDec(selfNorm.or)}</strong> (
        {fmtCI(selfNorm.lo, selfNorm.hi)}, −{fmtPct(numbers.d3_self_drafted_scale.excess_reduction, 0)}{' '}
        sull&apos;eccesso sopra 1; −{fmtPct(numbers.d3_self_drafted_scale.log_reduction, 0)} su
        scala logaritmica), mentre con i soli parametri costituzionali scende a{' '}
        {fmtDec(selfParam.or)} ({fmtCI(selfParam.lo, selfParam.hi)}).
      </p>

      <ScientificFigure
        id="fig-3"
        label="Figura 3"
        caption="Odds ratio e intervalli di confidenza al 95% per la partecipazione al collegio (senza redazione) nel modello principale (rosso) e nelle quattordici varianti di robustezza, con vista alternativa di confronto rispetto all'auto-redazione su scala logaritmica. I dati provengono da reports/d3_results.json (corrispondenti alle Figure 7–8 della relazione)."
      >
        <ForestPlotD3 d3={d3} />
      </ScientificFigure>

      <p>
        Su {fmtInt(d3Abs.pairs)} coppie giudice–pronuncia in attività, il tasso medio di assenza dal
        collegio è del <strong>{fmtPct(d3Abs.absence_rate)}</strong> (Figura 4). La dipendenza da
        tipo di giudizio, articolo costituzionale e tema è contenuta (V di Cramér massima:{' '}
        {fmtDec(d3Abs.by.decade.cramers_v, 3)} per decennio, dal 3,4% negli anni 2020 al 7,2% negli
        anni 1980–1990). Nei controlli non citati, la massima differenza standardizzata (|SMD|) tra
        precedenti con giudice presente e assente è {fmtDec(d3Abs.balance.max_abs_smd, 3)} (età
        media {fmtDec(d3Abs.balance.covariates.age.mean_present)} vs{' '}
        {fmtDec(d3Abs.balance.covariates.age.mean_absent)} anni); solo lo{' '}
        {fmtPct(d3Abs.collegio_quality.absent.share_collegio_under_11)} dei precedenti in assenza
        presenta meno di 11 giudici riconosciuti.
      </p>

      <ScientificFigure
        id="fig-4"
        label="Figura 4"
        caption="Tasso di assenza dal collegio per decennio, tipo di giudizio, principali articoli costituzionali e 20 temi LDA (asse verticale da zero; linea tratteggiata rossa = media globale 6,3%; n = 327.252 coppie, reports/d3_absences.json)."
      >
        <AbsencesBarChart d3Abs={d3Abs} />
      </ScientificFigure>

      <p>
        Nel modello completo secondario ({fmtInt(d3Full.baseline.strata)} strati, riferimento =
        precedenti decisi prima dell&apos;ingresso in Corte), i precedenti decisi durante il mandato
        mostrano un odds ratio di {fmtDec(d3Full.baseline.sat_not_drafted.or)} (
        {fmtCI(d3Full.baseline.sat_not_drafted.lo, d3Full.baseline.sat_not_drafted.hi)}) se presenti
        e {fmtDec(d3Full.baseline.in_mandate_absent.or)} (
        {fmtCI(d3Full.baseline.in_mandate_absent.lo, d3Full.baseline.in_mandate_absent.hi)}) se
        assenti (rapporto presente/assente {fmtDec(d3Full.baseline.ratio_present_absent.or)};{' '}
        {fmtCI(
          d3Full.baseline.ratio_present_absent.lo,
          d3Full.baseline.ratio_present_absent.hi
        )}
        ). Come riportato in Tabella 4, la riduzione a 0,88 non si modifica con classi di età
        trimestrali (0,87), ma risale a {fmtDec(d3Full.v4_norme_param.sat_not_drafted.or)} (
        {fmtCI(d3Full.v4_norme_param.sat_not_drafted.lo, d3Full.v4_norme_param.sat_not_drafted.hi)})
        controllando congiuntamente per norma impugnata e parametri costituzionali.
      </p>

      <ScientificTable
        id="tab-4"
        label="Tabella 4"
        title="Controllo esplorativo dello 0,88 nel modello completo di D3 (soglia decisionale preregistrata ≥ 0,935)."
        note="Fonte: reports/d3_full_check.json. Tutti i modelli hanno raggiunto convergenza esatta."
      >
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-zinc-800 text-left font-mono text-muted">
              <th className="p-2">Specificazione</th>
              <th className="p-2 text-right">Presente (IC 95%)</th>
              <th className="p-2 text-right">Assente (IC 95%)</th>
              <th className="p-2 text-right">Rapporto Pres/Ass</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100 font-mono tabular-nums">
            {fullRows.map(([lbl, obj]) => (
              <tr key={lbl} className={obj.reaches_half ? 'bg-blue-50/30' : ''}>
                <td className="p-2 font-sans text-ink">{lbl}</td>
                <td className="p-2 text-right">
                  {fmtDec(obj.sat_not_drafted.or)} ({fmtCI(obj.sat_not_drafted.lo, obj.sat_not_drafted.hi)})
                </td>
                <td className="p-2 text-right">
                  {fmtDec(obj.in_mandate_absent.or)} ({fmtCI(obj.in_mandate_absent.lo, obj.in_mandate_absent.hi)})
                </td>
                <td className="p-2 text-right">
                  {fmtDec(obj.ratio_present_absent.or)} ({fmtCI(obj.ratio_present_absent.lo, obj.ratio_present_absent.hi)})
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </ScientificTable>

      {/* 3.2 D1 e D1b */}
      <SubTitle
        id="risultati-d1"
        num="3.2"
        title="Concentrazione, autorevolezza e durata dei precedenti (D1 e D1b)"
        status="secondario"
      />
      <p>
        La rete delle citazioni conta {fmtInt(network.nodes)} pronunce e {fmtInt(network.edges)}{' '}
        archi diretti (densità verso il passato {fmtDec(network.density_backward * 100, 3)}%,
        componente connessa principale {fmtPct(network.wcc_largest_share)}, {fmtInt(network.isolates)}{' '}
        nodi isolati, catena più lunga {network.dag_longest_path} anelli). Le citazioni medie in
        uscita passano da {fmtDec(network.by_decade_out['1950'], 1)} negli anni Cinquanta a{' '}
        {fmtDec(network.by_decade_out['2020'], 1)} negli anni Venti; le sentenze ricevono in media{' '}
        {fmtDec(network.by_type.S.in_mean, 1)} citazioni contro {fmtDec(network.by_type.O.in_mean, 1)}{' '}
        delle ordinanze. Tutte le metriche di concentrazione superano i valori attesi sia nel nullo
        per anno sia in quello per anno e tipo (Tabella 5 e Figura 5). Le tre pronunce più citate
        sono le sentenze 303/2003 (113), 401/2007 (111) e 383/2005 (99). Sulla coda (da{' '}
        <em>x_min</em> = {d1.tail.xmin}, <em>n</em> = {fmtInt(d1.tail.n_tail)}), il test di
        verosimiglianza preferisce la distribuzione lognormale alla legge di potenza (<em>R</em> ={' '}
        {fmtDec(d1.tail.vs_lognormal_R, 2)}, <em>p</em> &lt; 0,001; Figura 6).
      </p>

      <ScientificTable
        id="tab-5"
        label="Tabella 5"
        title="Misure di concentrazione delle citazioni ricevute confrontate con 1.000 repliche nulle."
        note="Tra parentesi l'intervallo 2,5°–97,5° percentile delle repliche nulle. Tutte le differenze presentano p = 0,001. Fonte: reports/d1_results.json."
      >
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-zinc-800 text-left font-mono text-muted">
              <th className="p-2">Misura</th>
              <th className="p-2 text-right">Osservato</th>
              <th className="p-2 text-right">Nullo stesso anno (95%)</th>
              <th className="p-2 text-right">Nullo anno e tipo (95%)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100 font-mono tabular-nums">
            <tr>
              <td className="p-2 font-sans text-ink">Quota citazioni all&apos;1% più citato</td>
              <td className="p-2 text-right font-semibold text-primary">
                {fmtPct(d1.concentration.top1_share.observed)}
              </td>
              <td className="p-2 text-right text-muted">
                {fmtPct(d1.concentration.top1_share.null_mean)} (
                {fmtPctCI(d1.concentration.top1_share.null_lo, d1.concentration.top1_share.null_hi)})
              </td>
              <td className="p-2 text-right text-muted">
                {fmtPct(d1.concentration_by_type.top1_share.null_mean)} (
                {fmtPctCI(
                  d1.concentration_by_type.top1_share.null_lo,
                  d1.concentration_by_type.top1_share.null_hi
                )}
                )
              </td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Indice di Gini</td>
              <td className="p-2 text-right font-semibold text-primary">
                {fmtDec(d1.concentration.gini.observed)}
              </td>
              <td className="p-2 text-right text-muted">
                {fmtDec(d1.concentration.gini.null_mean)} (
                {fmtCI(d1.concentration.gini.null_lo, d1.concentration.gini.null_hi)})
              </td>
              <td className="p-2 text-right text-muted">
                {fmtDec(d1.concentration_by_type.gini.null_mean)} (
                {fmtCI(d1.concentration_by_type.gini.null_lo, d1.concentration_by_type.gini.null_hi)})
              </td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Pronunce mai citate</td>
              <td className="p-2 text-right font-semibold text-primary">
                {fmtPct(d1.concentration.never_cited.observed)}
              </td>
              <td className="p-2 text-right text-muted">
                {fmtPct(d1.concentration.never_cited.null_mean)} (
                {fmtPctCI(d1.concentration.never_cited.null_lo, d1.concentration.never_cited.null_hi)})
              </td>
              <td className="p-2 text-right text-muted">
                {fmtPct(d1.concentration_by_type.never_cited.null_mean)} (
                {fmtPctCI(
                  d1.concentration_by_type.never_cited.null_lo,
                  d1.concentration_by_type.never_cited.null_hi
                )}
                )
              </td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Massimo citazioni ricevute</td>
              <td className="p-2 text-right font-semibold text-primary">
                {fmtInt(d1.concentration.max.observed)}
              </td>
              <td className="p-2 text-right text-muted">
                {fmtDec(d1.concentration.max.null_mean, 1)} ({fmtInt(d1.concentration.max.null_lo)}–
                {fmtInt(d1.concentration.max.null_hi)})
              </td>
              <td className="p-2 text-right text-muted">
                {fmtDec(d1.concentration_by_type.max.null_mean, 1)} (
                {fmtInt(d1.concentration_by_type.max.null_lo)}–
                {fmtInt(d1.concentration_by_type.max.null_hi)})
              </td>
            </tr>
          </tbody>
        </table>
      </ScientificTable>

      <ScientificFigure
        id="fig-5"
        label="Figura 5"
        caption="Confronto tra dato osservato (rosso) e media con intervallo al 95% delle repliche nulle (grigio) per le tre misure di concentrazione (assi verticali da zero; reports/d1_results.json)."
      >
        <ConcentrationBarChart d1={d1} />
      </ScientificFigure>

      <p>
        Sulla rete completa, l&apos;1% più autorevole secondo HITS e l&apos;1% più citato
        condividono il {fmtPct(d1.rete_completa.top1_overlap)} delle pronunce (atteso sotto scambi
        alla Uzzi: {fmtPct(d1.rete_completa.top1_overlap_null.mean)}; Figura 7). Il{' '}
        {fmtPct(extras.hits_communities.authority_hits.top1_share_largest_community)} del top 1%
        HITS ricade tuttavia in un&apos;unica comunità Leiden (comunità 0,{' '}
        {fmtInt(extras.hits_communities.authority_hits.largest_community_size)} nodi, anno mediano{' '}
        {extras.hits_communities.authority_hits.largest_community_median_year}, che raccoglie il{' '}
        {fmtPct(extras.hits_communities.authority_mass_in_largest_community)} dell&apos;authority
        totale), mentre il {fmtPct(d1.rete_completa.share_auth_zero)} delle pronunce ha authority
        zero. Sul perimetro di Agnoloni e Pagallo (sentenze incidentali ≤2014,{' '}
        {fmtInt(d1.replica_agnoloni_pagallo.nodes)} nodi), solo{' '}
        <strong>{d1.replica_agnoloni_pagallo.top30_auth_in_top30_cited} su 30</strong> delle prime
        pronunce per HITS coincidono con le prime 30 per citazioni. Nel modello predittivo
        out-of-sample (2011–2025), aggiungere l&apos;authority HITS aumenta la devianza dello{' '}
        {fmtPct(Math.abs(d1.prediction.reduction), 2)} (IC 95%:{' '}
        {fmtPctCI(Math.abs(d1.prediction.reduction_hi), Math.abs(d1.prediction.reduction_lo), 2)}),
        non raggiungendo la soglia preregistrata di riduzione ≥2%.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 my-6">
        <ScientificFigure
          id="fig-6"
          label="Figura 6"
          caption="Funzione di ripartizione complementare (CCDF) delle citazioni ricevute in scala bilogaritmica (reports/figures/fig3_distribuzione_citazioni.png)."
        >
          <img
            src="./figures/fig3_distribuzione_citazioni.png"
            alt="Distribuzione CCDF citazioni"
            loading="lazy"
            className="w-full h-auto"
          />
        </ScientificFigure>
        <ScientificFigure
          id="fig-7"
          label="Figura 7"
          caption="Sovrapposizione annuale (1966–2026) tra l'1% più autorevole secondo HITS e l'1% più citato; a destra il riferimento nullo a parità di citazioni sulla rete 2026 (fig6_authority_vs_citazioni.png)."
        >
          <img
            src="./figures/fig6_authority_vs_citazioni.png"
            alt="Sovrapposizione HITS vs citazioni nel tempo"
            loading="lazy"
            className="w-full h-auto"
          />
        </ScientificFigure>
      </div>

      <p>
        Per D1b, la frequenza relativa di citazione raggiunge il massimo a {d1.ageing.peak_age} anno
        dal deposito ({fmtDec(d1.ageing.relative_rate_by_age[1], 2)}× la scelta uniforme), si
        dimezza in {d1.ageing.half_life_after_peak} anni e scende sotto 1× dopo{' '}
        {d1.ageing.age_when_rate_below_1} anni (Figura 8). La mediana Kaplan–Meier fino
        all&apos;ultima citazione è {fmtDec(d1.survival.median, 0)} anni (19 per le sentenze, 1 per
        le ordinanze); il {fmtPct(d1.survival.share_cited_after_30y)} delle pronunce con almeno 30
        anni viene ancora citato. Nella verifica esplorativa sulla sostituzione (
        {fmtInt(succession.precedents)} precedenti del 1970–2010 con ≥5 citazioni entro 4 anni), i{' '}
        {fmtInt(succession.successors)} successori ricevono nella finestra 4–15 anni (escludendo chi
        cita ancora il precedente){' '}
        <strong>{fmtDec(succession.later_window.ratio_successors_controls)} volte</strong> (IC 95%:{' '}
        {fmtCI(succession.later_window.ratio_lo, succession.later_window.ratio_hi)}) le citazioni di
        controlli appaiati per anno, tipo e tema ({fmtDec(succession.later_window.successors_mean, 1)}{' '}
        vs {fmtDec(succession.later_window.controls_mean, 1)} citazioni medie).
      </p>

      <ScientificFigure
        id="fig-8"
        label="Figura 8"
        caption="Frequenza relativa di citazione per età del precedente (0–60 anni, scala verticale logaritmica) e curva di sopravvivenza Kaplan–Meier fino all'ultima citazione ricevuta (reports/d1_results.json)."
      >
        <AgeingSurvivalChart d1={d1} />
      </ScientificFigure>

      {/* 3.3 D2 e D4 */}
      <SubTitle
        id="risultati-d2"
        num="3.3"
        title="Singoli giudici e appartenenza a gruppi (D2 e D4)"
        status="esplorativo"
      />
      <p>
        Su {d2.permutazione_anno.judges_tested} giudici con almeno 30 pronunce ({fmtInt(d2.citations_used)}{' '}
        citazioni ricevute entro 10 anni da altri redattori), la variabilità complessiva dei
        rapporti osservati/attesi è {fmtDec(d2.permutazione_anno.var_ratio_to_null, 2)} volte quella
        attesa sotto permutazione annuale (<em>p</em> &lt; 0,001), ma dopo correzione di Holm solo{' '}
        <strong>{d2.permutazione_anno.sig_holm_above} giudici</strong> risultano sopra l&apos;atteso
        (primi tre: Baldassarre 1,88; Onida 1,61; De Siervo 1,48) e{' '}
        <strong>{d2.permutazione_anno.sig_holm_below}</strong> sotto (Figura 9; tabella completa
        in <a href="#appendici" className="ref-link">Appendice A</a>). Aggiungendo controlli più
        fini, i giudici significativi sopra/sotto scendono a 2/4 (anno e tipo), 1/3 (anno, tipo e
        materia) e 0/3 (anno, tipo e articolo costituzionale principale). La correlazione di
        Spearman tra mandato e dieci anni successivi (87 giudici usciti entro il 2015) è{' '}
        {fmtDec(d2.permutazione_anno.post_mandate.spearman_during_post)} contro{' '}
        {fmtDec(d2.permutazione_anno.post_mandate.spearman_null_mean)} attesa per anno, ma rientra
        nell&apos;intervallo nullo nel controllo per articolo costituzionale (
        {fmtDec(d2.permutazione_anno_tipo_parametro.post_mandate.spearman_during_post)} vs{' '}
        {fmtDec(d2.permutazione_anno_tipo_parametro.post_mandate.spearman_null_mean)},{' '}
        {fmtCI(
          d2.permutazione_anno_tipo_parametro.post_mandate.spearman_null_lo,
          d2.permutazione_anno_tipo_parametro.post_mandate.spearman_null_hi
        )}
        ).
      </p>

      <ScientificFigure
        id="fig-9"
        label="Figura 9"
        caption={`Rapporti osservate/attese con intervalli al 95% per i ${d2Spec.judges_tested} giudici (specificazione: ${d2Meta.label}; significativi Holm: ${d2Spec.sig_holm_above} sopra, ${d2Spec.sig_holm_below} sotto; varianza ${fmtDec(d2Spec.var_ratio_to_null, 2)}× il nullo${d2StrataInfo ? `; strati misti ${fmtPct(d2StrataInfo.share_tested_pronunce_in_mixed_strata)}` : ''}) e persistenza nei 10 anni post-mandato (reports/d2_results.json).`}
        controls={D2_SPECS.map((s) => (
          <SwitchBtn key={s.key} active={d2SpecKey === s.key} onClick={() => setD2SpecKey(s.key)}>
            {s.label}
          </SwitchBtn>
        ))}
      >
        <D2JudgeChart specData={d2Spec} />
      </ScientificFigure>

      <p>
        In D4 (potenza simulata pari a 1,00 per l&apos;effetto minimo del 20%), la quota di
        citazioni tra giudici nominati dallo stesso organo è del{' '}
        {fmtPct(d4.organo.same_group_share)} contro il {fmtPct(d4.organo.null_mean)} atteso (IC 95%:{' '}
        {fmtPctCI(d4.organo.null_lo, d4.organo.null_hi)}; <em>p</em>_Holm = {fmtP(d4.organo.p_holm)}
        ). Per provenienza professionale è del {fmtPct(d4.provenienza.same_group_share)} contro il{' '}
        {fmtPct(d4.provenienza.null_mean)} atteso ({fmtPctCI(d4.provenienza.null_lo, d4.provenienza.null_hi)}
        ; <em>p</em>_Holm = {fmtP(d4.provenienza.p_holm)}), un eccesso del +
        {fmtPct(d4.provenienza.excess_over_null)}, inferiore alla soglia d&apos;interesse del 20%.
      </p>

      {/* 3.4 Reti, filoni, esiti e misure EM1421 */}
      <SubTitle
        id="risultati-reti"
        num="3.4"
        title="Struttura delle reti, filoni, esiti API e misure del corso"
        status="esplorativo"
      />
      <p>
        L&apos;algoritmo di Leiden individua {extras.communities.communities_50plus} comunità con
        almeno 50 pronunce ({fmtPct(extras.communities.share_nodes_in_50plus)} dei nodi; modularità{' '}
        {fmtDec(extras.communities.modularity)} contro {fmtDec(extras.communities.modularity_rewired)}{' '}
        in 100 reti rimescolate; NMI con i temi {fmtDec(extras.communities.nmi_topic)} vs 0,006 del
        caso; NMI con Infomap {fmtDec(extras.communities.infomap.nmi_with_leiden)}). La Figura 10
        consente l&apos;esplorazione del sottografo delle 400 pronunce più citate (2.170 legami).
        Nella rete di co-sitting ({cositting.judges} giudici, {fmtInt(cositting.edges)} archi;{' '}
        <a href="#appendici" className="ref-link">Appendice B</a>),{' '}
        {fmtInt(cositting.pairs_active_same_years_together)} su{' '}
        {fmtInt(cositting.pairs_active_same_years)} coppie di giudici coevi siedono insieme almeno
        una volta (quota mediana {fmtPct(cositting.share.median)}).
      </p>

      <ScientificFigure
        id="fig-10"
        label="Figura 10"
        caption="Sottografo interattivo delle 400 pronunce più citate e delle 2.170 citazioni interne (layout Fruchterman–Reingold; area proporzionale al grado entrante; reports/rete_interattiva.html)."
        controls={
          <a
            href="./rete_interattiva.html"
            target="_blank"
            rel="noreferrer"
            className="px-2 py-1 text-[11px] font-mono border border-rule bg-paper text-ink hover:border-ink rounded-[2px]"
          >
            Apri in nuova scheda ↗
          </a>
        }
      >
        <iframe
          src="./rete_interattiva.html"
          title="Rete interattiva dei 400 precedenti più citati"
          className="w-full h-[600px] border border-zinc-200 bg-paper"
        />
      </ScientificFigure>

      <p>
        Dalle API esterne emerge che, tra le pronunce del 2006–2015, quelle con almeno una
        dichiarazione di illegittimità ricevono in 10 anni {fmtDec(extras.esito.tutte.media_ill, 1)}{' '}
        citazioni medie contro {fmtDec(extras.esito.tutte.media_altre, 1)} delle altre (rapporto{' '}
        {fmtDec(extras.esito.tutte.rapporto_medie, 2)}×, IC 95%:{' '}
        {fmtCI(extras.esito.tutte.rapporto_lo, extras.esito.tutte.rapporto_hi)}; tra le sole
        sentenze {fmtDec(extras.esito.sentenze.rapporto_medie, 2)}×). Su Wikipedia in italiano è
        citato l&apos;{fmtPct(extras.wikipedia.base_rate)} delle pronunce ({fmtInt(extras.wikipedia.linked_pronunce)}),
        quota che sale all&apos;{fmtPct(extras.wikipedia.share_in_top1_authority_pct)} nel top 1%
        HITS e al {fmtPct(extras.wikipedia.share_in_top1_citations_pct)} nel top 1% per citazioni.
        La Tabella 6 riassume le misure strutturali dei libri di testo (Easley e Kleinberg;
        Barabási).
      </p>

      <ScientificTable
        id="tab-6"
        label="Tabella 6"
        title="Misure strutturali dei libri di testo del corso EM1421 confrontate con i rispettivi modelli nulli."
        note="Fonte: reports/course_measures.json. Top 3 pronunce ponte per betweenness: 349/2007 (56% vicini esterni), 348/2007 (46%), 10/2015 (50%)."
      >
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-zinc-800 text-left font-mono text-muted">
              <th className="p-2">Proprietà</th>
              <th className="p-2 text-right">Osservato</th>
              <th className="p-2 text-right">Baseline / Nullo</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100 font-mono tabular-nums">
            <tr>
              <td className="p-2 font-sans text-ink">Attaccamento preferenziale (esponente a)</td>
              <td className="p-2 text-right">
                {fmtDec(course.preferential_attachment.a)} (
                {fmtCI(course.preferential_attachment.lo, course.preferential_attachment.hi)})
              </td>
              <td className="p-2 text-right text-muted">
                {fmtDec(course.preferential_attachment.null_mean)} (nullo D1)
              </td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Transitività / clustering locale medio (indiretto)</td>
              <td className="p-2 text-right">
                {fmtDec(course.structure.transitivity.observed, 3)} /{' '}
                {fmtDec(course.structure.avg_local_clustering.observed, 3)}
              </td>
              <td className="p-2 text-right text-muted">
                {fmtDec(course.structure.transitivity.null_mean, 3)} /{' '}
                {fmtDec(course.structure.avg_local_clustering.null_mean, 3)}
              </td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Correlazione di grado (in–in / out–in)</td>
              <td className="p-2 text-right">
                {fmtDec(course.structure.corr_in_in.observed, 3)} /{' '}
                {fmtDec(course.structure.corr_out_in.observed, 3)}
              </td>
              <td className="p-2 text-right text-muted">
                {fmtDec(course.structure.corr_in_in.null_mean, 3)} /{' '}
                {fmtDec(course.structure.corr_out_in.null_mean, 3)}
              </td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Piccolo mondo: distanza media nel blocco principale</td>
              <td className="p-2 text-right">{fmtDec(course.small_world.avg_distance)} passi</td>
              <td className="p-2 text-right text-muted">
                {fmtDec(course.small_world.er_avg_distance)} (Erdős–Rényi)
              </td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Ponti (vicini in altri filoni, top 1% betweenness)</td>
              <td className="p-2 text-right">
                {fmtPct(course.bridges.top1_betweenness_share_neighbours_outside)}
              </td>
              <td className="p-2 text-right text-muted">
                {fmtPct(course.bridges.top1_citations_share_neighbours_outside)} (top cit.) ·{' '}
                {fmtPct(course.bridges.all_connected_share_neighbours_outside)} (tutte)
              </td>
            </tr>
            <tr>
              <td className="p-2 font-sans text-ink">Robustezza: blocco principale dopo rimozione 20%</td>
              <td className="p-2 text-right">
                {fmtPct(course.robustness.after_removal['0.2'].targeted)} (mirata)
              </td>
              <td className="p-2 text-right text-muted">
                {fmtPct(course.robustness.after_removal['0.2'].random_mean)} (casuale)
              </td>
            </tr>
          </tbody>
        </table>
      </ScientificTable>

      {/* 3.5 Polarità e Altre Corti */}
      <SubTitle
        id="risultati-polarita"
        num="3.5"
        title="Risultato negativo sulla polarità e censimento delle altre quattro corti"
        status="negativo"
      />
      <p>
        Sul campione cieco di prova ({polarity.items} passi), le regole lessicali per la distinzione
        giurisprudenziale ottengono {polarity.flagged_true} veri positivi su {polarity.flagged}{' '}
        segnalati: precisione <strong>{fmtDec(polarity.precision, 2)}</strong> (IC 95% Wilson:{' '}
        {fmtPctCI(polarity.precision_lo, polarity.precision_hi)}), inferiore alla soglia
        preregistrata di {fmtDec(polarity.threshold, 2)} (per regola: <em>non_pertinente</em> 19/21,{' '}
        <em>caso_diverso</em> 7/8, <em>superamento</em> 2/7, <em>non_affermato</em> 0/1;{' '}
        {polarity.not_flagged_true}/{polarity.not_flagged} distinzioni nei passi non segnalati). In
        applicazione della regola d&apos;arresto, non è stata eseguita alcuna analisi inferenziale o
        di equilibrio strutturale.
      </p>
      <p>
        Sul versante dell&apos;estensione verso altre giurisdizioni (Figura 11; dettagli in{' '}
        <a href="#appendici" className="ref-link">Appendice C</a>), nel testo di base la Corte
        costituzionale nomina la Corte di cassazione in {fmtInt(courts.courts.Cassazione.pronunce_base)}{' '}
        pronunce ({fmtInt(courts.courts.Cassazione.pronunce_base_with_identifier)} con possibile
        identificativo), il Consiglio di Stato in {fmtInt(courts.courts['Consiglio di Stato'].pronunce_base)},
        la Corte di giustizia UE in {fmtInt(courts.courts['Corte di giustizia UE'].pronunce_base)} e
        la Corte EDU in {fmtInt(courts.courts['Corte EDU'].pronunce_base)}.
      </p>

      <ScientificFigure
        id="fig-11"
        label="Figura 11"
        caption="Numero di pronunce della Corte costituzionale che nominano ciascuna delle altre quattro corti nel testo di base, per decennio (1950–2020; reports/courts_sizing.json)."
      >
        <CourtsDecadeChart courts={courts} />
      </ScientificFigure>
    </section>
  );
}
