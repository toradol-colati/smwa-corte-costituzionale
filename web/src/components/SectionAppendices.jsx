import React, { useState } from 'react';
import { SectionHeader, SubHeader, TabButton } from './UI';

const LIMITI = [
  ['Lettura di riferimento citazioni fatta da Claude (342 coppie, solo passi con parole chiave)', 'Tutta la rete', 'Se assistente ed estrattore condividono errori, precisione e richiamo risultano sovrastimati'],
  ['Richiamo inferiore nei testi fino al 1986 (0,92; IC inf. 0,83)', 'Durata precedenti, D2 giudici antichi', 'Citazioni ai precedenti antichi leggermente sottostimate'],
  ['Prima del 23/12/1986 il redattore non è registrato (si usa il relatore)', 'D2, D3', 'Attenua le differenze tra giudici; la variante dal 1987 conferma D3 (OR 1,01)'],
  ['Assegnazione non casuale dei relatori da parte del Presidente', 'D3 (5,47 → 3,27), classifiche D2', 'Gonfia l\'effetto dell\'auto-redazione e le differenze individuali'],
  ['Motivo delle assenze dal collegio non registrato nei dati', 'Endpoint primario D3', 'Direzione incerta; tuttavia V di Cramér ≤ 0,049 e max |SMD| = 0,097'],
  ['Modello LDA a 20 temi con bassa stabilità (0,31) e temi formulari', 'Controllo materia D2 e D3', 'Controllo imperfetto; con i parametri costituzionali D3 resta 0,99 ma la persistenza D2 diventa incerta'],
  ['Citare non equivale ad approvare', 'Tutta la rete', 'Un precedente può essere citato per distinguersene; strumento polarità sotto soglia (0,76)'],
  ['Censura a destra per pronunce recenti', 'D1, D2', 'Gestita con finestre fisse (10 anni) e coorti annuali; dal 2020 informazione ridotta'],
  ['HITS assegna authority 0 a un terzo dei nodi e concentra il 95,1% in un filone', 'HITS vs citazioni', 'La differenza dal nullo misura soprattutto l\'esistenza dei filoni'],
  ['Modello nullo di D2 cambiato dopo aver visto i risultati', 'D2', 'Statuto strettamente esplorativo; nessuna inferenza confermativa'],
  ['Provenienza professionale estratta in automatico dalle biografie', 'D4', 'Errori di classificazione attenuano eventuali effetti, non li creano'],
  ['Verifica sostituzione non separa passaggio di testimone da importanza intrinseca', 'Sezione 3.3', 'Il +43% dei successori può riflettere entrambi i meccanismi'],
];

const PROBLEMI_NOTI = [
  ['11.1 Risultato senza script sorgente', 'reports/collegio_vs_sedute.json esiste dal primo commit ma nessuno script nel repo lo rigenera (va scritto uno script che legga sedute_membri.csv e collegio.csv).'],
  ['11.2 Script modificati non rieseguiti', 'src/analysis/topics.py e src/ingest/sparql_check.py sono stati aggiornati nel testo il 21/11/2026 senza rilanciarli (calcolo lungo / endpoint SPARQL dinamico).'],
  ['11.3 Legenda rete interattiva', 'reports/rete_interattiva.html non è stata ricontrollata integralmente dopo la riscrittura in linguaggio semplice.'],
  ['11.4 Controlli umani mancanti', 'Restano da compilare data/validation/gold_human.txt (36 pronunce) e gold_polarity_human.txt (67 passi).'],
  ['11.5 Date anagrafiche e 2 presenze isolate', '13 giudici compaiono in collegi dopo la fine mandato ufficiale (es. Mezzanotte +3.271 gg); 2 presenze isolate (Vaccarella 429/2007, Dell\'Andro 71/1991) allungano il periodo in attività.'],
  ['11.6 Due refusi anagrafici residui', '"Vincenzo Caianello" (Caianiello) e "Enzo Capolozza" (Capalozza) sono corretti nel matching (NAME_FIX) ma restano scritti male nei nomi mostrati in judges.csv.'],
  ['11.7 257 collegi incompleti (1,15%)', 'Elencati in data/interim/collegio_errors.csv (210 con nomi non riconosciuti per refusi OCR come "PERASS1", 47 sotto 11 giudici, 1 senza testo: 24/2000).'],
  ['11.8 Installazione da zero non testata', 'La procedura con requirements.lock (Python 3.12.4) non è ancora stata provata su una macchina pulita.'],
  ['11.9 Co-redattori: 19 vs 17', 'build_judges.py conta 19 pronunce con più redattori, il campo XML 17 (dal 2016): scarto non ancora ispezionato (escluse da D3).'],
];

