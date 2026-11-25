import React, { useState } from 'react';
import { useProjectData } from './hooks/useProjectData';
import { SectionOverview } from './components/SectionOverview';
import { SectionMethods } from './components/SectionMethods';
import { SectionD3 } from './components/SectionD3';
import { SectionD1 } from './components/SectionD1';
import { SectionD2D4 } from './components/SectionD2D4';
import { SectionNetworks } from './components/SectionNetworks';
import { SectionPolarityCourts } from './components/SectionPolarityCourts';
import { SectionAppendices } from './components/SectionAppendices';

const NAV_ITEMS = [
  { id: 'sintesi', label: '0. Abstract e Sintesi' },
  { id: 'metodi', label: '1. Dati, Contesto e Qualità' },
  { id: 'd3', label: '2. D3 Memoria Collegiale' },
  { id: 'd1', label: '3. D1 Gerarchia & Durata' },
  { id: 'd2-d4', label: '4. D2 & D4 Giudici' },
  { id: 'reti', label: '5. Reti & Misure EM1421' },
  { id: 'polarita-corti', label: '6. Polarità & Altre Corti' },
  { id: 'discussione', label: '7. Limiti & Appendici' },
];

export default function App() {
  const { data, error, loading } = useProjectData();
  const [fullMode, setFullMode] = useState(true);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-paper text-muted font-mono text-xs">
        Caricamento dei 20 file JSON di analisi da ./data/…
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-paper p-6">
        <div className="max-w-lg w-full bg-white border border-red-200 p-5 rounded-sm text-sm">
          <div className="font-mono text-xs uppercase text-primary font-semibold mb-1">
            Errore caricamento dati
          </div>
          <p className="text-zinc-800 mb-3">{error}</p>
          <p className="text-xs text-muted mb-2">
            Assicurati di aver eseguito lo script di sincronizzazione dalla root della repository
            prima di avviare il server:
          </p>
          <pre className="text-xs font-mono bg-zinc-900 text-zinc-100 p-2.5 rounded-sm">
            python3 scripts/sync_site_data.py
          </pre>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-paper text-ink">
      {/* Top bar minimalista */}
      <header className="sticky top-0 z-30 bg-paper/95 backdrop-blur border-b border-rule">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-13 py-2.5 flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2.5">
            <span className="font-serif font-semibold text-sm sm:text-base text-ink">
              Chi fa il precedente?
            </span>
            <span className="hidden sm:inline font-mono text-[11px] text-muted">
              Corte costituzionale · 1956–2026
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            <button
              type="button"
              onClick={() => setFullMode(true)}
              className={`px-2.5 py-1 text-xs font-mono border rounded-sm ${
                fullMode ? 'bg-ink text-white border-ink' : 'bg-white text-muted border-rule'
              }`}
            >
              Articolo completo (IMRAD)
            </button>
            <button
              type="button"
              onClick={() => setFullMode(false)}
              className={`px-2.5 py-1 text-xs font-mono border rounded-sm ${
                !fullMode ? 'bg-ink text-white border-ink' : 'bg-white text-muted border-rule'
              }`}
            >
              Sintesi (Parte I)
            </button>
          </div>
        </div>
      </header>

      {/* Layout editoriale con TOC laterale su desktop */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8 lg:grid lg:grid-cols-[210px_minmax(0,1fr)] lg:gap-10">
        {fullMode && (
          <aside className="hidden lg:block">
            <nav className="sticky top-20 space-y-1">
              <div className="font-mono text-[10px] uppercase tracking-widest text-muted mb-2.5">
                Indice
              </div>
              {NAV_ITEMS.map((item) => (
                <a
                  key={item.id}
                  href={`#${item.id}`}
                  className="block py-1 text-xs text-muted hover:text-ink transition-colors"
                >
                  {item.label}
                </a>
              ))}
              <div className="pt-4 mt-4 border-t border-rule text-[11px] text-muted leading-relaxed">
                <div>Umberto Toraldo</div>
                <div>Ca&apos; Foscari · EM1421</div>
                <div className="font-mono text-[10px] mt-1">Dati: CC BY-SA 3.0</div>
              </div>
            </nav>
          </aside>
        )}

        <main className={fullMode ? 'min-w-0' : 'max-w-3xl mx-auto lg:col-span-2'}>
          {/* Titolo articolo */}
          <div className="pb-6 mb-6 border-b border-rule">
            <div className="font-mono text-xs uppercase tracking-wider text-muted mb-2">
              Social Media and Web Analytics (EM1421) · Università Ca&apos; Foscari Venezia ·
              Novembre 2026
            </div>
            <h1 className="font-serif text-3xl sm:text-4xl font-medium tracking-tight text-ink leading-tight">
              Chi fa il precedente? La rete delle pronunce e dei giudici della Corte costituzionale,
              1956–2026
            </h1>
            <p className="mt-2.5 text-sm text-muted">
              Umberto Toraldo · Lavoro svolto con Claude Code · Stato: analisi complete, in attesa
              di approvazione del docente e validazione umana delle citazioni.
            </p>
          </div>

          <SectionOverview data={data} fullMode={fullMode} />

          {fullMode && (
            <>
              <SectionMethods data={data} />
              <SectionD3 data={data} />
              <SectionD1 data={data} />
              <SectionD2D4 data={data} />
              <SectionNetworks data={data} />
              <SectionPolarityCourts data={data} />
              <SectionAppendices />
            </>
          )}

          <footer className="mt-14 pt-6 border-t border-rule text-xs text-muted flex flex-wrap justify-between gap-2">
            <span>
              Fonte dati originali: Corte costituzionale (dati.cortecostituzionale.it), licenza CC
              BY-SA 3.0.
            </span>
            <span className="font-mono">20 JSON sincronizzati da reports/</span>
          </footer>
        </main>
      </div>
    </div>
  );
}
