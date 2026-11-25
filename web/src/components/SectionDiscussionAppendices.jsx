import React, { useMemo, useState } from 'react';
import { ScientificTable, SectionTitle, SubTitle, SwitchBtn } from './UI';
import { fmtCI, fmtDec, fmtInt, fmtP, fmtPct } from '../utils/format';

const LIMITI = [
  ['Lettura di riferimento citazioni fatta da Claude (342 coppie, solo passi con parole chiave)', 'Tutta la rete', 'Possibile sovrastima di precisione e richiamo se assistente ed estrattore condividono errori'],
  ['Richiamo inferiore nei testi fino al 1986 (0,917; IC inf. 0,830)', 'D1b, D2 giudici antichi', 'Citazioni ai precedenti più vecchi lievemente sottostimate'],
  ['Redattore non registrato prima del 23/12/1986 (approssimato dal relatore)', 'D2, D3', 'Attenua le differenze tra giudici; la variante dal 1987 conferma D3 (OR 1,01)'],
  ['Assegnazione non casuale dei relatori da parte del Presidente', 'D3 (5,47 → 3,27), D2', 'Gonfia l\'auto-redazione e la variabilità tra giudici'],
  ['Motivo delle assenze dal collegio non registrato nei dati', 'Endpoint primario D3', 'Direzione incerta; V di Cramér ≤0,049 e |SMD| ≤0,097 attenuano il rischio di selezione sistematica'],
  ['Modello LDA a 20 temi con bassa stabilità (0,31) e temi formulari', 'Controllo materia D2 e D3', 'Controllo imperfetto; con parametri costituzionali D3 resta 0,99 ma la persistenza D2 diventa incerta'],
  ['Citare non equivale ad approvare', 'Tutta la rete', 'La distinzione/distacco non è separata; strumento polarità fermato sotto soglia (0,76)'],
  ['Censura a destra per le pronunce recenti', 'D1, D2', 'Mitigata da coorti annuali e finestre fisse (10 anni); dal 2020 informazione ridotta'],
  ['HITS concentra il 95,1% del top 1% in una sola comunità e assegna 0 a un terzo dei nodi', 'HITS vs citazioni', 'La divergenza dal nullo riflette soprattutto la struttura a comunità'],
  ['Modello nullo di D2 modificato dopo l\'ispezione dei risultati', 'D2', 'Statuto strettamente esplorativo'],
  ['Provenienza professionale ricavata automaticamente dalle biografie', 'D4', 'Eventuali errori di classificazione attenuano l\'effetto osservato'],
  ['Verifica della sostituzione non separa passaggio di testimone da importanza intrinseca', 'Sezione 3.2', 'Il +43% dei successori è compatibile con entrambe le ipotesi'],
];

const PROBLEMI_NOTI = [
  ['11.1 File senza script sorgente', 'reports/collegio_vs_sedute.json è presente dal primo commit ma nessuno script nel repository lo rigenera da sedute_membri.csv e collegio.csv.'],
  ['11.2 Script modificati non rieseguiti', 'src/analysis/topics.py e src/ingest/sparql_check.py sono stati aggiornati nel testo il 21/11/2026 senza rilanciarli.'],
  ['11.3 Legenda rete interattiva', 'reports/rete_interattiva.html non è stata ricontrollata integralmente dopo la riscrittura in linguaggio semplice.'],
  ['11.4 Validazioni umane pendenti', 'Restano da compilare data/validation/gold_human.txt (36 pronunce) e gold_polarity_human.txt (67 passi).'],
  ['11.5 Date anagrafiche e 2 presenze isolate', '13 giudici compaiono in collegi dopo la data di cessazione anagrafica (Appendice B); 2 presenze isolate (Vaccarella 429/2007, Dell\'Andro 71/1991) allungano il periodo in attività.'],
  ['11.6 Due grafie errate nei nomi visualizzati', '"Vincenzo Caianello" e "Enzo Capolozza" sono corretti nel matching (NAME_FIX) ma restano non corretti nei nomi esportati in judges.csv.'],
  ['11.7 257 collegi incompleti (1,15%)', 'Registrati in data/interim/collegio_errors.csv (refusi OCR negli anni 1960–1980, 47 sotto 11 giudici, 1 senza testo: 24/2000).'],
  ['11.8 Installazione da zero non testata', 'La ricostruzione da zero con requirements.lock (Python 3.12.4) non è ancora stata provata su macchina pulita.'],
  ['11.9 Co-redattori: 19 vs 17', 'build_judges.py conta 19 pronunce con più redattori contro 17 nel campo XML (escluse da D3).'],
];

