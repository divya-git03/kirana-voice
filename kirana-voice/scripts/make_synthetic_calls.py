"""Generate synthetic customer calls with Timbre v2.5 (no real recordings, no personal data).
Usage: python scripts/make_synthetic_calls.py"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kirana_voice.gnani import GnaniClient

VOICES = ["Nalini"]  # add more voices from the Voice Catalog for speaker variety
c = GnaniClient()
out = pathlib.Path("samples/clean"); out.mkdir(parents=True, exist_ok=True)
for i, row in enumerate(json.load(open("samples/orders.json"))):
    for v in VOICES:
        p = out / f"call_{i:02d}_{v}.wav"
        p.write_bytes(c.synthesize(row["say"], voice=v, sample_rate=16000))
        print("wrote", p)
