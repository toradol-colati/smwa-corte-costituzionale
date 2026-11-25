import React, { useState } from 'react';
import { Badge, Callout, StatCell, SubHeader } from './UI';
import { fmtCI, fmtDec, fmtInt, fmtPct } from '../utils/format';

export function SectionOverview({ data, fullMode }) {
  const [openFaq, setOpenFaq] = useState(0);
  const { network, d1, d2, d3, d3Abs, d4, succession } = data;
  const sat = d3.primary.coef.sat_not_drafted;
  const selfD = d3.primary.coef.self_drafted;
  const selfNorm = d3.variants['controllo per norma impugnata in comune (esplorativo)'].coef.self_drafted;

  const faqs = [
    {
      q: 'Le 22.427 pronunce sono tutte quelle prese dalla Corte, o ne mancano?',
      a: `Sono tutte, dal 1956 al 2026, con un controllo interno: la numerazione riparte ogni anno, è unica per sentenze e ordinanze e non presenta buchi né doppioni. L'ultimo anno è incompleto: i file sono stati scaricati l'8 novembre 2026 e arrivano alla pronuncia n. ${data.numbers.last_year.last_number}, depositata il ${data.numbers.last_year.last_deposit}. Restano fuori gli altri atti della Corte (decreti, sentenza Lockheed del 1979 senza numero).`,
    },
    {
      q: 'Perché un collegio ha 11, 12, 13, 14 o 15 giudici?',
      a: `La Corte ha 15 giudici; per decidere ne servono almeno 11 (legge 87/1953, art. 16). Si scende sotto 15 per seggi vacanti o assenze. Nei dati il ${fmtPct(d3Abs.collegio_size.share_under_15)} delle pronunce ha meno di 15 giudici; in media ci sono ${fmtDec(d3Abs.collegio_size.mean_in_office, 1)} giudici in attività, ${fmtDec(d3Abs.collegio_size.mean_size, 1)} nel collegio e ${fmtDec(d3Abs.collegio_size.mean_absent, 1)} assenti. Tra i collegi sotto 15, il ${fmtPct(d3Abs.collegio_size.under_15_with_empty_seat)} cade con seggi vacanti e l'${fmtPct(d3Abs.collegio_size.under_15_with_absent_judge)} ha almeno un giudice assente. Il motivo della singola assenza non è registrato.`,
    },
    {
      q: 'Come si distingue il giudice che ha scritto una pronuncia da uno assente?',
      a: `Ogni pronuncia riporta in testa il collegio. Dal 23 dicembre 1986 (pronuncia 287/1986) riporta anche il redattore, nelle firme (fino al 2001) o nel campo dedicato (dal 2002). Un giudice in attività (presente in collegi prima e dopo) assente dall'elenco era assente. Prima del 23/12/1986 il nome del redattore non esiste: si usa il relatore come approssimazione dichiarata.`,
    },
    {
      q: 'Che cosa vuol dire "pronunce redatte da X", se a decidere è il collegio?',
      a: `La decisione è collegiale, presa a maggioranza in camera di consiglio senza voto pubblico né opinioni dissenzienti. Dopo il voto, il redattore stende le motivazioni e il collegio approva il testo. Si misura quindi se chi scrive lascia un'impronta sui precedenti citati, mai "decisioni di X".`,
    },
    {
      q: 'Come è stata verificata la "stessa provenienza" dei giudici (D4)?',
      a: `È ricavata in automatico dalla biografia ufficiale dell'anagrafica della Corte (parole chiave per professori, magistrati, avvocati), senza controllo manuale riga per riga. Eventuali errori di classificazione attenuerebbero un effetto, non lo creerebbero. L'organo di nomina viene invece dal campo ufficiale Eletto_da.`,
    },
    {
      q: 'Un precedente viene dimenticato, o lo sostituisce chi lo ha citato?',
      a: `Su ${fmtInt(succession.precedents)} precedenti del 1970–2010 citati almeno 5 volte entro 4 anni, le ${fmtInt(succession.successors)} pronunce che li hanno citati nei primi 4 anni ("successori") ricevono nella finestra 4–15 anni ${fmtDec(succession.later_window.ratio_successors_controls)} volte (IC 95%: ${fmtCI(succession.later_window.ratio_lo, succession.later_window.ratio_hi)}) le citazioni di pronunce simili (stesso anno, tipo, tema) che non li avevano citati, contando solo chi non cita più il precedente. Compatibile sia con un passaggio di testimone sia con l'importanza propria di chi cita precedenti rilevanti.`,
    },
  ];

  return (
    <section id="sintesi" className="scroll-mt-20">
      {/* Formulazione unica della domanda */}
      <Callout tone="primary" title="Domanda di ricerca (formulazione unica)">
        <p className="font-serif text-base sm:text-lg text-ink italic">
          «In un ordinamento in cui il precedente non vincola, la Corte costituzionale costruisce
          comunque una gerarchia di precedenti? E quanto di quell&apos;autorità passa attraverso i
          giudici che redigono e decidono le pronunce?»
        </p>
      </Callout>

      {/* KPI principali */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 my-6">
        <StatCell
          label="Endpoint primario (D3)"
          value={`OR ${fmtDec(sat.or)}`}
          sub={`IC 95%: ${fmtCI(sat.lo, sat.hi)} · p = ${fmtDec(sat.p)}`}
          highlight
        />
        <StatCell
          label="Scritto dallo stesso (D3)"
          value={`OR ${fmtDec(selfD.or)}`}
          sub={`Scende a ${fmtDec(selfNorm.or)} a parità di norma`}
        />
        <StatCell
          label="Concentrazione (D1)"
          value={fmtPct(d1.concentration.top1_share.observed)}
          sub={`Top 1% · atteso ${fmtPct(d1.concentration.top1_share.null_mean)} (anno)`}
        />
        <StatCell
          label="Base dati (1956–2026)"
          value={fmtInt(network.nodes)}
          sub={`${fmtInt(network.edges)} citazioni · 125 giudici`}
        />
      </div>

      {/* I tre risultati in sintesi */}
      <div className="prose-editorial space-y-4">
        <SubHeader title="I tre risultati principali" />

        <div className="p-4 bg-white border border-rule rounded-sm">
          <div className="flex items-center gap-2 mb-1.5">
            <span className="font-mono text-xs font-semibold text-primary">1. D3 — Memoria collegiale</span>
            <Badge type="principale" />
          </div>
          <p className="!mb-0 text-sm">
            Aver partecipato al collegio che ha deciso un precedente non aumenta la probabilità che
            lo stesso giudice lo citi in seguito: <strong>OR = {fmtDec(sat.or)}</strong> (IC 95%:{' '}
            {fmtCI(sat.lo, sat.hi)}; {fmtInt(d3.primary.strata)} pronunce che citano,{' '}
            {fmtInt(d3.primary.cases)} citazioni di cui {fmtInt(d3.primary.cases_absent)} a
            precedenti decisi in assenza del redattore). Averlo scritto, invece, pesa molto:{' '}
            <strong>OR = {fmtDec(selfD.or)}</strong> ({fmtCI(selfD.lo, selfD.hi)},{' '}
            <em>esplorativo</em>), ma il {fmtPct(d3.norme_descrittive.self_drafted.cases_same_article)}{' '}
            riguarda la stessa legge impugnata; a parità di norma impugnata scende a{' '}
            <strong>{fmtDec(selfNorm.or)}</strong> ({fmtCI(selfNorm.lo, selfNorm.hi)}).
          </p>
        </div>

        <div className="p-4 bg-white border border-rule rounded-sm">
          <div className="flex items-center gap-2 mb-1.5">
            <span className="font-mono text-xs font-semibold text-ink">2. D1 &amp; D1b — Concentrazione e durata</span>
            <Badge type="secondario" />
            <Badge type="esplorativo" />
          </div>
          <p className="!mb-0 text-sm">
            L&apos;1% più citato raccoglie il{' '}
            <strong>{fmtPct(d1.concentration.top1_share.observed)}</strong> delle citazioni (atteso{' '}
            {fmtPct(d1.concentration.top1_share.null_mean)} a parità d&apos;anno,{' '}
            {fmtPct(d1.concentration_by_type.top1_share.null_mean)} per anno e tipo); il{' '}
            {fmtPct(d1.concentration.never_cited.observed)} non è mai citato. Il picco di citazione
            cade a {d1.ageing.peak_age} anno ({fmtDec(d1.ageing.relative_rate_by_age[1], 1)}×), si
            dimezza in {d1.ageing.half_life_after_peak} anni e scende sotto 1× dopo{' '}
            {d1.ageing.age_when_rate_below_1} anni; il {fmtPct(d1.survival.share_cited_after_30y)}{' '}
            dei precedenti trentennali è ancora citato. I successori nei primi 4 anni sono citati il{' '}
            {fmtPct(succession.later_window.ratio_successors_controls - 1, 0)} in più dei controlli
            nella finestra 4–15 anni. Non reggono la legge di potenza (lognormale migliore,{' '}
            <em>p</em> &lt; 0,001) né l&apos;identità tra HITS e citazioni di Agnoloni e Pagallo
            (2016).
          </p>
        </div>

        <div className="p-4 bg-white border border-rule rounded-sm">
          <div className="flex items-center gap-2 mb-1.5">
            <span className="font-mono text-xs font-semibold text-ink">3. D2 &amp; D4 — Singoli giudici e gruppi</span>
            <Badge type="esplorativo" />
          </div>
          <p className="!mb-0 text-sm">
            Su {d2.permutazione_anno.judges_tested} giudici con almeno {d2.min_pronunce} pronunce,
            dopo correzione di Holm solo <strong>{d2.permutazione_anno.sig_holm_above}</strong> sono
            citati sopra l&apos;atteso e <strong>{d2.permutazione_anno.sig_holm_below}</strong>{' '}
            sotto (varianza {fmtDec(d2.permutazione_anno.var_ratio_to_null, 1)}× il nullo; controllando
            per anno, tipo e parametro costituzionale scendono a 0 sopra e 3 sotto). In D4 nessun
            effetto per organo di nomina (<em>p</em> = {fmtDec(d4.organo.p_holm, 3)}) e un eccesso del{' '}
            {fmtPct(d4.provenienza.excess_over_null)} per provenienza (<em>p</em>_Holm ={' '}
            {fmtDec(d4.provenienza.p_holm, 3)}), molto sotto la soglia d&apos;interesse del 20%.
          </p>
        </div>

        <Callout title="Sintesi in una frase">
          La Corte costruisce precedenti importanti ma di breve vita, che in parte passano il
          testimone alle pronunce che li citano. L&apos;autorità non passa dal collegio che ha deciso
          il precedente; passa in parte da chi lo ha redatto, soprattutto perché le questioni
          ripetute tornano allo stesso giudice.
        </Callout>

        {/* Contributo e punti aperti */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
          <div className="p-4 bg-white border border-rule rounded-sm text-sm">
            <div className="font-semibold text-ink mb-2">Che cosa aggiunge il lavoro</div>
            <ol className="list-decimal pl-4 space-y-1.5 text-zinc-700">
              <li>
                <strong>Risultato nullo preregistrato e preciso</strong> su D3 (OR 1,00; 0,92–1,09)
                affiancato al contrasto con l&apos;auto-redazione (5,47 → 3,27).
              </li>
              <li>
                <strong>Datazione empirica del cambio firme</strong>: 23/12/1986 (pronuncia
                287/1986), mesi prima della modifica normativa del luglio 1987 citata in dottrina.
              </li>
              <li>
                <strong>Verifica empirica di Agnoloni &amp; Pagallo (2016)</strong>: né legge di
                potenza né coincidenza tra top 30 HITS e citazioni (4/30 in comune).
              </li>
            </ol>
          </div>
          <div className="p-4 bg-white border border-rule rounded-sm text-sm">
            <div className="font-semibold text-ink mb-2">Che cosa resta aperto</div>
            <ul className="list-disc pl-4 space-y-1.5 text-zinc-700">
              <li>
                <strong>Validazione umana citazioni</strong> (36 pronunce,{' '}
                <code className="font-mono text-xs">human_check.md</code>): oggi la lettura di
                riferimento è dell&apos;assistente AI.
              </li>
              <li>
                <strong>Validazione umana polarità</strong> (67 passi): verifica del verdetto
                negativo (0,76 vs soglia 0,80).
              </li>
              <li>
                <strong>Approvazione del docente</strong> su tema, perimetro, lingua e uso AI.
              </li>
            </ul>
          </div>
        </div>

        {/* Chiarimenti di base (accordion) */}
        <SubHeader title="Chiarimenti di base (Parte I)" />
        <div className="border border-rule rounded-sm divide-y divide-rule bg-white">
          {faqs.map((f, i) => (
            <div key={f.q}>
              <button
                type="button"
                onClick={() => setOpenFaq(openFaq === i ? -1 : i)}
                className="w-full text-left px-4 py-3 flex items-center justify-between gap-4 hover:bg-zinc-50"
              >
                <span className="text-sm font-medium text-ink">{f.q}</span>
                <span className="font-mono text-xs text-muted shrink-0">
                  {openFaq === i ? '−' : '+'}
                </span>
              </button>
              {openFaq === i && (
                <div className="px-4 pb-3.5 text-sm text-zinc-700 leading-relaxed">{f.a}</div>
              )}
            </div>
          ))}
        </div>
      </div>

      {!fullMode && (
        <div className="mt-6 text-xs font-mono text-muted">
          Modalità sintesi attiva. Passa ad «Articolo completo (IMRAD)» in alto per leggere dati,
          metodi, risultati completi, reti interattive, limiti e appendici.
        </div>
      )}
    </section>
  );
}