const GLOSSARIO = [
  ['Collegio, relatore, redattore', 'Il collegio (11–15 giudici) decide; il relatore studia e riferisce; il redattore scrive le motivazioni approvate dal collegio.'],
  ['Correzione di Holm', 'Controllo del family-wise error rate su test multipli (mantiene sotto il 5% la probabilità di almeno un falso positivo).'],
  ['In attività vs in carica', 'In attività = prima–ultima presenza in collegio (usato in tutte le analisi); in carica = date ufficiali anagrafiche.'],
  ['Modello nullo', 'Repliche rimescolate dei dati che conservano vincoli strutturali (tempo, uscite) per quantificare cosa produce il caso.'],
  ['Odds ratio (OR)', 'Rapporto tra odds di due gruppi (1 = nessuna differenza; 2 = doppio; 0,5 = metà).'],
  ['Regressione logistica condizionata', 'Stima dentro ciascuno strato (pronuncia che cita) confrontando precedenti citati e 50 controlli non citati.'],
];

const PIPELINE_CMD = `python3.12 -m venv .venv
.venv/bin/pip install -r requirements.lock
.venv/bin/python -I src/ingest/download.py
.venv/bin/python src/ingest/inspect_raw.py
.venv/bin/python src/ingest/build_pronunce.py
.venv/bin/python src/extract/citations.py
.venv/bin/python src/extract/citations_massime.py
.venv/bin/python src/validation/evaluate.py test && .venv/bin/python src/validation/evaluate.py test2
.venv/bin/python src/judges/build_judges.py
.venv/bin/python src/analysis/topics.py && .venv/bin/python src/analysis/parametri.py
.venv/bin/python src/networks/build.py && .venv/bin/python src/networks/cositting.py
.venv/bin/python src/ingest/fetch_api.py
.venv/bin/python src/analysis/d1_pronunce.py
.venv/bin/python src/analysis/d2_d4_giudici.py && .venv/bin/python src/analysis/d2_strata_check.py
.venv/bin/python src/analysis/d3_memoria_collegiale.py && .venv/bin/python src/analysis/d3_absences.py && .venv/bin/python src/analysis/d3_full_check.py
.venv/bin/python src/analysis/precedent_succession.py && .venv/bin/python src/analysis/extras.py && .venv/bin/python src/analysis/course_measures.py
.venv/bin/python src/analysis/figures.py && .venv/bin/python src/analysis/interactive.py
.venv/bin/python src/report/report_numbers.py && .venv/bin/python src/report/plain_intros.py
.venv/bin/python src/courts/sizing.py && .venv/bin/python src/polarity/contexts.py && .venv/bin/python src/polarity/evaluate.py claude
.venv/bin/python -m pytest`;

