import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "extract"))
from citations import find_mentions

CASES = {
    "sentenza n, 110 del 1963 della Corte costituzionale": [(1963, 110, "")],
    "nelle sue decisioni 27 dicembre 1973, n. 183, e 30 ottobre 1975, n. 232. I regolamenti": [(1973, 183, ""), (1975, 232, "")],
    "con la sentenza n. 134 del 1986 e che nell'ordinanza di rimessione non": [(1986, 134, "")],
    "Con ordinanza del 19 luglio 2017 (reg. ord. n. 137 del 2017), il Tribunale": [(2017, 137, "referral_order")],
    "espressi dal giudice rimettente» (sentenza n. 125 del 2018). Ciò": [(2018, 125, "")],
    "(Cass., sez. un., sentenza n. 120 del 2019; sentenza n. 7 del 2011)": [(2019, 120, "other_court_before"), (2011, 7, "other_court_before")],
    "Corte di cassazione, sezioni unite civili, sentenza 3 marzo 2010, n. 123": [(2010, 123, "other_court_before")],
    "sentenze nn. 26 e 320 del 2007, n.4/2008 e ordinanza n. 5 del 2009": [(2007, 26, ""), (2007, 320, ""), (2008, 4, ""), (2009, 5, "")],
    "ex plurimis, ordinanze n. 41 del 2010 e nn. 188 e 52 del 2009": [(2010, 41, ""), (2009, 188, ""), (2009, 52, "")],
    "la sentenza del Tribunale di Roma n. 55 del 2001": [],
    "sentenza n. 1234 del 2018 della Corte di cassazione": [(2018, 1234, "other_court_after")],
    "con la propria sentenza 19 giugno 1956, n. 9, confermata": [(1956, 9, "")],
    "(sent. n. 46 dell'8 marzo 1957)": [(1957, 46, "")],
    "con sent. 174/1972, l'illegittimità": [(1972, 174, "")],
    "La C. cost. 16/1977, poi, non conforta": [(1977, 16, "")],
    "precedenti sentenze del 16 e 22 gennaio 1957, n. 3 e n. 28, e del 9 luglio 1958, n. 53, con le quali": [(1957, 3, ""), (1957, 28, ""), (1958, 53, "")],
    "della Corte di cassazione (del resto già in precedenza verificatosi: sent. n. 66 del 1964)": [(1964, 66, "")],
    "La Cassazione (sentenza n. 5048 del 1988) ha ritenuto": [(1988, 5048, "other_court_before")],
    "con la legge n. 6 del 1981 e la sentenza n. 5 del 1980": [(1980, 5, "")],
}


def test_cases():
    for text, expected in CASES.items():
        got = [(m["year"], m["number"], m["excluded"]) for m in find_mentions(text)]
        assert got == expected, (text, got)


def test_same_date():
    got = [(m["year"], m["number"]) for m in find_mentions("respinta con la sentenza n. 59, in pari data, alla quale", default_year=1957)]
    assert got == [(1957, 59)]
