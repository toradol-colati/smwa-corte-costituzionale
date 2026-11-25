export function fmtInt(v) {
  if (v === null || v === undefined || Number.isNaN(v)) return '—';
  return Math.round(v).toLocaleString('it-IT');
}

export function fmtDec(v, digits = 2) {
  if (v === null || v === undefined || Number.isNaN(v)) return '—';
  return Number(v).toLocaleString('it-IT', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

export function fmtPct(v, digits = 1) {
  if (v === null || v === undefined || Number.isNaN(v)) return '—';
  return `${fmtDec(v * 100, digits)}%`;
}

export function fmtP(p) {
  if (p === null || p === undefined || Number.isNaN(p)) return '—';
  if (p < 0.001) return '< 0,001';
  return fmtDec(p, 3);
}

export function fmtPid(pid) {
  const s = String(pid);
  if (s.length !== 8) return s;
  const year = s.slice(0, 4);
  const num = parseInt(s.slice(4), 10);
  return `${num}/${year}`;
}

export function fmtCI(lo, hi, digits = 2) {
  return `${fmtDec(lo, digits)}–${fmtDec(hi, digits)}`;
}

export function fmtPctCI(lo, hi, digits = 1) {
  return `${fmtDec(lo * 100, digits)}–${fmtDec(hi * 100, digits)}%`;
}
