import React, { useMemo, useState } from 'react';
import { Badge, FigureBox, SectionHeader, StaticPngFigure, SubHeader, TabButton } from './UI';
import { D2JudgeChart } from './Charts';
import { fmtCI, fmtDec, fmtInt, fmtP, fmtPct, fmtPctCI } from '../utils/format';

const D2_SPECS = [
  { key: 'permutazione_anno', label: 'Anno (principale espl.)', strataKey: 'anno' },
  { key: 'permutazione_anno_tipo', label: 'Anno + Tipo', strataKey: 'anno_tipo' },
  { key: 'permutazione_anno_tipo_materia', label: 'Anno + Tipo + Materia', strataKey: 'anno_tipo_materia' },
  { key: 'permutazione_anno_tipo_parametro', label: 'Anno + Tipo + Parametro', strataKey: 'anno_tipo_parametro' },
  { key: 'permutazione_anno_dal_1987', label: 'Solo dal 1987 (red. oss.)', strataKey: null },
];

export function SectionD2D4({ data }) {
  const [specKey, setSpecKey] = useState('permutazione_anno');
  const [figMode, setFigMode] = useState('interactive');
  const [search, setSearch] = useState('');
  const [filterHolm, setFilterHolm] = useState('all'); // 'all' | 'sig'
  const [filterOrgano, setFilterOrgano] = useState('all');
  const [sortBy, setSortBy] = useState('rapporto');
  const [sortDir, setSortDir] = useState('desc');

  const { d2, d2Strata, d4 } = data;
  const currentSpec = D2_SPECS.find((s) => s.key === specKey);
  const spec = d2[specKey];
  const strataInfo = currentSpec?.strataKey ? d2Strata[currentSpec.strataKey] : null;

  const filteredJudges = useMemo(() => {
    let list = [...spec.table];
    if (search.trim()) {
      const q = search.trim().toLowerCase();
      list = list.filter((j) => j.nome.toLowerCase().includes(q));
    }
    if (filterHolm === 'sig') {
      list = list.filter((j) => j.p_holm < 0.05);
    }
    if (filterOrgano !== 'all') {
      list = list.filter((j) => j.organo === filterOrgano);
    }
    list.sort((a, b) => {
      const av = a[sortBy] ?? -999;
      const bv = b[sortBy] ?? -999;
      if (typeof av === 'string') return sortDir === 'asc' ? av.localeCompare(bv) : bv.localeCompare(av);
      return sortDir === 'asc' ? av - bv : bv - av;
    });
    return list;
  }, [spec, search, filterHolm, filterOrgano, sortBy, sortDir]);

  const toggleSort = (col) => {
    if (sortBy === col) setSortDir((d) => (d === 'desc' ? 'asc' : 'desc'));
    else {
      setSortBy(col);
      setSortDir('desc');
    }
  };

  return (
    <section>
      <SectionHeader
        id="d2-d4"
        num="4"
        title="D2 & D4 — I singoli giudici e l'appartenenza a gruppi"
        subtitle="Rapporto citazioni osservate/attese (finestra 10 anni, senza autocitazioni, 10.000 permutazioni, correzione di Holm) e omofilia per organo di nomina e provenienza."
        badge="esplorativo"
      />

      <div className="prose-editorial text-sm">
        <p>
          In D2 si studiano i giudici con almeno {d2.min_pronunce} pronunce redatte, contando le
          citazioni ricevute entro {d2.window_years} anni dal deposito da altri redattori (
          {fmtInt(d2.citations_used)} citazioni usate; {fmtInt(d2.self_citations_excluded)}{' '}
          autocitazioni escluse). D2 è marcato come <em>esplorativo</em> perché il modello nullo
          preregistrato (citazioni casuali tra pronunce dello stesso anno) ignorava la dispersione
          tra pronunce e gonfiava i risultati ({d2.nullo_preregistrato.age_only.sig_holm_above}{' '}
          sopra e {d2.nullo_preregistrato.age_only.sig_holm_below} sotto; varianza{' '}
          {fmtDec(d2.nullo_preregistrato.age_only.var_ratio_to_null, 1)}×). Con la permutazione dei
          giudici (10.000 repliche) le differenze restano reali nel complesso, ma pochi singoli
          giudici superano la soglia di Holm.
        </p>
      </div>

      {/* Selettore specificazione D2 */}
      <div className="flex flex-wrap gap-1.5 my-4">
        {D2_SPECS.map((s) => (
          <TabButton key={s.key} active={specKey === s.key} onClick={() => setSpecKey(s.key)}>
            {s.label}
          </TabButton>
        ))}
      </div>

      {/* KPI della specificazione selezionata */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 my-4 text-xs font-mono">
        <div className="p-3 bg-white border border-rule rounded-sm">
          <span className="text-muted block">Significativi Holm (p &lt; 0,05)</span>
          <strong className="text-base text-accent">
            {spec.sig_holm_above} sopra · {spec.sig_holm_below} sotto
          </strong>
          <span className="text-muted block">su {spec.judges_tested} giudici</span>
        </div>
        <div className="p-3 bg-white border border-rule rounded-sm">
          <span className="text-muted block">Variabilità vs nullo</span>
          <strong className="text-base text-ink">{fmtDec(spec.var_ratio_to_null, 2)}×</strong>
          <span className="text-muted block">p = {fmtP(spec.p_heterogeneity)}</span>
        </div>
        <div className="p-3 bg-white border border-rule rounded-sm">
          <span className="text-muted block">Persistenza post-mandato</span>
          <strong className="text-base text-ink">
            ρ = {fmtDec(spec.post_mandate.spearman_during_post)}
          </strong>
          <span className="text-muted block">
            atteso {fmtDec(spec.post_mandate.spearman_null_mean)} (
            {fmtCI(spec.post_mandate.spearman_null_lo, spec.post_mandate.spearman_null_hi)}) · n=
            {spec.post_mandate.judges}
          </span>
        </div>
        <div className="p-3 bg-white border border-rule rounded-sm">
          <span className="text-muted block">Strati misti (≥2 giudici)</span>
          <strong className="text-base text-ink">
            {strataInfo ? fmtPct(strataInfo.share_tested_pronunce_in_mixed_strata) : 'n/d'}
          </strong>
          <span className="text-muted block">
            {strataInfo ? `${fmtInt(strataInfo.strata)} strati` : 'solo pronunce ≥287/1986'}
          </span>
        </div>
      </div>

      {/* Figura 9-10 */}
      <FigureBox
        num="Figure 9–10 (D2)"
        title={`Distribuzione dei ${spec.judges_tested} giudici (${currentSpec.label}) e persistenza nei 10 anni dopo il mandato`}
        caption="Barre verticali: intervalli di confidenza al 95% (bootstrap sulle pronunce). Blu: giudici statisticamente diversi dal nullo dopo correzione di Holm (p_Holm < 0,05). Linea rossa: rapporto = 1."
        source="reports/d2_results.json · fig9_d2_giudici.png · fig10_d2_dopo_mandato.png"
        controls={
          <>
            <TabButton active={figMode === 'interactive'} onClick={() => setFigMode('interactive')}>
              Interattivo (JSON)
            </TabButton>
            <TabButton active={figMode === 'png'} onClick={() => setFigMode('png')}>
              Figure 9 &amp; 10 (PNG)
            </TabButton>
          </>
        }
      >
        {figMode === 'interactive' ? (
          <D2JudgeChart specData={spec} />
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <StaticPngFigure src="./figures/fig9_d2_giudici.png" alt="D2 giudici" />
            <StaticPngFigure src="./figures/fig10_d2_dopo_mandato.png" alt="D2 dopo mandato" />
          </div>
        )}
      </FigureBox>

      {/* Tabella completa di tutti i 113 / 74 giudici */}
      <SubHeader title={`Tabella completa dei giudici (${filteredJudges.length} di ${spec.table.length})`} />
      <div className="flex flex-wrap items-center gap-2 mb-3 text-xs">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Cerca giudice (es. Baldassarre, Onida)..."
          className="px-2.5 py-1.5 border border-rule rounded-sm bg-white text-ink w-60"
        />
        <select
          value={filterHolm}
          onChange={(e) => setFilterHolm(e.target.value)}
          className="px-2.5 py-1.5 border border-rule rounded-sm bg-white text-ink font-mono"
        >
          <option value="all">Tutti i giudici</option>
          <option value="sig">Solo significativi Holm (p &lt; 0,05)</option>
        </select>
        <select
          value={filterOrgano}
          onChange={(e) => setFilterOrgano(e.target.value)}
          className="px-2.5 py-1.5 border border-rule rounded-sm bg-white text-ink font-mono"
        >
          <option value="all">Tutti gli organi</option>
          <option value="Presidente della Repubblica">Presidente della Repubblica</option>
          <option value="Parlamento">Parlamento</option>
          <option value="magistrature">Magistrature</option>
        </select>
      </div>

      <div className="overflow-x-auto max-h-[420px] overflow-y-auto bg-white border border-rule rounded-sm">
        <table className="w-full text-xs">
          <thead className="sticky top-0 bg-zinc-50 border-b border-rule font-mono text-muted">
            <tr>
              <th className="p-2 text-left cursor-pointer hover:text-ink" onClick={() => toggleSort('nome')}>
                Giudice
              </th>
              <th className="p-2 text-left">Organo / Prov.</th>
              <th className="p-2 text-right cursor-pointer hover:text-ink" onClick={() => toggleSort('pronunce')}>
                Pron.
              </th>
              <th className="p-2 text-right cursor-pointer hover:text-ink" onClick={() => toggleSort('osservate')}>
                Oss.
              </th>
              <th className="p-2 text-right">Attese</th>
              <th className="p-2 text-right cursor-pointer hover:text-ink" onClick={() => toggleSort('rapporto')}>
                Rapporto (IC 95%)
              </th>
              <th className="p-2 text-right cursor-pointer hover:text-ink" onClick={() => toggleSort('p_holm')}>
                p_Holm
              </th>
              <th className="p-2 text-right">Dur. / Post</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100">
            {filteredJudges.map((j) => {
              const sig = j.p_holm < 0.05;
              return (
                <tr key={j.judge_id} className={sig ? 'bg-blue-50/40' : ''}>
                  <td className="p-2 font-medium text-ink">
                    {j.nome}{' '}
                    <span className="font-mono text-[10px] text-muted">
                      ({j.giuramento?.slice(0, 4)})
                    </span>
                  </td>
                  <td className="p-2 text-zinc-600">
                    {j.organo === 'Presidente della Repubblica' ? 'PdR' : j.organo} · {j.provenienza}
                  </td>
                  <td className="p-2 text-right font-mono tabular-nums">{fmtInt(j.pronunce)}</td>
                  <td className="p-2 text-right font-mono tabular-nums">{fmtInt(j.osservate)}</td>
                  <td className="p-2 text-right font-mono tabular-nums text-muted">
                    {fmtDec(j.attese, 1)}
                  </td>
                  <td
                    className={`p-2 text-right font-mono tabular-nums font-semibold ${
                      sig ? 'text-accent' : 'text-ink'
                    }`}
                  >
                    {fmtDec(j.rapporto)} ({fmtCI(j.lo, j.hi)})
                  </td>
                  <td className="p-2 text-right font-mono tabular-nums">{fmtP(j.p_holm)}</td>
                  <td className="p-2 text-right font-mono tabular-nums text-muted">
                    {j.rapporto_durante != null ? fmtDec(j.rapporto_durante) : '—'} /{' '}
                    {j.rapporto_post != null ? fmtDec(j.rapporto_post) : '—'}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* D4: Organo e Provenienza */}
      <SubHeader id="d4" title="D4 — Omofilia per organo di nomina e provenienza professionale" badge="secondario" />
      <div className="overflow-x-auto bg-white border border-rule rounded-sm my-3">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-rule bg-zinc-50 text-left font-mono text-muted">
              <th className="p-2.5">Attributo (potenza per +20% = 1,00)</th>
              <th className="p-2.5 text-right">Giudici / Citazioni</th>
              <th className="p-2.5 text-right">Quota osservata</th>
              <th className="p-2.5 text-right">Atteso nullo (95%)</th>
              <th className="p-2.5 text-right">Eccesso</th>
              <th className="p-2.5 text-right">p_Holm</th>
              <th className="p-2.5 text-right">Soglia +20%?</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100 font-mono tabular-nums">
            <tr>
              <td className="p-2.5 font-sans font-medium text-ink">
                Organo di nomina (Parlamento 41, PdR 41, Magistrature 40)
              </td>
              <td className="p-2.5 text-right">
                {d4.organo.judges} / {fmtInt(d4.organo.citations)}
              </td>
              <td className="p-2.5 text-right font-semibold">{fmtPct(d4.organo.same_group_share)}</td>
              <td className="p-2.5 text-right text-muted">
                {fmtPct(d4.organo.null_mean)} ({fmtPctCI(d4.organo.null_lo, d4.organo.null_hi)})
              </td>
              <td className="p-2.5 text-right">+{fmtPct(d4.organo.excess_over_null)}</td>
              <td className="p-2.5 text-right">{fmtP(d4.organo.p_holm)}</td>
              <td className="p-2.5 text-right">no</td>
            </tr>
            <tr>
              <td className="p-2.5 font-sans font-medium text-ink">
                Provenienza (professori 60, magistrati 55, avvocati 3)
              </td>
              <td className="p-2.5 text-right">
                {d4.provenienza.judges} / {fmtInt(d4.provenienza.citations)}
              </td>
              <td className="p-2.5 text-right font-semibold">
                {fmtPct(d4.provenienza.same_group_share)}
              </td>
              <td className="p-2.5 text-right text-muted">
                {fmtPct(d4.provenienza.null_mean)} (
                {fmtPctCI(d4.provenienza.null_lo, d4.provenienza.null_hi)})
              </td>
              <td className="p-2.5 text-right text-accent font-semibold">
                +{fmtPct(d4.provenienza.excess_over_null)}
              </td>
              <td className="p-2.5 text-right">{fmtP(d4.provenienza.p_holm)}</td>
              <td className="p-2.5 text-right">no</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  );
}
