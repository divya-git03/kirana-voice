from kirana_voice.parser import parse_order, intent
from kirana_voice.assistant import Session


def asdict(text):
    return {l.item.key: (l.qty, l.unit) for l in parse_order(text)}


def test_basic_hinglish():
    assert asdict("do kilo chawal aur ek packet maggi") == {"rice": (2, "kg"), "maggi": (1, "pack")}

def test_half_kilo():
    assert asdict("aadha kilo cheeni") == {"sugar": (0.5, "kg")}

def test_grams_convert():
    assert asdict("500 gram dal") == {"dal": (0.5, "kg")}

def test_dozen():
    assert asdict("ek dozen ande") == {"eggs": (12, "piece")}

def test_devanagari():
    assert asdict("दो किलो आटा और एक लीटर तेल") == {"atta": (2, "kg"), "oil": (1, "l")}

def test_quantity_after_item():
    assert asdict("chawal do kilo aur atta teen kilo") == {"rice": (2, "kg"), "atta": (3, "kg")}

def test_dedh_and_milk():
    assert asdict("ek litre doodh aur dedh kilo pyaz") == {"milk": (1, "l"), "onion": (1.5, "kg")}

def test_multiword_alias_not_double_counted():
    assert list(asdict("ek packet chai patti")) == ["tea"]

def test_fused_units():
    assert asdict("2kg aloo") == {"potato": (2, "kg")}

def test_polite_noise_words():
    assert asdict("bhaiya teen packet biscuit aur ek sabun dena") == {"biscuit": (3, "pack"), "soap": (1, "piece")}

def test_conversation_flow():
    s = Session()
    assert "134" in s.handle("do kilo chawal aur ek packet maggi")
    assert "294" in s.handle("ek litre tel bhi")
    assert intent("haan theek hai") == "confirm"
    assert "Order number" in s.handle("haan theek hai")

def test_cancel():
    s = Session(); s.handle("ek kilo atta")
    assert "cancel" in s.handle("nahi cancel karo")
    assert not s.basket

def test_unrecognised():
    assert "samajh nahi aaya" in Session().handle("blah blah")
