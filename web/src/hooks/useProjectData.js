import { useEffect, useState } from 'react';

const FILES = {
  network: 'network_basic.json',
  d1: 'd1_results.json',
  d2: 'd2_results.json',
  d2Strata: 'd2_strata_check.json',
  d3: 'd3_results.json',
  d3Abs: 'd3_absences.json',
  d3Full: 'd3_full_check.json',
  d4: 'd4_results.json',
  succession: 'precedent_succession.json',
  topics: 'topics.json',
  parametri: 'parametri.json',
  extras: 'extras.json',
  course: 'course_measures.json',
  polarity: 'polarity_validation_claude.json',
  courts: 'courts_sizing.json',
  cositting: 'cositting_network.json',
  sedute: 'collegio_vs_sedute.json',
  numbers: 'numbers.json',
  massime: 'massime_citations.json',
  api: 'api_fetch.json',
};

function parseSafeJson(text) {
  // Difesa aggiuntiva se i JSON non sono stati sanitizzati da sync_site_data.py
  const cleaned = text.replace(/\bNaN\b|\b-?Infinity\b/g, 'null');
  return JSON.parse(cleaned);
}

export function useProjectData() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    Promise.all(
      Object.entries(FILES).map(async ([key, file]) => {
        const res = await fetch(`./data/${file}`);
        if (!res.ok) {
          throw new Error(`Impossibile caricare ./data/${file} (HTTP ${res.status})`);
        }
        const txt = await res.text();
        return [key, parseSafeJson(txt)];
      })
    )
      .then((entries) => {
        if (active) setData(Object.fromEntries(entries));
      })
      .catch((err) => {
        if (active) setError(err.message);
      });

    return () => {
      active = false;
    };
  }, []);

  return { data, error, loading: !data && !error };
}