export function SectionDiscussionAppendices({ data }) {
  const [appTab, setAppTab] = useState('A');
  const [judgeQ, setJudgeQ] = useState('');
  const [judgeHolmOnly, setJudgeHolmOnly] = useState(false);
  const [cositView, setCositView] = useState('top');

  const { d2, cositting, topics, parametri, courts } = data;

  const judgesFiltered = useMemo(() => {
    let list = [...d2.permutazione_anno.table];
    if (judgeQ.trim()) {
      const q = judgeQ.trim().toLowerCase();
      list = list.filter((j) => j.nome.toLowerCase().includes(q));
    }
    if (judgeHolmOnly) list = list.filter((j) => j.p_holm < 0.05);
    return list;
  }, [d2, judgeQ, judgeHolmOnly]);

  return (
    <section className="article-prose">
      <SectionTitle id="discussione" num="4" title="Discussione" />
      <p>
        Riprendendo la domanda di ricerca — se la Corte costituzionale costruisca una gerarchia di
        precedenti pur senza vincolo formale e quanto di tale autorità passi attraverso i giudici —
        lo studio restituisce un quadro netto. Sull&apos;endpoint primario preregistrato (D3),
        l&apos;ipotesi che la partecipazione al collegio decidente aumenti la probabilità di citare
        in seguito il precedente viene respinta con precisione elevata (OR 1,00; IC 95%: 0,92–1,09):
        in una corte collegiale priva di opinioni dissenzienti, il precedente non circola attraverso
        la semplice presenza in camera di consiglio.
      </p>
      <p>
        Al contrario, emerge un forte segnale legato al redattore (OR 5,47 in analisi esplorativa),
        che tuttavia non va letto come preferenza personale: l&apos;aggiunta del controllo per
        disposizione impugnata in comune riduce quasi della metà l&apos;eccesso sopra 1 (a 3,27),
        coerentemente con quanto osservato da Frankenreiter (2017b) alla Corte di giustizia UE
        sull&apos;assegnazione sistematica di questioni seriali allo stesso giudice relatore. Il
        medesimo meccanismo spiega l&apos;apparente anomalia dello 0,88 nel modello completo (che
        risale a 0,98 controllando per norma impugnata e parametri) e riduce drasticamente i giudici
        che si distinguono singolarmente in D2 (da 6 sopra l&apos;atteso a 0 controllando per
        articolo costituzionale).
      </p>
      <p>
        Sul piano strutturale (D1), i risultati ridimensionano le due conclusioni di Agnoloni e
        Pagallo (2016): la coda delle citazioni è descritta meglio da una lognormale che da una
        legge di potenza, e l&apos;algoritmo HITS non coincide con il conteggio delle citazioni (4
        su 30 sul loro perimetro) né migliora la previsione delle citazioni future, a differenza di
        quanto riportato da Fowler et al. (2007) per la Corte suprema statunitense. Infine, i due
        esiti negativi — l&apos;assenza di effetto in D3 e il mancato superamento della soglia di
        precisione nella polarità delle citazioni (0,76 &lt; 0,80) — costituiscono risultati
        metodologici essenziali, che delimitano ciò che è misurabile con dati aperti senza
        sovrainterpretazioni.
      </p>

      <SubTitle id="limiti" num="4.1" title="Limiti specifici dello studio" />
      <ScientificTable
        id="tab-7"
        label="Tabella 7"
        title="Limiti specifici dello studio, risultati interessati e direzione attesa della distorsione."
      >
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-zinc-800 text-left font-mono text-muted">
              <th className="p-2">Limite</th>
              <th className="p-2">Risultato minacciato</th>
              <th className="p-2">Direzione / Effetto</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100">
            {LIMITI.map(([l, r, e]) => (
              <tr key={l}>
                <td className="p-2 font-medium text-ink align-top">{l}</td>
                <td className="p-2 font-mono text-muted align-top whitespace-nowrap">{r}</td>
                <td className="p-2 text-zinc-700 align-top">{e}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </ScientificTable>

      {/* 5. Appendici */}
      <SectionTitle id="appendici" num="5" title="Appendici" />
      <div className="flex flex-wrap gap-1.5 mb-5">
        <SwitchBtn active={appTab === 'A'} onClick={() => setAppTab('A')}>
          Appendice A · 113 Giudici (D2)
        </SwitchBtn>
        <SwitchBtn active={appTab === 'B'} onClick={() => setAppTab('B')}>
          Appendice B · Co-sitting &amp; Anomalie
        </SwitchBtn>
        <SwitchBtn active={appTab === 'C'} onClick={() => setAppTab('C')}>
          Appendice C · 20 Temi, Parametri, Corti
        </SwitchBtn>
        <SwitchBtn active={appTab === 'D'} onClick={() => setAppTab('D')}>
          Appendice D · Problemi noti, AI, Pipeline
        </SwitchBtn>
      </div>

      {appTab === 'A' && (
        <div className="bg-white border border-rule p-4">
          <div className="flex flex-wrap items-center gap-2 mb-3 text-xs">
            <input
              type="text"
              value={judgeQ}
              onChange={(e) => setJudgeQ(e.target.value)}
              placeholder="Cerca giudice..."
              className="px-2.5 py-1 border border-rule rounded-[2px] w-56"
            />
            <label className="flex items-center gap-1.5 font-mono text-[11px] text-muted cursor-pointer">
              <input
                type="checkbox"
                checked={judgeHolmOnly}
                onChange={(e) => setJudgeHolmOnly(e.target.checked)}
              />
              Solo significativi Holm (p &lt; 0,05)
            </label>
            <span className="font-mono text-[11px] text-muted ml-auto">
              {judgesFiltered.length} / {d2.permutazione_anno.table.length} giudici (permutazione per anno)
            </span>
          </div>
          <div className="overflow-x-auto max-h-[420px] overflow-y-auto border-t border-rule">
            <table className="w-full text-xs">
              <thead className="sticky top-0 bg-zinc-50 border-b border-rule font-mono text-muted">
                <tr>
                  <th className="p-2 text-left">Giudice</th>
                  <th className="p-2 text-left">Organo · Prov.</th>
                  <th className="p-2 text-right">Pron.</th>
                  <th className="p-2 text-right">Oss. / Att.</th>
                  <th className="p-2 text-right">Rapporto (IC 95%)</th>
                  <th className="p-2 text-right">p_Holm</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100">
                {judgesFiltered.map((j) => (
                  <tr key={j.judge_id} className={j.p_holm < 0.05 ? 'bg-blue-50/40' : ''}>
                    <td className="p-1.5 font-medium text-ink">{j.nome}</td>
                    <td className="p-1.5 text-zinc-600">
                      {j.organo === 'Presidente della Repubblica' ? 'PdR' : j.organo} · {j.provenienza}
                    </td>
                    <td className="p-1.5 text-right font-mono tabular-nums">{fmtInt(j.pronunce)}</td>
                    <td className="p-1.5 text-right font-mono tabular-nums">
                      {fmtInt(j.osservate)} / {fmtDec(j.attese, 1)}
                    </td>
                    <td className="p-1.5 text-right font-mono tabular-nums font-semibold">
                      {fmtDec(j.rapporto)} ({fmtCI(j.lo, j.hi)})
                    </td>
                    <td className="p-1.5 text-right font-mono tabular-nums">{fmtP(j.p_holm)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {appTab === 'B' && (
        <div className="bg-white border border-rule p-4">
          <div className="flex flex-wrap gap-1.5 mb-3">
            <SwitchBtn active={cositView === 'top'} onClick={() => setCositView('top')}>Top 10 peso</SwitchBtn>
            <SwitchBtn active={cositView === 'bottom'} onClick={() => setCositView('bottom')}>Bottom 10 quota</SwitchBtn>
            <SwitchBtn active={cositView === 'never'} onClick={() => setCositView('never')}>7 mai insieme</SwitchBtn>
            <SwitchBtn active={cositView === 'anomalies'} onClick={() => setCositView('anomalies')}>13 anomalie anagrafica</SwitchBtn>
          </div>
          {cositView === 'top' && (
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-rule font-mono text-muted text-left">
                  <th className="py-1.5">Coppia</th>
                  <th className="py-1.5 text-right">Insieme</th>
                  <th className="py-1.5 text-right">Entrambi attivi</th>
                  <th className="py-1.5 text-right">Quota</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100">
                {cositting.top10_weight.map((p) => (
                  <tr key={`${p.a}-${p.b}`}>
                    <td className="py-1.5">{p.a} — {p.b}</td>
                    <td className="py-1.5 text-right font-mono">{fmtInt(p.weight)}</td>
                    <td className="py-1.5 text-right font-mono text-muted">{fmtInt(p.n_both_active)}</td>
                    <td className="py-1.5 text-right font-mono">{fmtPct(p.share)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          {cositView === 'bottom' && (
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-rule font-mono text-muted text-left">
                  <th className="py-1.5">Coppia (≥100 pronunce comuni)</th>
                  <th className="py-1.5 text-right">Insieme</th>
                  <th className="py-1.5 text-right">Attivi</th>
                  <th className="py-1.5 text-right">Quota</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100">
                {cositting.bottom10_share_pairs_100.map((p) => (
                  <tr key={`${p.a}-${p.b}`}>
                    <td className="py-1.5">{p.a} — {p.b}</td>
                    <td className="py-1.5 text-right font-mono">{fmtInt(p.weight)}</td>
                    <td className="py-1.5 text-right font-mono text-muted">{fmtInt(p.n_both_active)}</td>
                    <td className="py-1.5 text-right font-mono text-primary">{fmtPct(p.share)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          {cositView === 'never' && (
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-rule font-mono text-muted text-left">
                  <th className="py-1.5">Coppia coeva mai nello stesso collegio</th>
                  <th className="py-1.5 text-right">Pronunce nel periodo comune</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100">
                {cositting.pairs_active_same_years_never_together.map((p) => (
                  <tr key={`${p.a}-${p.b}`}>
                    <td className="py-1.5">{p.a} — {p.b}</td>
                    <td className="py-1.5 text-right font-mono">{fmtInt(p.n_both_active)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          {cositView === 'anomalies' && (
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-rule font-mono text-muted text-left">
                  <th className="py-1.5">Giudice</th>
                  <th className="py-1.5 text-right">Fine anagrafica</th>
                  <th className="py-1.5 text-right">Ultima presenza</th>
                  <th className="py-1.5 text-right">Scarto</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100">
                {cositting.registry_presence_after_end.map((r) => (
                  <tr key={r.judge}>
                    <td className="py-1.5">{r.judge}</td>
                    <td className="py-1.5 text-right font-mono text-muted">{r.end_in_list}</td>
                    <td className="py-1.5 text-right font-mono">{r.last_presence}</td>
                    <td className="py-1.5 text-right font-mono text-primary">+{fmtInt(r.days_after_end)} gg</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {appTab === 'C' && (
        <div className="space-y-4 bg-white border border-rule p-4">
          <div className="text-xs font-mono uppercase text-muted">I 20 temi LDA (k = 20, coerenza NPMI 0,2031)</div>
          <div className="overflow-x-auto max-h-[280px] overflow-y-auto">
            <table className="w-full text-xs">
              <thead className="sticky top-0 bg-zinc-50 border-b border-rule font-mono text-muted text-left">
                <tr>
                  <th className="p-1.5">ID</th>
                  <th className="p-1.5">Etichetta (lift ≥15 mass., ≥10%)</th>
                  <th className="p-1.5">Parole principali</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100">
                {Object.keys(topics.top_words).sort((a, b) => Number(a) - Number(b)).map((id) => (
                  <tr key={id}>
                    <td className="p-1.5 font-mono text-muted">{id}</td>
                    <td className="p-1.5 font-medium">{topics.label_details[id].label || '—'}</td>
                    <td className="p-1.5 text-zinc-600">{topics.top_words[id].slice(0, 7).join(', ')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="pt-3 border-t border-rule grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div>
              <div className="font-mono uppercase text-muted mb-1.5">Top 10 articoli Costituzione</div>
              <div className="grid grid-cols-2 gap-1 font-mono">
                {Object.entries(parametri.share_invoking_top).map(([a, s]) => (
                  <div key={a} className="flex justify-between pr-3">
                    <span>Art. {a}</span>
                    <span>{fmtPct(s, 1)}</span>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <div className="font-mono uppercase text-muted mb-1.5">Altre 4 corti (testo di base)</div>
              <div className="space-y-1">
                {Object.entries(courts.courts).map(([name, c]) => (
                  <div key={name} className="flex justify-between">
                    <span>{name}</span>
                    <span className="font-mono">{fmtInt(c.pronunce_base)} pron. ({fmtInt(c.mentions_base)} menz.)</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {appTab === 'D' && (
        <div className="space-y-5 bg-white border border-rule p-4 text-xs">
          <div>
            <div className="font-mono uppercase text-muted mb-2">Problemi noti e punti non verificati (handbook §11)</div>
            <div className="divide-y divide-zinc-100">
              {PROBLEMI_NOTI.map(([t, d]) => (
                <div key={t} className="py-1.5">
                  <strong className="font-mono text-ink">{t}:</strong> <span className="text-zinc-700">{d}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="pt-3 border-t border-rule">
            <div className="font-mono uppercase text-muted mb-1.5">Uso dell&apos;intelligenza artificiale</div>
            <p className="text-zinc-700 leading-relaxed !mb-0 !text-xs">
              Svolto con Claude Code sotto la direzione di Umberto Toraldo. Conseguenze per il lettore:
              (1) le letture di riferimento di citazioni e polarità sono dell&apos;assistente (controlli
              umani preparati e in attesa); (2) le regole del 16/11 sono state scritte dallo stesso
              assistente su delega; (3) le regole del corso sull&apos;AI vanno confermate dal docente.
            </p>
          </div>
          <div className="pt-3 border-t border-rule">
            <div className="font-mono uppercase text-muted mb-1.5">Glossario essenziale</div>
            <dl className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
              {GLOSSARIO.map(([term, def]) => (
                <div key={term}>
                  <dt className="font-semibold text-ink">{term}</dt>
                  <dd className="text-zinc-600">{def}</dd>
                </div>
              ))}
            </dl>
          </div>
          <div className="pt-3 border-t border-rule">
            <div className="font-mono uppercase text-muted mb-1.5">Pipeline completa di riproducibilità</div>
            <pre className="text-[10.5px] font-mono bg-zinc-900 text-zinc-100 p-3 overflow-x-auto leading-relaxed">
              {PIPELINE_CMD}
            </pre>
          </div>
        </div>
      )}

      {/* 6. Bibliografia */}
      <SectionTitle id="bibliografia" num="6" title="Bibliografia essenziale (fonti lette)" />
      <ol className="list-decimal pl-5 space-y-1.5 text-xs text-zinc-700 leading-relaxed">
        <li>Agnoloni, T., &amp; Pagallo, U. (2016). The Case Law of the Italian Constitutional Court between Network Theory and Philosophy of Information. <em>Informatica e diritto</em>, XXV(1), 139–151.</li>
        <li>Barabási, A.-L. (2016). <em>Network Science</em>. Cambridge University Press (§3.8–3.10).</li>
        <li>Caravita, B. (2021). <em>Ai margini della dissenting opinion. Lo «strano caso» della sostituzione del relatore nel giudizio costituzionale</em>. Giappichelli (pp. 2–8).</li>
        <li>Clauset, A., Shalizi, C. R., &amp; Newman, M. E. J. (2009). Power-law distributions in empirical data. <em>SIAM Review</em>, 51(4), 661–703.</li>
        <li>Easley, D., &amp; Kleinberg, J. (2010). <em>Networks, Crowds, and Markets</em>. Cambridge University Press (cap. 5, §14.5, cap. 20).</li>
        <li>Fowler, J. H., Johnson, T. R., Spriggs, J. F., Jeon, S., &amp; Wahlbeck, P. J. (2007). Network Analysis and the Law. <em>Political Analysis</em>, 15(3), 324–346.</li>
        <li>Frankenreiter, J. (2017a). Network analysis and the use of precedent in the case law of the CJEU — A reply to Derlén and Lindholm. <em>Journal of Empirical Legal Studies</em>, 14(4), 687–694.</li>
        <li>Frankenreiter, J. (2017b). The Politics of Citations at the ECJ — Policy Preferences of EU Member State Governments and the Citation Behavior of Judges at the European Court of Justice. <em>Journal of Empirical Legal Studies</em>, 14(4), 813–857.</li>
        <li>King, G., &amp; Zeng, L. (2001). Logistic Regression in Rare Events Data. <em>Political Analysis</em>, 9(2), 137–163.</li>
        <li>Landes, W. M., Lessig, L., &amp; Solimine, M. E. (1998). Judicial Influence: A Citation Analysis of Federal Courts of Appeals Judges. <em>Journal of Legal Studies</em>, 27(2), 271–332.</li>
        <li>Lupu, Y., &amp; Voeten, E. (2012). Precedent in International Courts: A Network Analysis of Case Citations by the European Court of Human Rights. <em>British Journal of Political Science</em>, 42(2), 413–439.</li>
        <li>Uzzi, B., Mukherjee, S., Stringer, M., &amp; Jones, B. (2013). Atypical Combinations and Scientific Impact. <em>Science</em>, 342(6157), 468–472 (Materiali aggiuntivi, pp. 3, 5).</li>
      </ol>
    </section>
  );
}
