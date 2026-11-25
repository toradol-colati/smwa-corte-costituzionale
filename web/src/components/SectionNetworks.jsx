import React, { useState } from 'react';
import { Badge, FigureBox, SectionHeader, SubHeader, TabButton } from './UI';
import { fmtCI, fmtDec, fmtInt, fmtPct, fmtPid } from '../utils/format';

export function SectionNetworks({ data }) {
  const [cositTab, setCositTab] = useState('top'); // 'top' | 'bottom' | 'never' | 'anomalies'
  const { cositting, extras, course } = data;

  return (
    <section>
      <SectionHeader
        id="reti"
        num="5"
        title="Reti interattive, filoni tematici, API e misure dei libri di testo"
        subtitle="Esplorazione del nucleo dei 400 precedenti più citati, rete di co-sitting tra giudici, comunità Leiden/Infomap, esiti SPARQL, Wikipedia e misure del corso EM1421."
        badge="esplorativo"
      />

      {/* Iframe rete interattiva */}
      <FigureBox
        num="Esplorazione interattiva"
        title="Il nucleo dei precedenti della Corte costituzionale (400 pronunce, 2.170 citazioni)"
        caption="Ogni cerchio è una pronuncia (area proporzionale alle citazioni ricevute sull'intera rete). Clicca un nodo per evidenziarne i legami in entrata e in uscita, filtra per filone o decennio, o cerca per numero/anno (es. 303/2003)."
        source="reports/rete_interattiva.html"
        controls={
          <a
            href="./rete_interattiva.html"
            target="_blank"
            rel="noreferrer"
            className="px-2.5 py-1 text-xs font-mono border border-rule bg-paper text-ink hover:border-ink rounded-sm"
          >
            Apri a schermo intero ↗
          </a>
        }
      >
        <iframe
          src="./rete_interattiva.html"
          title="Rete interattiva dei 400 precedenti più citati"
          className="w-full h-[640px] border border-zinc-200 rounded-sm bg-paper"
        />
      </FigureBox>

      {/* Rete di co-sitting */}
      <SubHeader id="cositting" title="Rete dei collegi tra giudici (co-sitting)" badge="descrittivo" />
      <div className="prose-editorial text-sm">
        <p>
          Proiezione sui giudici della rete di affiliazione collegio–pronuncia (
          <strong>{cositting.judges} giudici</strong>,{' '}
          <strong>{fmtInt(cositting.edges)} legami</strong> su {fmtInt(cositting.possible_pairs)}{' '}
          coppie possibili, densità globale {fmtPct(cositting.density)}). Tra i giudici in attività
          negli stessi anni la rete è quasi completa:{' '}
          <strong>
            {fmtInt(cositting.pairs_active_same_years_together)} su{' '}
            {fmtInt(cositting.pairs_active_same_years)}
          </strong>{' '}
          coppie coeve hanno deciso insieme almeno una pronuncia, con quota mediana di co-presenza
          pari all&apos;<strong>{fmtPct(cositting.share.median)}</strong> (peso mediano{' '}
          {fmtInt(cositting.weight.median)} pronunce; colleghi per giudice: mediana{' '}
          {fmtInt(cositting.colleagues.median)}, min {cositting.colleagues.min}–max{' '}
          {cositting.colleagues.max}). Per questa quasi-completezza locale la rete è usata solo per
          descrizione e controllo dati, mai per test statistici.
        </p>
      </div>

      <div className="bg-white border border-rule rounded-sm p-4 my-4">
        <div className="flex flex-wrap gap-1.5 mb-3">
          <TabButton active={cositTab === 'top'} onClick={() => setCositTab('top')}>
            Top 10 coppie per peso
          </TabButton>
          <TabButton active={cositTab === 'bottom'} onClick={() => setCositTab('bottom')}>
            Bottom 10 per quota (≥100 pron.)
          </TabButton>
          <TabButton active={cositTab === 'never'} onClick={() => setCositTab('never')}>
            7 coppie coeve mai insieme
          </TabButton>
          <TabButton active={cositTab === 'anomalies'} onClick={() => setCositTab('anomalies')}>
            13 anomalie date anagrafica
          </TabButton>
        </div>

        {cositTab === 'top' && (
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-rule text-left font-mono text-muted">
                <th className="py-1.5">Coppia di giudici</th>
                <th className="py-1.5 text-right">Decise insieme</th>
                <th className="py-1.5 text-right">Entrambi attivi</th>
                <th className="py-1.5 text-right">Quota</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100">
              {cositting.top10_weight.map((p) => (
                <tr key={`${p.a}-${p.b}`}>
                  <td className="py-1.5 font-medium text-ink">
                    {p.a} — {p.b}
                  </td>
                  <td className="py-1.5 text-right font-mono tabular-nums">{fmtInt(p.weight)}</td>
                  <td className="py-1.5 text-right font-mono tabular-nums text-muted">
                    {fmtInt(p.n_both_active)}
                  </td>
                  <td className="py-1.5 text-right font-mono tabular-nums">{fmtPct(p.share)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {cositTab === 'bottom' && (
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-rule text-left font-mono text-muted">
                <th className="py-1.5">Coppia (da verificare a mano)</th>
                <th className="py-1.5 text-right">Insieme</th>
                <th className="py-1.5 text-right">Entrambi attivi</th>
                <th className="py-1.5 text-right">Quota</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100">
              {cositting.bottom10_share_pairs_100.map((p) => (
                <tr key={`${p.a}-${p.b}`}>
                  <td className="py-1.5 font-medium text-ink">
                    {p.a} — {p.b}
                  </td>
                  <td className="py-1.5 text-right font-mono tabular-nums">{fmtInt(p.weight)}</td>
                  <td className="py-1.5 text-right font-mono tabular-nums text-muted">
                    {fmtInt(p.n_both_active)}
                  </td>
                  <td className="py-1.5 text-right font-mono tabular-nums text-amber-800">
                    {fmtPct(p.share)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {cositTab === 'never' && (
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-rule text-left font-mono text-muted">
                <th className="py-1.5">Coppia coeva mai nello stesso collegio</th>
                <th className="py-1.5 text-right">Pronunce nel periodo comune</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100">
              {cositting.pairs_active_same_years_never_together.map((p) => (
                <tr key={`${p.a}-${p.b}`}>
                  <td className="py-1.5 font-medium text-ink">
                    {p.a} — {p.b}
                  </td>
                  <td className="py-1.5 text-right font-mono tabular-nums">{fmtInt(p.n_both_active)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {cositTab === 'anomalies' && (
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-rule text-left font-mono text-muted">
                <th className="py-1.5">Giudice</th>
                <th className="py-1.5 text-right">Fine in anagrafica</th>
                <th className="py-1.5 text-right">Ultima presenza collegio</th>
                <th className="py-1.5 text-right">Giorni dopo</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100">
              {cositting.registry_presence_after_end.map((r) => (
                <tr key={r.judge}>
                  <td className="py-1.5 font-medium text-ink">{r.judge}</td>
                  <td className="py-1.5 text-right font-mono text-muted">{r.end_in_list}</td>
                  <td className="py-1.5 text-right font-mono">{r.last_presence}</td>
                  <td className="py-1.5 text-right font-mono font-semibold text-primary">
                    +{fmtInt(r.days_after_end)} gg
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Filoni Leiden/Infomap, Esiti e Wikipedia */}
      <SubHeader id="filoni" title="Filoni (Leiden & Infomap), esiti SPARQL e Wikipedia" badge="esplorativo" />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 my-4">
        <div className="lg:col-span-2 bg-white border border-rule rounded-sm p-4">
          <div className="text-xs font-mono uppercase tracking-wider text-muted mb-2">
            Le 12 comunità Leiden maggiori (modularità {fmtDec(extras.communities.modularity)} vs{' '}
            {fmtDec(extras.communities.modularity_rewired)} rimescolata; NMI con Infomap{' '}
            {fmtDec(extras.communities.infomap.nmi_with_leiden)})
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-rule text-left font-mono text-muted">
                  <th className="py-1.5">ID</th>
                  <th className="py-1.5 text-right">Nodi</th>
                  <th className="py-1.5 text-right">Anno med.</th>
                  <th className="py-1.5 pl-3">Parole del tema prevalente</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100">
                {extras.communities.largest.map((c) => (
                  <tr key={c.community}>
                    <td className="py-1.5 font-mono text-muted">{c.community}</td>
                    <td className="py-1.5 text-right font-mono tabular-nums font-medium">
                      {fmtInt(c.size)}
                    </td>
                    <td className="py-1.5 text-right font-mono tabular-nums">{c.median_year}</td>
                    <td className="py-1.5 pl-3 text-zinc-700">
                      {c.top_topic_words.slice(0, 5).join(', ')} ({fmtPct(c.top_topic_share, 0)})
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="space-y-4">
          <div className="bg-white border border-rule rounded-sm p-4 text-xs">
            <div className="font-mono uppercase tracking-wider text-muted mb-2">
              Esito (SPARQL, 2006–2015)
            </div>
            <p className="text-zinc-700 leading-relaxed mb-2">
              Pronunce con illegittimità ricevono in media{' '}
              <strong>{fmtDec(extras.esito.tutte.media_ill, 1)}</strong> citazioni in 10 anni contro{' '}
              <strong>{fmtDec(extras.esito.tutte.media_altre, 1)}</strong> delle altre:{' '}
              <strong>{fmtDec(extras.esito.tutte.rapporto_medie, 2)}×</strong> (IC 95%:{' '}
              {fmtCI(extras.esito.tutte.rapporto_lo, extras.esito.tutte.rapporto_hi)}). Tra le sole
              sentenze: <strong>{fmtDec(extras.esito.sentenze.rapporto_medie, 2)}×</strong> (
              {fmtCI(extras.esito.sentenze.rapporto_lo, extras.esito.sentenze.rapporto_hi)}).
            </p>
            <div className="space-y-1 pt-2 border-t border-zinc-100">
              {Object.entries(extras.esito.distribuzione)
                .slice(0, 5)
                .map(([k, v]) => (
                  <div key={k} className="flex justify-between">
                    <span className="text-zinc-600 truncate pr-2">{k}</span>
                    <span className="font-mono tabular-nums">{fmtInt(v)}</span>
                  </div>
                ))}
            </div>
          </div>

          <div className="bg-white border border-rule rounded-sm p-4 text-xs">
            <div className="font-mono uppercase tracking-wider text-muted mb-2">
              Wikipedia IT (descrittivo)
            </div>
            <p className="text-zinc-700 leading-relaxed mb-2">
              <strong>{fmtInt(extras.wikipedia.linked_pronunce)}</strong> pronunce citate (
              {fmtPct(extras.wikipedia.base_rate)} del totale). Quota linkata nel top 1% HITS:{' '}
              <strong>{fmtPct(extras.wikipedia.share_in_top1_authority_pct)}</strong>; nel top 1%
              citazioni: <strong>{fmtPct(extras.wikipedia.share_in_top1_citations_pct)}</strong>.
            </p>
            <div className="text-[11px] font-mono text-muted">
              Più linkate:{' '}
              {Object.entries(extras.wikipedia.most_linked)
                .slice(0, 5)
                .map(([pid, n]) => `${fmtPid(pid)} (${n})`)
                .join(' · ')}
            </div>
          </div>
        </div>
      </div>

      {/* Misure dei libri di testo EM1421 */}
      <SubHeader id="em1421" title="Misure dei libri di testo (Easley & Kleinberg; Barabási)" badge="esplorativo" />
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 my-4">
        <div className="bg-white border border-rule rounded-sm p-4">
          <div className="text-xs font-mono uppercase tracking-wider text-muted mb-2">
            Struttura, piccolo mondo e attaccamento preferenziale
          </div>
          <table className="w-full text-xs">
            <tbody className="divide-y divide-zinc-100">
              <tr>
                <td className="py-1.5 text-zinc-700">Attaccamento preferenziale (esponente a)</td>
                <td className="py-1.5 text-right font-mono">
                  <strong>{fmtDec(course.preferential_attachment.a)}</strong> (
                  {fmtCI(course.preferential_attachment.lo, course.preferential_attachment.hi)}) ·
                  nullo {fmtDec(course.preferential_attachment.null_mean)}
                </td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Transitività (chiusura triangoli, indiretto)</td>
                <td className="py-1.5 text-right font-mono">
                  <strong>{fmtDec(course.structure.transitivity.observed, 3)}</strong> vs{' '}
                  {fmtDec(course.structure.transitivity.null_mean, 3)}
                </td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Clustering locale medio</td>
                <td className="py-1.5 text-right font-mono">
                  <strong>{fmtDec(course.structure.avg_local_clustering.observed, 3)}</strong> vs{' '}
                  {fmtDec(course.structure.avg_local_clustering.null_mean, 3)}
                </td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Correlazione di grado (in–in / out–in)</td>
                <td className="py-1.5 text-right font-mono">
                  {fmtDec(course.structure.corr_in_in.observed, 3)} (vs{' '}
                  {fmtDec(course.structure.corr_in_in.null_mean, 3)}) ·{' '}
                  {fmtDec(course.structure.corr_out_in.observed, 3)} (vs{' '}
                  {fmtDec(course.structure.corr_out_in.null_mean, 3)})
                </td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Piccolo mondo (distanza media nel blocco)</td>
                <td className="py-1.5 text-right font-mono">
                  <strong>{fmtDec(course.small_world.avg_distance)}</strong> vs{' '}
                  {fmtDec(course.small_world.er_avg_distance)} (ER)
                </td>
              </tr>
              <tr>
                <td className="py-1.5 text-zinc-700">Ponti tra filoni (vicini esterni, top 1% btw)</td>
                <td className="py-1.5 text-right font-mono">
                  <strong>{fmtPct(course.bridges.top1_betweenness_share_neighbours_outside)}</strong>{' '}
                  vs {fmtPct(course.bridges.top1_citations_share_neighbours_outside)} (top cit.)
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="bg-white border border-rule rounded-sm p-4">
          <div className="text-xs font-mono uppercase tracking-wider text-muted mb-2">
            Robustezza della rete (blocco principale prima: {fmtPct(course.robustness.giant_share_before)})
          </div>
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-rule text-left font-mono text-muted">
                <th className="py-1.5">Quota rimossa</th>
                <th className="py-1.5 text-right">Mirata (più citate)</th>
                <th className="py-1.5 text-right">Casuale (min–max)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100 font-mono tabular-nums">
              {Object.entries(course.robustness.after_removal).map(([q, r]) => (
                <tr key={q}>
                  <td className="py-1.5">{fmtPct(Number(q), 0)}</td>
                  <td className="py-1.5 text-right font-semibold text-primary">
                    {fmtPct(r.targeted)}
                  </td>
                  <td className="py-1.5 text-right text-muted">
                    {fmtPct(r.random_mean)} ({fmtPct(r.random_lo)}–{fmtPct(r.random_hi)})
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Top 10 pronunce ponte */}
      <div className="bg-white border border-rule rounded-sm p-4 my-4">
        <div className="text-xs font-mono uppercase tracking-wider text-muted mb-2">
          Top 10 pronunce ponte per betweenness (sovrapposizione top 1% btw/citazioni:{' '}
          {fmtPct(course.bridges.overlap_top1_betweenness_citations)})
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-xs font-mono">
          {course.bridges.top10.map((b, i) => (
            <div key={b.pid} className="p-2 bg-paper border border-rule rounded-sm">
              <div className="font-semibold text-ink">
                {i + 1}. {fmtPid(b.pid)}
              </div>
              <div className="text-[11px] text-muted">
                cit. {b.citazioni} · est. {fmtPct(b.quota_vicini_in_altre_comunita, 0)}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