const PROGRAMMA = [
  ['Introduzione alla data science e social media analysis', 'Data science sì; dati social no', 'Sezioni 1–2 (pipeline riproducibile, manifest SHA-256, validazione); tema da concordare'],
  ['Social network analysis', 'Applicata', 'Sezioni 2–5: DAG citazioni, bipartiti, co-sitting, HITS, PageRank, Leiden, Infomap, misure EM1421'],
  ['Lavorare con API', 'Applicato', 'Endpoint SPARQL Corte (esiti e sedute) e MediaWiki API (Wikipedia IT)'],
  ['Data and information visualisation', 'Applicata', 'Figure 1–10 (regole Tufte/guida §3) e rete interattiva 400 nodi'],
  ['Topic extraction', 'Applicata', 'Modello LDA a 20 temi su 46.126 massime + validazione NMI e stabilità'],
  ['Sentiment analysis', 'Applicata con esito negativo', 'Polarità delle citazioni (precisione 0,76 < 0,80 → arresto preregistrato)'],
];

const GLOSSARIO = [
  ['API', 'Servizio interrogabile da un programma (qui SPARQL della Corte e MediaWiki di Wikipedia).'],
  ['Collegio, relatore, redattore', 'Il collegio (11–15 giudici) decide; il relatore studia e riferisce; il redattore scrive le motivazioni approvate dal collegio.'],
  ['Correzione di Holm', 'Procedura per test multipli che mantiene sotto il 5% la probabilità di almeno un falso positivo.'],
  ['Esplorativo / Principale', 'Principale = fissato prima dei dati (unico per conclusioni formali); esplorativo = aggiunto o modificato dopo.'],
  ['HITS e PageRank', 'Algoritmi di centralità: HITS separa authority e hub; PageRank pesa i nodi citati da nodi a loro volta citati.'],
  ['In attività vs in carica', 'In attività = prima–ultima presenza in collegio (usato in tutte le analisi); in carica = date ufficiali anagrafiche (affette da errori).'],
  ['Indice di Gini', 'Disuguaglianza da 0 (citazioni uniformi) a 1 (tutto concentrato in una pronuncia).'],
  ['Modello nullo', 'Versioni rimescolate dei dati che conservano vincoli ovvi (tempo, uscite) per stabilire cosa produce il caso.'],
  ['Odds ratio (OR)', 'Rapporto tra odds di due gruppi: 1 = nessuna differenza; 2 = doppio; 0,5 = metà.'],
  ['Precisione e richiamo', 'Precisione = quota di citazioni trovate che sono vere; richiamo = quota di citazioni vere che vengono trovate.'],
  ['Regressione logistica condizionata', 'Modello di D3 che confronta citati e controlli esclusivamente dentro la stessa pronuncia che cita.'],
];

const PIPELINE_CMD = `python3.12 -m venv .venv
.venv/bin/pip install -r requirements.lock
.venv/bin/python -I src/ingest/download.py
.venv/bin/python src/ingest/inspect_raw.py
.venv/bin/python src/ingest/build_pronunce.py
.venv/bin/python src/extract/citations.py
.venv/bin/python src/extract/citations_massime.py
.venv/bin/python src/validation/evaluate.py test
.venv/bin/python src/validation/evaluate.py test2
.venv/bin/python src/judges/build_judges.py
.venv/bin/python src/analysis/topics.py
.venv/bin/python src/analysis/parametri.py
.venv/bin/python src/networks/build.py
.venv/bin/python src/networks/cositting.py
.venv/bin/python src/ingest/fetch_api.py
.venv/bin/python src/analysis/d1_pronunce.py
.venv/bin/python src/analysis/d2_d4_giudici.py
.venv/bin/python src/analysis/d2_strata_check.py
.venv/bin/python src/analysis/d3_memoria_collegiale.py
.venv/bin/python src/analysis/d3_absences.py
.venv/bin/python src/analysis/d3_full_check.py
.venv/bin/python src/analysis/precedent_succession.py
.venv/bin/python src/analysis/extras.py
.venv/bin/python src/analysis/course_measures.py
.venv/bin/python src/analysis/figures.py
.venv/bin/python src/analysis/interactive.py
.venv/bin/python src/report/report_numbers.py
.venv/bin/python src/report/plain_intros.py
.venv/bin/python src/courts/sizing.py
.venv/bin/python src/polarity/contexts.py
.venv/bin/python src/polarity/evaluate.py claude
.venv/bin/python -m pytest`;

