"""Measure end-to-end order accuracy (audio -> Prisma -> parser) on clean vs noisy synthetic calls.
Usage: python scripts/benchmark.py samples/clean samples/noisy"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kirana_voice.gnani import GnaniClient
from kirana_voice.parser import parse_order

rows = json.load(open("samples/orders.json"))
c = GnaniClient()
print(f"{'set':<16}{'calls':>6}{'exact order':>14}{'item recall':>14}")
for d in sys.argv[1:]:
    files = sorted(pathlib.Path(d).glob("call_*.wav"))
    exact = hit = tot = 0
    for f in files:
        exp = {k: tuple(v) for k, v in rows[int(f.stem.split("_")[1])]["expect"].items()}
        got = {l.item.key: (l.qty, l.unit) for l in parse_order(c.transcribe(str(f))["transcript"])}
        exact += got == exp
        hit += sum(k in got for k in exp); tot += len(exp)
    print(f"{d:<16}{len(files):>6}{exact / len(files):>14.0%}{hit / tot:>14.0%}")
