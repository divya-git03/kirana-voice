"""Rule-based Hinglish/Hindi/English order parser. Deterministic, offline, testable."""
import re
from dataclasses import dataclass
from .catalog import CATALOG, Item

NUMBERS = {
    "ek": 1, "एक": 1, "one": 1, "do": 2, "दो": 2, "two": 2, "teen": 3, "तीन": 3, "three": 3,
    "char": 4, "chaar": 4, "चार": 4, "four": 4, "paanch": 5, "panch": 5, "पांच": 5, "पाँच": 5, "five": 5,
    "chhe": 6, "che": 6, "chah": 6, "छह": 6, "छः": 6, "six": 6, "saat": 7, "सात": 7, "seven": 7,
    "aath": 8, "आठ": 8, "eight": 8, "nau": 9, "नौ": 9, "nine": 9, "das": 10, "दस": 10, "ten": 10,
    "aadha": 0.5, "adha": 0.5, "आधा": 0.5, "half": 0.5, "dedh": 1.5, "डेढ़": 1.5, "dhai": 2.5, "ढाई": 2.5,
    "paav": 0.25, "pav": 0.25, "पाव": 0.25,
}
UNITS = {
    "kilo": "kg", "kg": "kg", "kilogram": "kg", "किलो": "kg", "किग्रा": "kg",
    "gram": "g", "gm": "g", "g": "g", "ग्राम": "g",
    "litre": "l", "liter": "l", "l": "l", "ltr": "l", "लीटर": "l",
    "ml": "ml", "मिली": "ml",
    "packet": "pack", "pkt": "pack", "pack": "pack", "पैकेट": "pack",
    "piece": "piece", "pieces": "piece", "pcs": "piece", "नग": "piece", "पीस": "piece",
    "dozen": "dozen", "darjan": "dozen", "दर्जन": "dozen",
}
_ALIASES = sorted(
    ((tuple(a.lower().split()), it) for it in CATALOG for a in it.aliases),
    key=lambda x: -len(x[0]),
)
_TOKEN = re.compile(r"[^\s,.;!?।|]+")
_FUSED = re.compile(r"^(\d+(?:\.\d+)?)([a-zA-Z\u0900-\u097F]+)$")


@dataclass
class Line:
    item: Item
    qty: float
    unit: str

    @property
    def total(self):
        return round(self.qty * self.item.price, 2)


def tokenize(text):
    out = []
    for t in _TOKEN.findall(text.lower()):
        m = _FUSED.match(t)  # "2kg" -> "2", "kg"
        out.extend(m.groups() if m else [t])
    return out


def _num(tok):
    if tok in NUMBERS:
        return NUMBERS[tok]
    try:
        return float(tok)
    except ValueError:
        return None


def _qty_from(tokens, idxs):
    """Find a number (+ optional unit) among the given token indexes."""
    for pos, i in enumerate(idxs):
        n = _num(tokens[i])
        if n is None:
            continue
        used, unit = [i], None
        j = idxs[pos + 1] if pos + 1 < len(idxs) else None
        if j is not None and j == i + 1 and tokens[j] in UNITS:
            unit = UNITS[tokens[j]]
            used.append(j)
        return n, unit, used
    for i in idxs:  # bare unit: "dozen ande"
        if tokens[i] in UNITS:
            return 1.0, UNITS[tokens[i]], [i]
    return None


def _to_base(qty, unit, item):
    if unit is None:
        return qty, item.unit
    if unit == "g" and item.unit == "kg":
        return qty / 1000, "kg"
    if unit == "ml" and item.unit == "l":
        return qty / 1000, "l"
    if unit == "dozen":
        return qty * 12, "piece"
    return qty, item.unit


def parse_order(text):
    toks = tokenize(text)
    found, taken = [], set()
    for i in range(len(toks)):
        if i in taken:
            continue
        for alias, item in _ALIASES:
            n = len(alias)
            if tuple(toks[i:i + n]) == alias and not (set(range(i, i + n)) & taken):
                found.append((i, i + n, item))
                taken.update(range(i, i + n))
                break
    consumed, lines = set(), []
    for k, (s, e, item) in enumerate(found):
        prev_end = found[k - 1][1] if k else 0
        next_start = found[k + 1][0] if k + 1 < len(found) else len(toks)
        left = [i for i in range(max(prev_end, s - 3), s) if i not in consumed]
        right = [i for i in range(e, min(next_start, e + 3)) if i not in consumed]
        hit = _qty_from(toks, left) or _qty_from(toks, right)
        if hit:
            qty, unit, used = hit
            consumed.update(used)
        else:
            qty, unit = 1.0, None
        qty, unit = _to_base(qty, unit, item)
        lines.append(Line(item, round(qty, 3), unit))
    merged = {}
    for ln in lines:
        if ln.item.key in merged:
            merged[ln.item.key].qty += ln.qty
        else:
            merged[ln.item.key] = ln
    return list(merged.values())


CONFIRM = {"haan", "han", "ha", "haa", "yes", "confirm", "ok", "okay", "theek", "thik", "हाँ", "हां", "ठीक", "कन्फर्म"}
CANCEL = {"nahi", "nahin", "no", "cancel", "ruko", "नहीं", "रद्द", "कैंसिल"}


def intent(text):
    toks = set(tokenize(text))
    if toks & CANCEL:
        return "cancel"
    if toks & CONFIRM and not parse_order(text):
        return "confirm"
    return "order"
