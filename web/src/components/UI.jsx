import React from 'react';

const STATUS_STYLE = {
  principale: 'text-primary border-red-300 bg-red-50/60',
  esplorativo: 'text-accent border-blue-200 bg-blue-50/50',
  secondario: 'text-zinc-700 border-zinc-300 bg-zinc-50',
  descrittivo: 'text-zinc-600 border-zinc-200 bg-zinc-50',
  negativo: 'text-amber-900 border-amber-300 bg-amber-50/60',
};

export function StatusTag({ type }) {
  return (
    <span
      className={`inline-block border px-1.5 py-0.5 text-[10px] font-mono uppercase tracking-wider rounded-[2px] align-middle ${
        STATUS_STYLE[type] || STATUS_STYLE.descrittivo
      }`}
    >
      {type}
    </span>
  );
}

export function SectionTitle({ id, num, title }) {
  return (
    <h2
      id={id}
      className="scroll-mt-20 mt-14 mb-4 pt-6 border-t border-rule font-serif text-2xl sm:text-[1.7rem] font-medium tracking-tight text-ink"
    >
      {num && <span className="text-muted mr-2.5 font-normal">{num}.</span>}
      {title}
    </h2>
  );
}

export function SubTitle({ id, num, title, status }) {
  return (
    <h3
      id={id}
      className="scroll-mt-20 mt-9 mb-3 font-serif text-xl font-medium text-ink flex flex-wrap items-baseline gap-2.5"
    >
      <span>
        {num && <span className="text-muted mr-2 font-normal text-base">{num}</span>}
        {title}
      </span>
      {status && <StatusTag type={status} />}
    </h3>
  );
}

/* Figura scientifica: titolo descrittivo breve, grafico pulito, didascalia autoesplicativa senza interpretazione (§3.2) */
export function ScientificFigure({ id, label, caption, controls, children }) {
  return (
    <figure id={id} className="scroll-mt-20 my-8 py-4 border-y border-rule bg-white px-4 sm:px-5">
      {controls && <div className="flex flex-wrap items-center justify-end gap-1.5 mb-3">{controls}</div>}
      <div className="w-full overflow-x-auto">{children}</div>
      <figcaption className="mt-3 pt-2.5 border-t border-zinc-100 text-xs text-muted leading-relaxed">
        <strong className="text-ink font-semibold mr-1.5">{label}.</strong>
        {caption}
      </figcaption>
    </figure>
  );
}

/* Tabella scientifica: titolo in testa (§3.2), linee orizzontali stile booktabs */
export function ScientificTable({ id, label, title, note, children }) {
  return (
    <div id={id} className="scroll-mt-20 my-7">
      <div className="text-xs text-ink mb-2 leading-snug">
        <strong className="font-semibold mr-1.5">{label}.</strong>
        <span>{title}</span>
      </div>
      <div className="overflow-x-auto border-y border-zinc-800 bg-white">{children}</div>
      {note && <div className="mt-1.5 text-[11px] text-muted leading-relaxed">{note}</div>}
    </div>
  );
}

export function SwitchBtn({ active, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`px-2.5 py-1 text-[11px] font-mono border rounded-[2px] transition-colors ${
        active
          ? 'bg-ink text-white border-ink'
          : 'bg-paper text-muted border-rule hover:border-zinc-400 hover:text-ink'
      }`}
    >
      {children}
    </button>
  );
}
