import React from 'react';
import { Callout, FigureBox, SectionHeader, SubHeader } from './UI';
import { CourtsDecadeChart } from './Charts';
import { fmtDec, fmtInt, fmtPct, fmtPctCI } from '../utils/format';

export function SectionPolarityCourts({ data }) {
  const { polarity, courts } = data;

  return (
    <section>
      <SectionHeader
        id="polarita-corti"
        num="6"
        title="Polarità delle citazioni (esito negativo) e altre quattro corti"
        subtitle="Adattamento della sentiment analysis alla distinzione giurisprudenziale (sotto soglia, fermata per regola preregistrata) e censimento dei riferimenti a Cassazione, Consiglio di Stato, CGUE e Corte EDU."
      />

      <SubHeader id="polarita" title="Polarità delle citazioni: strumento sotto soglia" badge="negativo" />
      <Callout tone="warn" title="Regola di arresto applicata: nessuna analisi inferenziale">
        Su {polarity.items} passi del campione cieco ({polarity.flagged} segnalati dalle regole
        lessicali + {polarity.not_flagged} non segnalati con parola chiave), i passi segnalati
        risultano vere distinzioni in <strong>{polarity.flagged_true} casi su {polarity.flagged}</strong>:
        precisione <strong>{fmtDec(polarity.precision, 2)}</strong> (IC 95% Wilson:{' '}
        {fmtPctCI(polarity.precision_lo, polarity.precision_hi)}),{' '}
        <strong>sotto la soglia preregistrata di {fmtDec(polarity.threshold, 2)}</strong>. Come
        stabilito prima della prova, non sono stati calcolati né quote di distacco né equilibrio
        strutturale (che inoltre richiederebbe adattamento a grafi diretti, Easley &amp; Kleinberg
        §5.3). Tra i {polarity.not_flagged} passi non segnalati, {polarity.not_flagged_true} sono
        vere distinzioni.
      </Callout>

      <div className="bg-white border border-rule rounded-sm p-4 my-4 max-w-xl">
        <div className="text-xs font-mono uppercase tracking-wider text-muted mb-2">
          Precisione per singola regola (campione di prova)
        </div>
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-rule text-left font-mono text-muted">
              <th className="py-1.5">Regola</th>
              <th className="py-1.5 text-right">Segnalati</th>
              <th className="py-1.5 text-right">Veri</th>
              <th className="py-1.5 text-right">Precisione</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100 font-mono tabular-nums">
            {Object.entries(polarity.precision_by_rule).map(([rule, r]) => (
              <tr key={rule}>
                <td className="py-1.5 text-ink">{rule}</td>
                <td className="py-1.5 text-right">{r.n}</td>
                <td className="py-1.5 text-right">{r.true}</td>
                <td className="py-1.5 text-right font-semibold">
                  {r.n > 0 ? fmtPct(r.true / r.n, 1) : '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <SubHeader id="altre-corti" title="Rete tra corti: censimento delle menzioni (impostato)" badge="descrittivo" />
      <div className="prose-editorial text-sm">
        <p>
          Prima di estrarre una rete tra corti sono stati verificati competenze, identificatori e
          condizioni d&apos;uso di Cassazione, Consiglio di Stato, Corte di giustizia UE e Corte
          EDU. Con dati aperti è costruibile solo il verso &laquo;Corte costituzionale → altre
          corti&raquo; (il verso opposto è escluso dalle licenze per Cassazione e Consiglio di
          Stato, e possibile in principio solo per la CGUE via EUR-Lex/CELLAR CC0). Le regole di
          estrazione (<code className="font-mono text-xs">src/courts/mentions.py</code>) sono in
          sviluppo su metà del corpus; la metà di prova resta chiusa in attesa di validazione umana.
        </p>
      </div>

      <div className="overflow-x-auto bg-white border border-rule rounded-sm my-4">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-rule bg-zinc-50 text-left font-mono text-muted">
              <th className="p-2.5">Corte</th>
              <th className="p-2.5 text-right">Pronunce (testo base)</th>
              <th className="p-2.5 text-right">Con possibile ID</th>
              <th className="p-2.5 text-right">In fatto</th>
              <th className="p-2.5 text-right">Menzioni totali</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100 font-mono tabular-nums">
            {Object.entries(courts.courts).map(([name, c]) => (
              <tr key={name}>
                <td className="p-2.5 font-sans font-medium text-ink">{name}</td>
                <td className="p-2.5 text-right font-semibold">{fmtInt(c.pronunce_base)}</td>
                <td className="p-2.5 text-right">{fmtInt(c.pronunce_base_with_identifier)}</td>
                <td className="p-2.5 text-right text-muted">{fmtInt(c.pronunce_facts)}</td>
                <td className="p-2.5 text-right">{fmtInt(c.mentions_base)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <FigureBox
        num="Censimento corti"
        title="Pronunce della Corte costituzionale che nominano le altre quattro corti per decennio"
        caption="Conteggi nel testo di base (ragionamento + dispositivo). Nominare una corte include riferimenti generici e casi in cui la corte è giudice a quo."
        source="reports/courts_sizing.json"
      >
        <CourtsDecadeChart courts={courts} />
      </FigureBox>
    </section>
  );
}
