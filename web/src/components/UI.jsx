import React from 'react';

const BADGE_STYLES = {
  principale: 'bg-red-50 text-red-900 border-red-200',
  esplorativo: 'bg-blue-50 text-blue-900 border-blue-200',
  descrittivo: 'bg-zinc-100 text-zinc-700 border-zinc-300',
  secondario: 'bg-zinc-100 text-zinc-800 border-zinc-300',
  negativo: 'bg-amber-50 text-amber-900 border-amber-200',
};

export function Badge({ type = 'descrittivo', children }) {
  const cls = BADGE_STYLES[type] || BADGE_STYLES.descrittivo;
  return (
    <span
      className={`inline-block border px-1.5 py-0.5 text-[10px] font-mono uppercase tracking-wider rounded-sm align-middle ${cls}`}
    >
      {children || type}
    </span>
  );
}

export function SectionHeader({ id, num, title, subtitle, badge }) {
  return (
    <div id={id} className="scroll-mt-20 pt-10 pb-4 border-b border-rule mb-6">
      <div className="flex flex-wrap items-center gap-2.5 mb-1.5">
        {num && (
          <span className="font-mono text-xs uppercase tracking-widest text-muted">
            Sezione {num}
          </span>
        )}
        {badge && <Badge type={badge} />}
      </div>
      <h2 className="font-serif text-2xl sm:text-3xl font-medium tracking-tight text-ink">
        {title}
      </h2>
      {subtitle && <p className="mt-1.5 text-sm text-muted max-w-3xl">{subtitle}</p>}
    </div>
  );
}

export function SubHeader({ id, title, badge }) {
  return (
    <div id={id} className="scroll-mt-20 flex flex-wrap items-center gap-2 mt-8 mb-3">
      <h3 className="font-serif text-xl font-medium text-ink">{title}</h3>
      {badge && <Badge type={badge} />}
    </div>
  );
}

export function FigureBox({ num, title, caption, source, controls, children }) {
  return (
    <figure className="my-6 bg-white border border-rule rounded-sm p-4 sm:p-5">
      <div className="flex flex-wrap items-start justify-between gap-3 mb-3">
        <div>
          {num && (
            <span className="font-mono text-[11px] uppercase tracking-wider text-muted block mb-0.5">
              {num}
            </span>
          )}
          <div className="font-sans text-sm font-semibold text-ink">{title}</div>
        </div>
        {controls && <div className="flex flex-wrap items-center gap-1.5">{controls}</div>}
      </div>
      <div className="w-full overflow-x-auto">{children}</div>
      {(caption || source) && (
        <figcaption className="mt-3 pt-2.5 border-t border-zinc-100 text-xs text-muted leading-relaxed">
          {caption}
          {source && (
            <span className="block font-mono text-[11px] text-zinc-400 mt-1">
              Fonte dati: {source}
            </span>
          )}
        </figcaption>
      )}
    </figure>
  );
}

export function StaticPngFigure({ src, alt }) {
  return (
    <div className="bg-white flex justify-center py-2">
      <img
        src={src}
        alt={alt}
        loading="lazy"
        className="max-w-full h-auto max-h-[460px] object-contain"
      />
    </div>
  );
}

export function TabButton({ active, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`px-2.5 py-1 text-xs font-mono border rounded-sm transition-colors ${
        active
          ? 'bg-ink text-white border-ink'
          : 'bg-paper text-muted border-rule hover:border-zinc-400 hover:text-ink'
      }`}
    >
      {children}
    </button>
  );
}

export function StatCell({ label, value, sub, highlight = false }) {
  return (
    <div
      className={`p-3.5 border rounded-sm ${
        highlight ? 'bg-red-50/40 border-red-200' : 'bg-white border-rule'
      }`}
    >
      <div className="text-[11px] font-mono uppercase tracking-wider text-muted">{label}</div>
      <div
        className={`mt-1 text-xl font-mono font-semibold tabular-nums ${
          highlight ? 'text-primary' : 'text-ink'
        }`}
      >
        {value}
      </div>
      {sub && <div className="mt-0.5 text-xs text-muted">{sub}</div>}
    </div>
  );
}

export function Callout({ title, tone = 'neutral', children }) {
  const styles =
    tone === 'primary'
      ? 'border-l-2 border-l-primary bg-red-50/30 border-y border-r border-rule'
      : tone === 'warn'
      ? 'border-l-2 border-l-amber-600 bg-amber-50/30 border-y border-r border-rule'
      : 'border-l-2 border-l-zinc-400 bg-zinc-50/70 border-y border-r border-rule';
  return (
    <div className={`my-5 p-4 text-sm leading-relaxed text-zinc-800 ${styles}`}>
      {title && <div className="font-semibold text-ink mb-1">{title}</div>}
      {children}
    </div>
  );
}