export function SectionAppendices() {
  const [tab, setTab] = useState('limiti');
  const [glossQ, setGlossQ] = useState('');

  const filteredGloss = GLOSSARIO.filter(
    ([t, d]) =>
      t.toLowerCase().includes(glossQ.toLowerCase()) ||
      d.toLowerCase().includes(glossQ.toLowerCase())
  );

  return (
    <section>
      <SectionHeader
        id="discussione"
        num="7"
        title="Discussione, limiti, problemi noti e riproducibilità"
        subtitle="Valutazione critica dei limiti con direzione dell'effetto, inventario tecnico dei difetti aperti, mappatura EM1421, dichiarazione sull'uso dell'AI e glossario."
      />

      <div className="flex flex-wrap gap-1.5 mb-5">
        <TabButton active={tab === 'limiti'} onClick={() => setTab('limiti')}>
          12 Limiti dello studio
        </TabButton>
        <TabButton active={tab === 'noti'} onClick={() => setTab('noti')}>
          Problemi noti (§11)
        </TabButton>
        <TabButton active={tab === 'em1421'} onClick={() => setTab('em1421')}>
          Programma EM1421
        </TabButton>
        <TabButton active={tab === 'ripro'} onClick={() => setTab('ripro')}>
          Riproducibilità &amp; AI
        </TabButton>
        <TabButton active={tab === 'glossario'} onClick={() => setTab('glossario')}>
          Glossario
        </TabButton>
      </div>

      {tab === 'limiti' && (
        <div className="overflow-x-auto bg-white border border-rule rounded-sm">
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-rule bg-zinc-50 text-left font-mono text-muted">
                <th className="p-2.5">Limite</th>
                <th className="p-2.5">Risultato toccato</th>
                <th className="p-2.5">Direzione / Effetto</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100">
              {LIMITI.map(([l, t, e]) => (
                <tr key={l}>
                  <td className="p-2.5 font-medium text-ink align-top">{l}</td>
                  <td className="p-2.5 font-mono text-muted align-top whitespace-nowrap">{t}</td>
                  <td className="p-2.5 text-zinc-700 align-top">{e}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'noti' && (
        <div className="bg-white border border-rule rounded-sm divide-y divide-zinc-100 text-xs">
          {PROBLEMI_NOTI.map(([title, desc]) => (
            <div key={title} className="p-3">
              <div className="font-mono font-semibold text-ink mb-0.5">{title}</div>
              <div className="text-zinc-700 leading-relaxed">{desc}</div>
            </div>
          ))}
        </div>
      )}

      {tab === 'em1421' && (
        <div className="overflow-x-auto bg-white border border-rule rounded-sm">
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-rule bg-zinc-50 text-left font-mono text-muted">
                <th className="p-2.5">Voce programma 2026/27</th>
                <th className="p-2.5">Stato</th>
                <th className="p-2.5">Copertura nel progetto</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100">
              {PROGRAMMA.map(([v, s, d]) => (
                <tr key={v}>
                  <td className="p-2.5 font-medium text-ink">{v}</td>
                  <td className="p-2.5 font-mono text-muted whitespace-nowrap">{s}</td>
                  <td className="p-2.5 text-zinc-700">{d}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'ripro' && (
        <div className="space-y-4">
          <div className="bg-white border border-rule rounded-sm p-4 text-sm prose-editorial">
            <SubHeader title="Dichiarazione sull'uso dell'intelligenza artificiale" />
            <p className="!mb-2">
              Il lavoro è stato svolto con Claude Code sotto la direzione di Umberto Toraldo, che ha
              definito tema, domanda, estensioni e scelte di metodo (o le ha delegate, come
              registrato in <code className="font-mono text-xs">docs/decisions.md</code>). Tre
              conseguenze dirette: (1) le letture di riferimento per la validazione di citazioni e
              polarità sono dell&apos;assistente e non ancora umane; (2) le regole preregistrate del
              16/11 sono state scritte dallo stesso assistente che ha eseguito le analisi; (3) le
              regole del corso sull&apos;uso dell&apos;AI vanno ancora confermate dal docente.
            </p>
          </div>
          <div className="bg-white border border-rule rounded-sm p-4">
            <div className="text-xs font-mono uppercase tracking-wider text-muted mb-2">
              Sequenza completa di riproducibilità (Python 3.12.4, semi fissi)
            </div>
            <pre className="text-[11px] font-mono bg-zinc-900 text-zinc-100 p-3.5 rounded-sm overflow-x-auto leading-relaxed">
              {PIPELINE_CMD}
            </pre>
          </div>
        </div>
      )}

      {tab === 'glossario' && (
        <div className="bg-white border border-rule rounded-sm p-4">
          <input
            type="text"
            value={glossQ}
            onChange={(e) => setGlossQ(e.target.value)}
            placeholder="Filtra glossario..."
            className="mb-3 px-2.5 py-1.5 text-xs border border-rule rounded-sm w-64"
          />
          <dl className="divide-y divide-zinc-100 text-xs">
            {filteredGloss.map(([term, def]) => (
              <div key={term} className="py-2">
                <dt className="font-semibold text-ink">{term}</dt>
                <dd className="text-zinc-700 mt-0.5">{def}</dd>
              </div>
            ))}
          </dl>
        </div>
      )}
    </section>
  );
}
