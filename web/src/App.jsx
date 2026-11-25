import React, { useState } from 'react';
import { useProjectData } from './hooks/useProjectData';
import { AbstractSection, SectionIntroduction, SectionMethods } from './components/SectionIntroMethods';
import { SectionResults } from './components/SectionResults';
import { SectionDiscussionAppendices } from './components/SectionDiscussionAppendices';

const TOC = [
  { id: 'abstract', label: 'Abstract' },
  { id: 'introduzione', label: '1. Introduzione' },
  { id: 'metodi', label: '2. Metodi' },
  { id: 'risultati', label: '3. Risultati' },
  { id: 'risultati-d3', label: '   3.1 D3 (Primario)', sub: true },
  { id: 'risultati-d1', label: '   3.2 D1 & D1b', sub: true },
  { id: 'risultati-d2', label: '   3.3 D2 & D4', sub: true },
  { id: 'risultati-reti', label: '   3.4 Reti & EM1421', sub: true },
  { id: 'risultati-polarita', label: '   3.5 Polarità & Corti', sub: true },
  { id: 'discussione', label: '4. Discussione e Limiti' },
  { id: 'appendici', label: '5. Appendici (A–D)' },
  { id: 'bibliografia', label: '6. Bibliografia' },
];

export default function App() {
  const { data, error, loading } = useProjectData();
  const [view, setView] = useState('imrad'); // 'imrad' | 'abstract_only'

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-paper text-muted font-mono text-xs">
        Caricamento dei 20 file JSON da ./data/…
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-paper p-6">
        <div className="max-w-lg w-full bg-white border border-red-200 p-5 text-sm">
          <div className="font-mono text-xs uppercase text-primary font-semibold mb-1">
            Errore caricamento dati
          </div>
          <p className="text-zinc-800 mb-3">{error}</p>
          <pre className="text-xs font-mono bg-zinc-900 text-zinc-100 p-2.5">
            python3 scripts/sync_site_data.py
          </pre>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-paper text-ink">
      <header className="sticky top-0 z-30 bg-paper/95 backdrop-blur border-b border-rule">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-2.5 flex flex-wrap items-center justify-between gap-2">
          <div className="font-serif text-sm sm:text-base font-medium text-ink">
            Chi fa il precedente?{' '}
            <span className="hidden sm:inline font-sans text-xs text-muted font-normal ml-1.5">
              Corte costituzionale, 1956–2026
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            <button
              type="button"
              onClick={() => setView('imrad')}
              className={`px-2.5 py-1 text-[11px] font-mono border rounded-[2px] ${
                view === 'imrad' ? 'bg-ink text-white border-ink' : 'bg-white text-muted border-rule'
              }`}
            >
              Articolo IMRAD completo
            </button>
            <button
              type="button"
              onClick={() => setView('abstract_only')}
              className={`px-2.5 py-1 text-[11px] font-mono border rounded-[2px] ${
                view === 'abstract_only' ? 'bg-ink text-white border-ink' : 'bg-white text-muted border-rule'
              }`}
            >
              Solo Abstract
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-10 lg:grid lg:grid-cols-[195px_minmax(0,1fr)] lg:gap-12">
        {view === 'imrad' && (
          <aside className="hidden lg:block">
            <nav className="sticky top-20 space-y-1">
              <div className="font-mono text-[10px] uppercase tracking-widest text-muted mb-2">
                Struttura IMRAD
              </div>
              {TOC.map((item) => (
                <a
                  key={item.id}
                  href={`#${item.id}`}
                  className={`block py-0.5 text-xs transition-colors hover:text-ink ${
                    item.sub ? 'pl-3 text-[11px] text-zinc-400' : 'text-muted'
                  }`}
                >
                  {item.label}
                </a>
              ))}
            </nav>
          </aside>
        )}

        <article className={view === 'imrad' ? 'min-w-0 max-w-[780px]' : 'max-w-[760px] mx-auto lg:col-span-2'}>
          <header className="pb-6 border-b border-rule">
            <div className="font-mono text-[11px] uppercase tracking-wider text-muted mb-2">
              Social Media and Web Analytics (EM1421) · Università Ca&apos; Foscari Venezia · Novembre 2026
            </div>
            <h1 className="font-serif text-3xl sm:text-[2.35rem] font-medium tracking-tight text-ink leading-[1.18]">
              Chi fa il precedente? Pronunce e giudici della Corte costituzionale italiana, 1956–2026
            </h1>
            <div className="mt-3 text-sm text-muted">
              <strong className="text-ink font-medium">Umberto Toraldo</strong> · Lavoro svolto con
              Claude Code · Dati: portale open data Corte costituzionale (CC BY-SA 3.0)
            </div>
          </header>

          <AbstractSection data={data} />

          {view === 'imrad' && (
            <>
              <SectionIntroduction />
              <SectionMethods data={data} />
              <SectionResults data={data} />
              <SectionDiscussionAppendices data={data} />
            </>
          )}

          <footer className="mt-16 pt-5 border-t border-rule text-[11px] text-muted flex flex-wrap justify-between gap-2">
            <span>Fonte dati: Corte costituzionale (dati.cortecostituzionale.it), CC BY-SA 3.0.</span>
            <span className="font-mono">Caricamento dinamico da reports/*.json</span>
          </footer>
        </article>
      </div>
    </div>
  );
}
