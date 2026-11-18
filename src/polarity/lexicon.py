"""Rules for the polarity of a citation: is the cited precedent distinguished or departed from?
("distinzione o distacco"). Support is the default and is not detected: most citations quote a
precedent as authority with no cue at all. A rule fires only when the cue is tied to the cited
precedent (the precedent, its reasoning or the case it decided is called not pertinent, different,
not a precedent, or to be overruled), within a short window around the mention. Written on the
development half of the citing pronunce (src/polarity/contexts.py), then frozen before the test.
"""
import re

GAP = r"[^.;]{0,120}?"          # same clause, at most 120 characters
PREC = r"(?:sentenz[ae]|ordinanz[ae]|pronunc[ei]a?|pronunzi[ae]|decision[ei]|precedent[ei]|giurisprudenza|orientamento|indirizzo)"
RULES = {
    # the reference to the precedent (or its reasoning) is not pertinent / not relevant here
    "non_pertinente": rf"(?:richiam\w*|riferiment\w*|argomentazion\w*|considerazion\w*|principi\w*|affermazion\w*|ratio)\W[^.;«»]{{0,120}}?"
                      rf"non (?:è|sono|appare|appaiono|risulta|risultano|può ritenersi|possono ritenersi) (?:pertinent|conferent|utilmente richiamabil)"
                      rf"|non (?:è|sono|appare|appaiono|risulta|risultano) (?:pertinent|conferent)\w* (?:il|i|le|la|l'|gli) (?:richiam|riferiment|argomentazion|considerazion|principi|affermazion|precedent)"
                      rf"|(?:inconferente|non pertinente|non conferente) (?:il|è il) (?:richiamo|riferimento)",
    # the precedent does not support the thesis / is not a precedent on the point
    "non_precedente": rf"non (?:si può|può|è possibile) ravvisare un precedente|non (?:costituisce|rappresenta|integra) un precedente|non (?:è|sono) (?:un )?precedent\w* in termini"
                      rf"|non (?:trova|trovano) conforto|neppure trova conforto|nessun conforto|non (?:è|sono) (?:invocabil|richiamabil)\w* (?:a sostegno|in senso)",
    # what the Court decided then differs from the present case
    "caso_diverso": rf"(?:diversamente|a differenza) (?:da|di) quanto (?:deciso|affermato|ritenuto|riscontrato|accaduto|avvenuto|stabilito|rilevato|esaminato|osservato|statuito){GAP}{PREC}"
                    rf"|(?:diversamente|a differenza) (?:dalla|dal|dalle|dai|della|del|delle|dei) (?:questione|questioni|fattispecie|caso|casi|vicenda|disciplina|norma|norme|ipotesi|situazione) (?:allora |ivi |già )?(?:esaminat|decis|scrutinat|risolt|trattat|giudicat)"
                    rf"|(?:divers|different)\w* (?:da|rispetto a) (?:quell[aoie]|quanto)\W{{0,3}}(?:allora |già )?(?:esaminat|decis|scrutinat|risolt|trattat|giudicat|considerat|affrontat)\w*{GAP}{PREC}"
                    rf"|non (?:è|sono|era|erano|risulta|risultano|appare|appaiono|appaia|sia|siano) (?:del tutto |affatto |pienamente |in alcun modo )?(?:sovrapponibil|assimilabil|comparabil|analog|identic|equiparabil)\w* (?:a|con) quell[aoie]\W{{0,3}}(?:allora |ora |oggi |già )?(?:in esame|presa in esame|esaminat|decis|scrutinat|risolt|oggetto|considerat)"
                    rf"|pur non (?:sovrapponibil|assimilabil|comparabil|analog|identic|equiparabil)\w*"
                    rf"|(?:concern\w*|riguard\w*|aveva ad oggetto|avevano ad oggetto|si riferiv\w*) (?:una |un )?(?:ben |del tutto |affatto )?(?:distint|divers|different)\w* (?:fattispecie|questione|situazione|caso|disciplina|norma|vicenda|ipotesi)",
    # the precedent did not say / did not decide what is claimed
    "non_affermato": rf"(?:questa corte|la corte|la sentenza|l'ordinanza|la pronuncia|la decisione|tale pronuncia|quella pronuncia|la citata|il citato)\W{GAP}non (?:ha|hanno) (?:già )?(?:affermato|inteso|stabilito|sancito|deciso|valutato)",
    # explicit overruling / departure
    "superamento": rf"(?:superare|superando|rimeditare|rimeditando|rivedere|rivedendo|abbandonare|abbandonando|discostarsi da|discostandosi da|rivisitare|correggere)\W+(?:il|l'|la|i|gli|le|tale|tali|quel|quell'|quella|questo|questa|propri[ao]|precedente)\W*(?:\w+\W+){{0,1}}?(?:precedent|orientament|indirizz|giurisprudenz|principi|soluzion)"
                   rf"|mutamento (?:di|della|del) (?:giurisprudenza|orientamento|indirizzo)|revirement|overruling",
}
# a negated or hypothetical departure means the opposite ("non sussistono ragioni per discostarsi",
# "nessun nuovo argomento tale da superare", "si dovrebbe superare l'orientamento")
NEG_BEFORE = re.compile(r"(?:\bnon\b|\bnessun|\bné\b|\balcun|\bsenza\b|dovrebbe|dovrebbero|occorrerebbe|implicherebbe|comporterebbe|richiederebbe)", re.I)
# the cue is in the words of the referring judge or a party, not of the Court
ATTRIBUTED = re.compile(r"(?:rimettente|giudice a quo|giudici a quibus|ricorrente|resistente|difesa|avvocatura|parte privata|parti private)\W(?:[^.;]{0,60}?)"
                        r"(?:invoca|invocano|chiede|chiedono|sollecita|sollecitano|auspica|propone|propongono|sostiene|sostengono|ritiene|ritengono|lamenta)\w*", re.I)
