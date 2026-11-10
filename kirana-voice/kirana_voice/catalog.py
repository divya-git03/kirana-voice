"""Synthetic store catalogue. Aliases cover Roman Hinglish and Devanagari spellings."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    key: str
    name: str          # spoken back to the customer
    price: float       # rupees per base unit
    unit: str          # kg | l | pack | piece
    aliases: tuple


CATALOG = [
    Item("rice", "chawal", 60, "kg", ("chawal", "chaawal", "rice", "चावल")),
    Item("atta", "atta", 45, "kg", ("atta", "aata", "आटा", "आटे")),
    Item("dal", "toor dal", 140, "kg", ("dal", "daal", "toor", "दाल")),
    Item("sugar", "cheeni", 45, "kg", ("cheeni", "chini", "sugar", "shakkar", "चीनी", "शक्कर")),
    Item("salt", "namak", 25, "pack", ("namak", "salt", "नमक")),
    Item("oil", "tel", 160, "l", ("tel", "oil", "तेल")),
    Item("milk", "doodh", 56, "l", ("doodh", "dudh", "milk", "दूध")),
    Item("tea", "chai patti", 120, "pack", ("chai patti", "chaipatti", "tea", "चायपत्ती", "चाय पत्ती", "chai", "चाय")),
    Item("maggi", "Maggi", 14, "pack", ("maggi", "noodles", "मैगी")),
    Item("biscuit", "biscuit", 10, "pack", ("biscuit", "biscuits", "बिस्कुट")),
    Item("soap", "sabun", 38, "piece", ("sabun", "soap", "साबुन")),
    Item("eggs", "ande", 7, "piece", ("anda", "ande", "egg", "eggs", "अंडा", "अंडे")),
    Item("bread", "bread", 45, "pack", ("bread", "ब्रेड")),
    Item("haldi", "haldi", 30, "pack", ("haldi", "हल्दी")),
    Item("onion", "pyaz", 40, "kg", ("pyaz", "pyaaz", "onion", "प्याज", "प्याज़")),
    Item("potato", "aloo", 30, "kg", ("aloo", "alu", "potato", "आलू")),
]
