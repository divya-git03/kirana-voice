"""Simulate a bad phone line: 8 kHz telephony band, background noise at a chosen SNR.
Usage: python scripts/add_noise.py samples/clean samples/noisy --snr 10"""
import argparse, pathlib, wave
import numpy as np


def read(p):
    with wave.open(str(p)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32), w.getframerate()


def write(p, x, sr):
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(np.clip(x, -32768, 32767).astype(np.int16).tobytes())


def degrade(x, sr, snr_db, rng):
    n = int(len(x) * 8000 / sr)  # downsample to telephony 8 kHz
    x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)
    noise = rng.normal(0, 1, n)
    noise = np.convolve(noise, np.ones(8) / 8, mode="same")  # coloured "crowd/street" hiss
    p_sig, p_noise = np.mean(x ** 2) + 1e-9, np.mean(noise ** 2)
    noise *= np.sqrt(p_sig / (p_noise * 10 ** (snr_db / 10)))
    return x + noise, 8000


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--snr", type=float, default=10)
    a = ap.parse_args()
    rng = np.random.default_rng(0)
    dst = pathlib.Path(a.dst); dst.mkdir(parents=True, exist_ok=True)
    for p in sorted(pathlib.Path(a.src).glob("*.wav")):
        x, sr = read(p)
        y, sr2 = degrade(x, sr, a.snr, rng)
        write(dst / p.name, y, sr2)
        print("wrote", dst / p.name)
