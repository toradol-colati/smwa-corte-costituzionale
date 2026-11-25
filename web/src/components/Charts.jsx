import React, { useMemo, useState } from 'react';
import { fmtCI, fmtDec, fmtInt, fmtP, fmtPct } from '../utils/format';

/* 1. Forest Plot D3 (tutte le 15 specificazioni reali + contrasto self_drafted) */
export function ForestPlotD3({ d3 }) {
  const [view, setView] = useState('sat'); // 'sat' | 'contrast'
  const [selectedIdx, setSelectedIdx] = useState(0);

  const rows = useMemo(() => {
    const list = [
      {
        key: 'primary',
        label: 'Risultato principale: sedeva nel collegio, senza scriverlo',
        isPrimary: true,
        isExploratory: false,
        item: d3.primary,
      },
      ...Object.entries(d3.variants).map(([k, v]) => ({
        key: k,
        label: k,
        isPrimary: false,
        isExploratory: k.includes('esplorativo'),
        item: v,
      })),
    ];
    return list;
  }, [d3]);

  const active = rows[selectedIdx] || rows[0];

  if (view === 'contrast') {
    const p = d3.primary.coef;
    const norm = d3.variants['controllo per norma impugnata in comune (esplorativo)'].coef;
    const par = d3.variants['materia fine: parametri costituzionali (esplorativo)'].coef;
    const items = [
      {
        label: 'Sedeva nel collegio, non ha scritto (principale)',
        c: p.sat_not_drafted,
        color: '#71717A',
      },
      {
        label: 'Ha scritto lui — modello base (esplorativo)',
        c: p.self_drafted,
        color: '#991B1B',
      },
      {
        label: 'Ha scritto lui — a parità di parametri cost. (esplorativo)',
        c: par.self_drafted,
        color: '#1E40AF',
      },
      {
        label: 'Ha scritto lui — a parità di norma impugnata (esplorativo)',
        c: norm.self_drafted,
        color: '#1E40AF',
      },
    ];

    const W = 720;
    const H = 215;
    const padL = 320;
    const padR = 30;
    const minLog = Math.log(0.75);
    const maxLog = Math.log(7.0);
    const xOf = (v) => padL + ((Math.log(v) - minLog) / (maxLog - minLog)) * (W - padL - padR);
    const ticks = [0.8, 1, 2, 3, 4, 6];

    return (
      <div>
        <div className="flex gap-2 mb-3">
          <button
            type="button"
            onClick={() => setView('sat')}
            className="px-2.5 py-1 text-xs font-mono border border-rule bg-paper text-muted hover:text-ink rounded-sm"
          >
            Tutte le 15 specificazioni (collegio)
          </button>
          <button
            type="button"
            onClick={() => setView('contrast')}
            className="px-2.5 py-1 text-xs font-mono border border-ink bg-ink text-white rounded-sm"
          >
            Contrasto: redattore vs collegio (scala log)
          </button>
        </div>
        <svg viewBox={`0 0 ${W} ${H}`} className="w-full max-w-[760px] h-auto">
          <line x1={xOf(1)} x2={xOf(1)} y1={14} y2={H - 36} stroke="#18181B" strokeWidth="1.2" />
          {ticks.map((t) => (
            <g key={t}>
              <line x1={xOf(t)} x2={xOf(t)} y1={H - 36} y2={H - 31} stroke="#71717A" />
              <text
                x={xOf(t)}
                y={H - 16}
                textAnchor="middle"
                fontSize="11"
                fill="#52525B"
                className="font-mono"
              >
                {fmtDec(t, t < 1 ? 1 : 0)}
              </text>
            </g>
          ))}
          <line x1={padL} x2={W - padR} y1={H - 36} y2={H - 36} stroke="#D4D4D8" />
          {items.map((it, i) => {
            const y = 34 + i * 38;
            return (
              <g key={it.label}>
                <text x={padL - 12} y={y + 4} textAnchor="end" fontSize="11.5" fill="#27272A">
                  {it.label}
                </text>
                <line
                  x1={xOf(it.c.lo)}
                  x2={xOf(it.c.hi)}
                  y1={y}
                  y2={y}
                  stroke={it.color}
                  strokeWidth="2.2"
                />
                <line
                  x1={xOf(it.c.lo)}
                  x2={xOf(it.c.lo)}
                  y1={y - 5}
                  y2={y + 5}
                  stroke={it.color}
                  strokeWidth="1.5"
                />
                <line
                  x1={xOf(it.c.hi)}
                  x2={xOf(it.c.hi)}
                  y1={y - 5}
                  y2={y + 5}
                  stroke={it.color}
                  strokeWidth="1.5"
                />
                <circle cx={xOf(it.c.or)} cy={y} r="4.5" fill={it.color} />
                <text
                  x={xOf(it.c.hi) + 8}
                  y={y + 4}
                  fontSize="11"
                  fill="#52525B"
                  className="font-mono"
                >
                  {fmtDec(it.c.or)} ({fmtCI(it.c.lo, it.c.hi)})
                </text>
              </g>
            );
          })}
          <text
            x={(padL + W - padR) / 2}
            y={H - 2}
            textAnchor="middle"
            fontSize="11"
            fill="#52525B"
          >
            Odds ratio, scala logaritmica (1 = come un precedente deciso in assenza del giudice)
          </text>
        </svg>
      </div>
    );
  }

  const W = 760;
  const rowH = 27;
  const H = 36 + rows.length * rowH + 34;
  const padL = 370;
  const padR = 95;
  const minX = 0.74;
  const maxX = 1.36;
  const xOf = (v) => padL + ((v - minX) / (maxX - minX)) * (W - padL - padR);
  const ticks = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3];

  const cSat = active.item.coef.sat_not_drafted;
  const cSelf = active.item.coef.self_drafted;

  return (
    <div>
      <div className="flex flex-wrap gap-2 mb-3">
        <button
          type="button"
          onClick={() => setView('sat')}
          className="px-2.5 py-1 text-xs font-mono border border-ink bg-ink text-white rounded-sm"
        >
          Tutte le 15 specificazioni (collegio)
        </button>
        <button
          type="button"
          onClick={() => setView('contrast')}
          className="px-2.5 py-1 text-xs font-mono border border-rule bg-paper text-muted hover:text-ink rounded-sm"
        >
          Contrasto: redattore vs collegio (scala log)
        </button>
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} className="w-full max-w-[820px] h-auto select-none">
        <line x1={xOf(1)} x2={xOf(1)} y1={14} y2={H - 34} stroke="#18181B" strokeWidth="1.2" />
        {ticks.map((t) => (
          <g key={t}>
            <line x1={xOf(t)} x2={xOf(t)} y1={14} y2={H - 34} stroke="#F4F4F5" strokeWidth="1" />
            <line x1={xOf(t)} x2={xOf(t)} y1={H - 34} y2={H - 29} stroke="#71717A" />
            <text
              x={xOf(t)}
              y={H - 16}
              textAnchor="middle"
              fontSize="11"
              fill="#52525B"
              className="font-mono"
            >
              {fmtDec(t, 1)}
            </text>
          </g>
        ))}
        <line x1={padL} x2={W - padR} y1={H - 34} y2={H - 34} stroke="#D4D4D8" />

        {rows.map((r, i) => {
          const c = r.item.coef.sat_not_drafted;
          const y = 26 + i * rowH;
          const isSel = i === selectedIdx;
          const color = r.isPrimary ? '#991B1B' : r.isExploratory ? '#1E40AF' : '#71717A';
          return (
            <g
              key={r.key}
              onClick={() => setSelectedIdx(i)}
              onMouseEnter={() => setSelectedIdx(i)}
              className="cursor-pointer"
            >
              <rect
                x={0}
                y={y - rowH / 2}
                width={W}
                height={rowH}
                fill={isSel ? '#F4F4F5' : 'transparent'}
              />
              <text
                x={padL - 10}
                y={y + 4}
                textAnchor="end"
                fontSize="11"
                fontWeight={r.isPrimary || isSel ? '600' : '400'}
                fill={r.isPrimary ? '#991B1B' : '#27272A'}
              >
                {r.label.length > 56 ? `${r.label.slice(0, 54)}…` : r.label}
              </text>
              <line
                x1={xOf(c.lo)}
                x2={xOf(c.hi)}
                y1={y}
                y2={y}
                stroke={color}
                strokeWidth={r.isPrimary ? 2.4 : 1.7}
              />
              <line x1={xOf(c.lo)} x2={xOf(c.lo)} y1={y - 4} y2={y + 4} stroke={color} />
              <line x1={xOf(c.hi)} x2={xOf(c.hi)} y1={y - 4} y2={y + 4} stroke={color} />
              <circle cx={xOf(c.or)} cy={y} r={r.isPrimary ? 4.5 : 3.5} fill={color} />
              <text
                x={W - padR + 8}
                y={y + 4}
                fontSize="10.5"
                fill="#52525B"
                className="font-mono"
              >
                {fmtDec(c.or)} ({fmtCI(c.lo, c.hi)})
              </text>
            </g>
          );
        })}

        <text
          x={(padL + W - padR) / 2}
          y={H - 2}
          textAnchor="middle"
          fontSize="11"
          fill="#52525B"
        >
          Odds ratio di "sedeva nel collegio senza scriverlo" (1 = nessun effetto), IC 95%
        </text>
      </svg>

      <div className="mt-3 p-3 bg-paper border border-rule rounded-sm text-xs font-mono grid grid-cols-2 sm:grid-cols-4 gap-2">
        <div>
          <span className="text-muted block">Specificazione</span>
          <span className="text-ink font-sans font-medium">{active.label}</span>
        </div>
        <div>
          <span className="text-muted block">Collegio (esatto / Breslow)</span>
          <span className="text-primary font-semibold">
            {fmtDec(cSat.or)} ({fmtCI(cSat.lo, cSat.hi)})
          </span>
          <span className="text-muted block">
            p = {fmtP(cSat.p)} · Breslow {fmtDec(cSat.or_breslow)}
          </span>
        </div>
        <div>
          <span className="text-muted block">Redatto dallo stesso giudice</span>
          <span className="text-ink font-semibold">
            {cSelf ? `${fmtDec(cSelf.or)} (${fmtCI(cSelf.lo, cSelf.hi)})` : 'escluso'}
          </span>
          {cSelf && <span className="text-muted block">Breslow {fmtDec(cSelf.or_breslow)}</span>}
        </div>
        <div>
          <span className="text-muted block">Strati / Citazioni / Assenti</span>
          <span className="text-ink">
            {fmtInt(active.item.strata)} / {fmtInt(active.item.cases)} /{' '}
            {fmtInt(active.item.cases_absent)}
          </span>
          <span className="text-muted block">
            {active.item.clusters} giudici · conv: {active.item.converged ? 'sì' : 'no*'}
          </span>
        </div>
      </div>
    </div>
  );
}

