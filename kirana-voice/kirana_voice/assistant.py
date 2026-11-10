"""Conversation logic: transcript -> order -> Hinglish reply."""
import uuid
from .parser import parse_order, intent


def _fmt(q):
    return str(int(q)) if float(q).is_integer() else f"{q:g}"


def _unit_word(u):
    return {"kg": "kilo", "l": "litre", "pack": "packet", "piece": "piece"}[u]


def describe(lines):
    return ", ".join(f"{_fmt(l.qty)} {_unit_word(l.unit)} {l.item.name}" for l in lines)


class Session:
    """One phone call. Keeps a running basket until the customer confirms or cancels."""

    def __init__(self):
        self.basket = {}
        self.order_id = None

    def total(self):
        return round(sum(l.total for l in self.basket.values()), 2)

    def handle(self, transcript):
        kind = intent(transcript)
        if kind == "cancel":
            self.basket.clear()
            return "Theek hai, order cancel kar diya. Kuch aur chahiye toh bataiye."
        if kind == "confirm":
            if not self.basket:
                return "Abhi tak koi saamaan nahi liya. Kya chahiye aapko?"
            self.order_id = uuid.uuid4().hex[:6].upper()
            msg = (f"Order pakka ho gaya. Order number {self.order_id}. "
                   f"Total {_fmt(self.total())} rupaye. Dhanyavaad!")
            self.basket.clear()
            return msg
        lines = parse_order(transcript)
        if not lines:
            return "Maaf kijiye, samajh nahi aaya. Kripya saamaan aur matra dobara bataiye."
        for l in lines:
            if l.item.key in self.basket:
                self.basket[l.item.key].qty += l.qty
            else:
                self.basket[l.item.key] = l
        return (f"Aapka order: {describe(list(self.basket.values()))}. "
                f"Total {_fmt(self.total())} rupaye. Confirm karein?")