COMPILED = {k: re.compile(v, re.I) for k, v in RULES.items()}


OBJECT_NOT_PRECEDENT = re.compile(r"^\W{0,3}(?:\w+\W+){0,2}?(?:agli? artt?\.|all'art\.|dell'art|degli artt|ai? parametr|agli (?:\w+ )?parametr|al(?:l[ae])? (?:parametr|norm|disposizion|legge|decreto|articol)|del(?:l[ae']| )?\s?(?:parametr|norm|disposizion|legge|decreto|articol))", re.I)
# "argomentazioni / profili diversi da quelli già esaminati" concerns the arguments, not the case
ARGUMENTS = re.compile(r"(?:argoment|argomentazion|profil|motiv|ragion|element|censur|deduzion|doglianz|prospettazion)\w*\s+(?:\w+\s+){0,3}$", re.I)
CONDITIONAL = re.compile(r"\b\w{3,}(?:rebbe|rebbero)\b", re.I)  # reported speech of a party or of the referring judge
CITATION = re.compile(r"\b(?:sentenz|ordinanz|pronunc|pronunz|decision)\w*\b[^.;]{0,40}?\bn\.?\s*\d|\bn\.\s*\d+\s*(?:del|/)\s*\d{2,4}|pronunce di questa corte", re.I)


def classify(before, mention, after):
    """Return the name of the first rule that fires around the mention, or None.
    The window is the last 160 characters before the mention and the first 160 after it."""
    w = before[-160:] + " ⟦M⟧ " + after[:160]
    pos = w.index("⟦M⟧")
    end_m = pos + 3
    for name, rx in COMPILED.items():
        for m in rx.finditer(w):
            dist = 0 if m.start() <= pos <= m.end() else min(abs(m.start() - pos), abs(m.end() - pos))
            if dist > 120:
                continue
            pre = w[max(0, m.start() - 80):m.start()]
            # another citation between the cue and this mention, or right after a cue that follows the
            # mention: the cue belongs to that other citation
            between = w[m.end():pos] if m.end() <= pos else w[end_m:m.start()] if m.start() >= end_m else ""
            if CITATION.search(between):
                continue
            if m.start() >= end_m and CITATION.search(w[m.end():m.end() + 60]):
                continue
            if name == "superamento" and NEG_BEFORE.search(w[max(0, m.start() - 100):m.start()]):
                continue  # negated departure ("nessun nuovo argomento ... tale da superare")
            if name == "caso_diverso" and NEG_BEFORE.search(pre[-60:]):
                continue  # negated departure or difference ("non vengono addotti argomenti diversi da quelli")
            if name == "caso_diverso" and ARGUMENTS.search(w[max(0, m.start() - 40):m.start()]):
                continue
            if name in ("caso_diverso", "non_affermato", "superamento") and CONDITIONAL.search(pre):
                continue  # reported speech ("porrebbe problemi diversi", "si dovrebbe superare")
            if name == "superamento" and ATTRIBUTED.search(pre):
                continue  # the party asks for an overruling; the Court is not departing
            if name == "non_pertinente" and OBJECT_NOT_PRECEDENT.search(w[m.end():m.end() + 40]):
                continue  # "non è pertinente il richiamo agli artt. ...": the object is not a precedent
            return name
    return None
