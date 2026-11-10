"""CLI: python -m kirana_voice.cli call1.wav call2.wav   |   --text "do kilo chawal" --text "haan" """
import argparse, pathlib
from .assistant import Session


def main():
    ap = argparse.ArgumentParser(description="Kirana Voice, built on Gnani AI Prisma + Timbre")
    ap.add_argument("audio", nargs="*", help="audio files, one per customer turn")
    ap.add_argument("--text", action="append", help="skip STT; feed text turns (offline demo)")
    ap.add_argument("--speak", action="store_true", help="synthesize replies with Timbre v2.5 into out/")
    a = ap.parse_args()

    client = None
    if a.audio or a.speak:
        from .gnani import GnaniClient
        client = GnaniClient()
    s = Session()
    turns = [("audio", p) for p in a.audio] + [("text", t) for t in (a.text or [])]
    pathlib.Path("out").mkdir(exist_ok=True)
    for i, (kind, val) in enumerate(turns, 1):
        text = client.transcribe(val)["transcript"] if kind == "audio" else val
        print(f"\n[turn {i}] Customer: {text}")
        reply = s.handle(text)
        print(f"          Shop:     {reply}")
        if a.speak:
            path = f"out/reply_{i}.wav"
            open(path, "wb").write(client.synthesize(reply))
            print(f"          (audio -> {path})")


if __name__ == "__main__":
    main()