/* 2. Grafico a barre concentrazione D1 (assi rigorosamente da 0) */
export function ConcentrationBarChart({ d1 }) {
  const [nullMode, setNullMode] = useState('year'); // 'year' | 'type'
  const src = nullMode === 'year' ? d1.concentration : d1.concentration_by_type;

  const panels = [
    {
      title: "Quota citazioni all'1% più citato",
      obs: src.top1_share.observed * 100,
      nMean: src.top1_share.null_mean * 100,
      nLo: src.top1_share.null_lo * 100,
      nHi: src.top1_share.null_hi * 100,
      maxY: 12,
      fmt: (v) => `${fmtDec(v, 1)}%`,
    },
    {
      title: 'Indice di Gini',
      obs: src.gini.observed,
      nMean: src.gini.null_mean,
      nLo: src.gini.null_lo,
      nHi: src.gini.null_hi,
      maxY: 0.75,
      fmt: (v) => fmtDec(v, 2),
    },
    {
      title: 'Pronunce mai citate',
      obs: src.never_cited.observed * 100,
      nMean: src.never_cited.null_mean * 100,
      nLo: src.never_cited.null_lo * 100,
      nHi: src.never_cited.null_hi * 100,
      maxY: 35,
      fmt: (v) => `${fmtDec(v, 1)}%`,
    },
  ];

  return (
    <div>
      <div className="flex flex-wrap gap-2 mb-3">
        <button
          type="button"
          onClick={() => setNullMode('year')}
          className={`px-2.5 py-1 text-xs font-mono border rounded-sm ${
            nullMode === 'year'
              ? 'bg-ink text-white border-ink'
              : 'bg-paper text-muted border-rule'
          }`}
        >
          Nullo: stesso anno (preregistrato)
        </button>
        <button
          type="button"
          onClick={() => setNullMode('type')}
          className={`px-2.5 py-1 text-xs font-mono border rounded-sm ${
            nullMode === 'type'
              ? 'bg-ink text-white border-ink'
              : 'bg-paper text-muted border-rule'
          }`}
        >
          Nullo: stesso anno e tipo (esplorativo)
        </button>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {panels.map((p) => {
          const H = 175;
          const W = 210;
          const padB = 28;
          const padT = 22;
          const yOf = (v) => H - padB - (v / p.maxY) * (H - padB - padT);
          return (
            <div key={p.title} className="border border-zinc-100 p-2 rounded-sm">
              <div className="text-xs font-medium text-center text-ink mb-1">{p.title}</div>
              <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto">
                <line x1={28} x2={W - 10} y1={yOf(0)} y2={yOf(0)} stroke="#A1A1AA" />
                <line x1={28} x2={28} y1={padT} y2={yOf(0)} stroke="#A1A1AA" />
                {/* Barra Osservato */}
                <rect
                  x={48}
                  y={yOf(p.obs)}
                  width={48}
                  height={yOf(0) - yOf(p.obs)}
                  fill="#991B1B"
                />
                <text
                  x={72}
                  y={yOf(p.obs) - 5}
                  textAnchor="middle"
                  fontSize="11"
                  fontWeight="600"
                  fill="#991B1B"
                  className="font-mono"
                >
                  {p.fmt(p.obs)}
                </text>
                <text x={72} y={H - 10} textAnchor="middle" fontSize="10.5" fill="#27272A">
                  Osservato
                </text>
                {/* Barra Nullo */}
                <rect
                  x={124}
                  y={yOf(p.nMean)}
                  width={48}
                  height={yOf(0) - yOf(p.nMean)}
                  fill="#A1A1AA"
                />
                <line
                  x1={148}
                  x2={148}
                  y1={yOf(p.nHi)}
                  y2={yOf(p.nLo)}
                  stroke="#18181B"
                  strokeWidth="1.5"
                />
                <text
                  x={148}
                  y={yOf(p.nHi) - 5}
                  textAnchor="middle"
                  fontSize="11"
                  fill="#52525B"
                  className="font-mono"
                >
                  {p.fmt(p.nMean)}
                </text>
                <text x={148} y={H - 10} textAnchor="middle" fontSize="10.5" fill="#52525B">
                  Atteso
                </text>
              </svg>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* 3. Curva di invecchiamento D1b (61 punti reali) + toggle Kaplan-Meier */
export function AgeingSurvivalChart({ d1 }) {
  const [mode, setMode] = useState('rate'); // 'rate' | 'km'
  const [hoverAge, setHoverAge] = useState(1);

  const rates = d1.ageing.relative_rate_by_age;
  const W = 720;
  const H = 260;
  const padL = 56;
  const padR = 24;
  const padT = 18;
  const padB = 38;

  if (mode === 'km') {
    const pts = Object.entries(d1.survival.km)
      .map(([k, v]) => ({ age: Number(k), s: v }))
      .sort((a, b) => a.age - b.age);
    const xOf = (a) => padL + (a / 50) * (W - padL - padR);
    const yOf = (s) => H - padB - s * (H - padB - padT);
    const path = pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${xOf(p.age)},${yOf(p.s)}`).join(' ');

    return (
      <div>
        <div className="flex gap-2 mb-3">
          <button
            type="button"
            onClick={() => setMode('rate')}
            className="px-2.5 py-1 text-xs font-mono border border-rule bg-paper text-muted rounded-sm"
          >
            Frequenza relativa per età (0–60 anni)
          </button>
          <button
            type="button"
            onClick={() => setMode('km')}
            className="px-2.5 py-1 text-xs font-mono border border-ink bg-ink text-white rounded-sm"
          >
            Sopravvivenza Kaplan–Meier
          </button>
        </div>
        <svg viewBox={`0 0 ${W} ${H}`} className="w-full max-w-[760px] h-auto">
          {[0, 0.25, 0.5, 0.75, 1].map((y) => (
            <g key={y}>
              <line x1={padL} x2={W - padR} y1={yOf(y)} y2={yOf(y)} stroke="#F4F4F5" />
              <text
                x={padL - 8}
                y={yOf(y) + 4}
                textAnchor="end"
                fontSize="10.5"
                fill="#52525B"
                className="font-mono"
              >
                {fmtPct(y, 0)}
              </text>
            </g>
          ))}
          <line x1={padL} x2={W - padR} y1={yOf(0.5)} y2={yOf(0.5)} stroke="#D4D4D8" strokeDasharray="4 3" />
          <line x1={padL} x2={W - padR} y1={H - padB} y2={H - padB} stroke="#A1A1AA" />
          <line x1={padL} x2={padL} y1={padT} y2={H - padB} stroke="#A1A1AA" />
          <path d={path} fill="none" stroke="#991B1B" strokeWidth="2.2" />
          {pts.map((p) => (
            <g key={p.age}>
              <circle cx={xOf(p.age)} cy={yOf(p.s)} r="3.5" fill="#991B1B" />
              <text
                x={xOf(p.age)}
                y={yOf(p.s) - 8}
                textAnchor="middle"
                fontSize="10"
                fill="#27272A"
                className="font-mono"
              >
                {fmtPct(p.s, 1)}
              </text>
              <text
                x={xOf(p.age)}
                y={H - 18}
                textAnchor="middle"
                fontSize="10.5"
                fill="#52525B"
                className="font-mono"
              >
                {p.age}
              </text>
            </g>
          ))}
          <text x={(padL + W - padR) / 2} y={H - 2} textAnchor="middle" fontSize="11" fill="#52525B">
            Anni dal deposito (mediana: tutte {fmtDec(d1.survival.median, 0)} anni · sentenze{' '}
            {fmtDec(d1.survival.sentenze.median, 0)} · ordinanze {fmtDec(d1.survival.ordinanze.median, 0)})
          </text>
        </svg>
      </div>
    );
  }

  const maxAge = rates.length - 1;
  const minLog = Math.log10(0.08);
  const maxLog = Math.log10(7);
  const xOf = (a) => padL + (a / maxAge) * (W - padL - padR);
  const yOf = (r) =>
    H - padB - ((Math.log10(Math.max(0.08, r)) - minLog) / (maxLog - minLog)) * (H - padB - padT);
  const path = rates.map((r, a) => `${a === 0 ? 'M' : 'L'}${xOf(a)},${yOf(r)}`).join(' ');

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setMode('rate')}
            className="px-2.5 py-1 text-xs font-mono border border-ink bg-ink text-white rounded-sm"
          >
            Frequenza relativa per età (0–60 anni)
          </button>
          <button
            type="button"
            onClick={() => setMode('km')}
            className="px-2.5 py-1 text-xs font-mono border border-rule bg-paper text-muted rounded-sm"
          >
            Sopravvivenza Kaplan–Meier
          </button>
        </div>
        <div className="text-xs font-mono text-muted">
          Età <strong className="text-ink">{hoverAge} anni</strong>: frequenza{' '}
          <strong className="text-primary">{fmtDec(rates[hoverAge], 2)}×</strong> rispetto al caso
        </div>
      </div>

      <svg
        viewBox={`0 0 ${W} ${H}`}
        className="w-full max-w-[760px] h-auto"
        onMouseMove={(e) => {
          const rect = e.currentTarget.getBoundingClientRect();
          const rx = ((e.clientX - rect.left) / rect.width) * W;
          const age = Math.round(((rx - padL) / (W - padL - padR)) * maxAge);
          if (age >= 0 && age <= maxAge) setHoverAge(age);
        }}
      >
        {[0.1, 0.2, 0.5, 1, 2, 5].map((y) => (
          <g key={y}>
            <line
              x1={padL}
              x2={W - padR}
              y1={yOf(y)}
              y2={yOf(y)}
              stroke={y === 1 ? '#71717A' : '#F4F4F5'}
              strokeDasharray={y === 1 ? '4 3' : undefined}
            />
            <text
              x={padL - 8}
              y={yOf(y) + 4}
              textAnchor="end"
              fontSize="10.5"
              fill="#52525B"
              className="font-mono"
            >
              {fmtDec(y, y < 1 ? 1 : 0)}×
            </text>
          </g>
        ))}
        <line x1={padL} x2={W - padR} y1={H - padB} y2={H - padB} stroke="#A1A1AA" />
        <line x1={padL} x2={padL} y1={padT} y2={H - padB} stroke="#A1A1AA" />
        {[0, 5, 10, 20, 30, 40, 50, 60].map((a) => (
          <text
            key={a}
            x={xOf(a)}
            y={H - 18}
            textAnchor="middle"
            fontSize="10.5"
            fill="#52525B"
            className="font-mono"
          >
            {a}
          </text>
        ))}
        <path d={path} fill="none" stroke="#991B1B" strokeWidth="2.1" />
        <line
          x1={xOf(hoverAge)}
          x2={xOf(hoverAge)}
          y1={padT}
          y2={H - padB}
          stroke="#1E40AF"
          strokeWidth="1"
          strokeDasharray="2 2"
        />
        <circle cx={xOf(hoverAge)} cy={yOf(rates[hoverAge])} r="4" fill="#1E40AF" />
        <text x={W - padR - 4} y={yOf(1) - 6} textAnchor="end" fontSize="10" fill="#71717A">
          1× = scelta uniforme tra precedenti disponibili
        </text>
        <text x={(padL + W - padR) / 2} y={H - 2} textAnchor="middle" fontSize="11" fill="#52525B">
          Età del precedente (anni, scala y logaritmica)
        </text>
      </svg>
    </div>
  );
}

/* 4. Grafico citazioni uscenti per decennio (da 0) */
export function DecadeOutChart({ byDecade }) {
  const entries = Object.entries(byDecade);
  const W = 680;
  const H = 200;
  const padL = 44;
  const padR = 16;
  const padT = 22;
  const padB = 34;
  const maxY = 16;
  const bw = (W - padL - padR) / entries.length;
  const yOf = (v) => H - padB - (v / maxY) * (H - padB - padT);

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full max-w-[700px] h-auto">
      {[0, 4, 8, 12, 16].map((y) => (
        <g key={y}>
          <line x1={padL} x2={W - padR} y1={yOf(y)} y2={yOf(y)} stroke="#F4F4F5" />
          <text x={padL - 8} y={yOf(y) + 4} textAnchor="end" fontSize="10.5" fill="#52525B" className="font-mono">
            {y}
          </text>
        </g>
      ))}
      <line x1={padL} x2={W - padR} y1={yOf(0)} y2={yOf(0)} stroke="#A1A1AA" />
      {entries.map(([dec, val], i) => {
        const x = padL + i * bw + bw * 0.2;
        const w = bw * 0.6;
        return (
          <g key={dec}>
            <rect x={x} y={yOf(val)} width={w} height={yOf(0) - yOf(val)} fill="#1E40AF" />
            <text
              x={x + w / 2}
              y={yOf(val) - 5}
              textAnchor="middle"
              fontSize="10.5"
              fill="#18181B"
              className="font-mono"
            >
              {fmtDec(val, 1)}
            </text>
            <text
              x={x + w / 2}
              y={H - 14}
              textAnchor="middle"
              fontSize="10.5"
              fill="#52525B"
              className="font-mono"
            >
              {dec}s
            </text>
          </g>
        );
      })}
    </svg>
  );
}

/* 5. Grafico D2 Dot-and-Whisker (tutti i 113/74 giudici) + Scatter Post-Mandato */
export function D2JudgeChart({ specData }) {
  const [chartView, setChartView] = useState('rank'); // 'rank' | 'post'
  const [hoverJudge, setHoverJudge] = useState(null);

  const sorted = useMemo(
    () => [...specData.table].sort((a, b) => a.rapporto - b.rapporto),
    [specData]
  );

  const postJudges = useMemo(
    () =>
      specData.table.filter(
        (j) =>
          j.rapporto_durante !== null &&
          j.rapporto_durante !== undefined &&
          j.rapporto_post !== null &&
          j.rapporto_post !== undefined &&
          j.rapporto_durante > 0 &&
          j.rapporto_post > 0
      ),
    [specData]
  );

  const W = 760;
  const H = 290;
  const padL = 50;
  const padR = 20;
  const padT = 20;
  const padB = 38;

  if (chartView === 'post') {
    const minV = 0.4;
    const maxV = 2.4;
    const xOf = (v) =>
      padL + ((Math.log(v) - Math.log(minV)) / (Math.log(maxV) - Math.log(minV))) * (W - padL - padR);
    const yOf = (v) =>
      H - padB - ((Math.log(v) - Math.log(minV)) / (Math.log(maxV) - Math.log(minV))) * (H - padB - padT);
    const ticks = [0.5, 0.75, 1, 1.5, 2];

    return (
      <div>
        <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => setChartView('rank')}
              className="px-2.5 py-1 text-xs font-mono border border-rule bg-paper text-muted rounded-sm"
            >
              Tutti i {sorted.length} giudici (IC 95%)
            </button>
            <button
              type="button"
              onClick={() => setChartView('post')}
              className="px-2.5 py-1 text-xs font-mono border border-ink bg-ink text-white rounded-sm"
            >
              Durante vs 10 anni dopo ({postJudges.length} giudici)
            </button>
          </div>
          {hoverJudge && (
            <div className="text-xs font-mono text-ink">
              <strong>{hoverJudge.nome}</strong> · durante {fmtDec(hoverJudge.rapporto_durante)} · dopo{' '}
              {fmtDec(hoverJudge.rapporto_post)}
            </div>
          )}
        </div>
        <svg viewBox={`0 0 ${W} ${H}`} className="w-full max-w-[780px] h-auto">
          {ticks.map((t) => (
            <g key={t}>
              <line x1={padL} x2={W - padR} y1={yOf(t)} y2={yOf(t)} stroke="#F4F4F5" />
              <line x1={xOf(t)} x2={xOf(t)} y1={padT} y2={H - padB} stroke="#F4F4F5" />
              <text x={padL - 8} y={yOf(t) + 4} textAnchor="end" fontSize="10" fill="#52525B" className="font-mono">
                {fmtDec(t, t === 1 ? 0 : 2)}
              </text>
              <text x={xOf(t)} y={H - 18} textAnchor="middle" fontSize="10" fill="#52525B" className="font-mono">
                {fmtDec(t, t === 1 ? 0 : 2)}
              </text>
            </g>
          ))}
          <line x1={xOf(minV)} y1={yOf(minV)} x2={xOf(maxV)} y2={yOf(maxV)} stroke="#A1A1AA" strokeDasharray="4 3" />
          <line x1={padL} x2={W - padR} y1={H - padB} y2={H - padB} stroke="#A1A1AA" />
          <line x1={padL} x2={padL} y1={padT} y2={H - padB} stroke="#A1A1AA" />
          {postJudges.map((j) => {
            const sig = j.p_holm < 0.05;
            return (
              <circle
                key={j.judge_id}
                cx={xOf(j.rapporto_durante)}
                cy={yOf(j.rapporto_post)}
                r={hoverJudge?.judge_id === j.judge_id ? 6 : 4}
                fill={sig ? '#1E40AF' : '#71717A'}
                fillOpacity={0.75}
                stroke="#fff"
                strokeWidth="0.8"
                className="cursor-pointer"
                onMouseEnter={() => setHoverJudge(j)}
              />
            );
          })}
          <text x={(padL + W - padR) / 2} y={H - 2} textAnchor="middle" fontSize="11" fill="#52525B">
            Rapporto osservate / attese durante il mandato (asse x) vs nei 10 anni dopo (asse y)
          </text>
        </svg>
      </div>
    );
  }

  const minY = 0.35;
  const maxY = 2.3;
  const xOf = (i) => padL + (i / Math.max(1, sorted.length - 1)) * (W - padL - padR);
  const yOf = (v) =>
    H - padB - ((Math.log(Math.max(minY, v)) - Math.log(minY)) / (Math.log(maxY) - Math.log(minY))) * (H - padB - padT);

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setChartView('rank')}
            className="px-2.5 py-1 text-xs font-mono border border-ink bg-ink text-white rounded-sm"
          >
            Tutti i {sorted.length} giudici (IC 95%)
          </button>
          <button
            type="button"
            onClick={() => setChartView('post')}
            className="px-2.5 py-1 text-xs font-mono border border-rule bg-paper text-muted rounded-sm"
          >
            Durante vs 10 anni dopo ({postJudges.length} giudici)
          </button>
        </div>
        <div className="text-xs font-mono text-muted">
          {hoverJudge ? (
            <>
              <strong className="text-ink">{hoverJudge.nome}</strong>: {fmtDec(hoverJudge.rapporto)} (
              {fmtCI(hoverJudge.lo, hoverJudge.hi)}) · p_Holm = {fmtP(hoverJudge.p_holm)}
            </>
          ) : (
            'Passa sopra un giudice per ispezionare rapporto e IC 95%'
          )}
        </div>
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} className="w-full max-w-[800px] h-auto">
        {[0.5, 0.75, 1, 1.5, 2].map((y) => (
          <g key={y}>
            <line
              x1={padL}
              x2={W - padR}
              y1={yOf(y)}
              y2={yOf(y)}
              stroke={y === 1 ? '#991B1B' : '#F4F4F5'}
              strokeWidth={y === 1 ? 1.3 : 1}
            />
            <text x={padL - 8} y={yOf(y) + 4} textAnchor="end" fontSize="10.5" fill="#52525B" className="font-mono">
              {fmtDec(y, y === 1 || y === 2 ? 0 : 2)}
            </text>
          </g>
        ))}
        <line x1={padL} x2={W - padR} y1={H - padB} y2={H - padB} stroke="#A1A1AA" />
        <line x1={padL} x2={padL} y1={padT} y2={H - padB} stroke="#A1A1AA" />

        {sorted.map((j, i) => {
          const sig = j.p_holm < 0.05;
          const isHov = hoverJudge?.judge_id === j.judge_id;
          const x = xOf(i);
          return (
            <g key={j.judge_id} onMouseEnter={() => setHoverJudge(j)} className="cursor-pointer">
              <line
                x1={x}
                x2={x}
                y1={yOf(j.lo)}
                y2={yOf(j.hi)}
                stroke={isHov ? '#991B1B' : sig ? '#1E40AF' : '#D4D4D8'}
                strokeWidth={isHov ? 2.2 : sig ? 1.5 : 1}
              />
              <circle
                cx={x}
                cy={yOf(j.rapporto)}
                r={isHov ? 4 : sig ? 2.6 : 1.9}
                fill={isHov ? '#991B1B' : sig ? '#1E40AF' : '#52525B'}
              />
            </g>
          );
        })}

        <text x={(padL + W - padR) / 2} y={H - 10} textAnchor="middle" fontSize="11" fill="#52525B">
          {sorted.length} giudici con almeno 30 pronunce, ordinati per rapporto (blu = p_Holm &lt; 0,05)
        </text>
      </svg>
    </div>
  );
}

/* 6. Grafico assenze D3 per categoria (da 0) */
export function AbsencesBarChart({ d3Abs }) {
  const [dim, setDim] = useState('decade');
  const dims = [
    { id: 'decade', label: 'Decennio' },
    { id: 'giudizio', label: 'Tipo di giudizio' },
    { id: 'main10', label: 'Top 10 art. Cost.' },
    { id: 'topic', label: '20 temi LDA' },
  ];
  const group = d3Abs.by[dim];
  const entries = Object.entries(group.rates);
  const W = 720;
  const H = 220;
  const padL = 44;
  const padR = 16;
  const padT = 18;
  const padB = 46;
  const maxY = 0.12;
  const bw = (W - padL - padR) / entries.length;
  const yOf = (v) => H - padB - (v / maxY) * (H - padB - padT);

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
        <div className="flex flex-wrap gap-1.5">
          {dims.map((d) => (
            <button
              key={d.id}
              type="button"
              onClick={() => setDim(d.id)}
              className={`px-2.5 py-1 text-xs font-mono border rounded-sm ${
                dim === d.id ? 'bg-ink text-white border-ink' : 'bg-paper text-muted border-rule'
              }`}
            >
              {d.label}
            </button>
          ))}
        </div>
        <span className="text-xs font-mono text-muted">
          V di Cramér = <strong className="text-ink">{fmtDec(group.cramers_v, 3)}</strong> (media globale{' '}
          {fmtPct(d3Abs.absence_rate, 1)})
        </span>
      </div>
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full max-w-[760px] h-auto">
        {[0, 0.03, 0.06, 0.09, 0.12].map((y) => (
          <g key={y}>
            <line x1={padL} x2={W - padR} y1={yOf(y)} y2={yOf(y)} stroke="#F4F4F5" />
            <text x={padL - 6} y={yOf(y) + 4} textAnchor="end" fontSize="10" fill="#52525B" className="font-mono">
              {fmtPct(y, 0)}
            </text>
          </g>
        ))}
        <line
          x1={padL}
          x2={W - padR}
          y1={yOf(d3Abs.absence_rate)}
          y2={yOf(d3Abs.absence_rate)}
          stroke="#991B1B"
          strokeDasharray="4 3"
          strokeWidth="1.2"
        />
        <line x1={padL} x2={W - padR} y1={yOf(0)} y2={yOf(0)} stroke="#A1A1AA" />
        {entries.map(([k, val], i) => {
          const x = padL + i * bw + bw * 0.16;
          const w = bw * 0.68;
          return (
            <g key={k}>
              <rect x={x} y={yOf(val.rate)} width={w} height={yOf(0) - yOf(val.rate)} fill="#71717A" />
              {entries.length <= 12 && (
                <text
                  x={x + w / 2}
                  y={yOf(val.rate) - 4}
                  textAnchor="middle"
                  fontSize="9.5"
                  fill="#27272A"
                  className="font-mono"
                >
                  {fmtPct(val.rate, 1)}
                </text>
              )}
              <text
                x={x + w / 2}
                y={H - 26}
                textAnchor="middle"
                fontSize={entries.length > 12 ? '8.5' : '9.5'}
                fill="#52525B"
                className="font-mono"
              >
                {k.length > 10 ? k.slice(0, 9) + '…' : k}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

/* 7. Grafico menzioni altre 4 corti per decennio */
export function CourtsDecadeChart({ courts }) {
  const decades = ['1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020'];
  const series = [
    { name: 'Cassazione', color: '#18181B' },
    { name: 'Consiglio di Stato', color: '#1E40AF' },
    { name: 'Corte di giustizia UE', color: '#991B1B' },
    { name: 'Corte EDU', color: '#B45309' },
  ];
  const W = 700;
  const H = 230;
  const padL = 46;
  const padR = 135;
  const padT = 16;
  const padB = 34;
  const maxY = 700;
  const xOf = (i) => padL + (i / (decades.length - 1)) * (W - padL - padR);
  const yOf = (v) => H - padB - (v / maxY) * (H - padB - padT);

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full max-w-[740px] h-auto">
      {[0, 200, 400, 600].map((y) => (
        <g key={y}>
          <line x1={padL} x2={W - padR} y1={yOf(y)} y2={yOf(y)} stroke="#F4F4F5" />
          <text x={padL - 8} y={yOf(y) + 4} textAnchor="end" fontSize="10" fill="#52525B" className="font-mono">
            {y}
          </text>
        </g>
      ))}
      <line x1={padL} x2={W - padR} y1={yOf(0)} y2={yOf(0)} stroke="#A1A1AA" />
      <line x1={padL} x2={padL} y1={padT} y2={yOf(0)} stroke="#A1A1AA" />
      {decades.map((d, i) => (
        <text key={d} x={xOf(i)} y={H - 14} textAnchor="middle" fontSize="10" fill="#52525B" className="font-mono">
          {d}s
        </text>
      ))}
      {series.map((s) => {
        const byD = courts.courts[s.name].pronunce_base_by_decade;
        const path = decades.map((d, i) => `${i === 0 ? 'M' : 'L'}${xOf(i)},${yOf(byD[d] || 0)}`).join(' ');
        const lastY = yOf(byD['2020'] || 0);
        return (
          <g key={s.name}>
            <path d={path} fill="none" stroke={s.color} strokeWidth="2" />
            {decades.map((d, i) => (
              <circle key={d} cx={xOf(i)} cy={yOf(byD[d] || 0)} r="3" fill={s.color} />
            ))}
            <text x={W - padR + 8} y={lastY + 4} fontSize="10.5" fill={s.color} fontWeight="500">
              {s.name} ({byD['2020']})
            </text>
          </g>
        );
      })}
    </svg>
  );
}
