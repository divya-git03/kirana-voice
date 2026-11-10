# 🛒 Kirana Voice: phone orders for neighbourhood stores, in Hinglish

> Call. Say *"bhaiya, do kilo chawal aur ek packet maggi"*. Get a spoken, priced order back in seconds.

Built for **The Great Indian AI Internship Challenge** on Gnani AI's own models.

**Awards targeted:** Mixed Vibes (code-mixed speech) · Real Deal (kirana stores) · Noise Canceller (telephony audio) · Solo Ninja

## Why
India has ~13 million kirana stores. Most orders arrive as a phone call or WhatsApp voice note in code-mixed Hindi-English. The owner is busy at the counter, so orders get missed or mis-heard. Kirana Voice answers the call, understands the order, reads it back with the price, and waits for a "haan".

## Gnani AI models used
| Model | Used for |
|---|---|
| **Prisma v3.0** (STT, `indic-auto`) | Transcribes Hindi / Hinglish / Devanagari speech from phone-quality audio, with automatic language detection |
| **Timbre v2.5** (TTS, voice `Nalini`, `hi-IN`) | Speaks the order read-back and total, including rupee numerals; also generates the synthetic test calls |

## How it works
```
caller audio ──▶ Prisma v3.0 ──▶ transcript ──▶ Hinglish order parser ──▶ basket + price
                                                                              │
              caller hears  ◀── Timbre v2.5 ◀── Hinglish reply ◀─────────────┘
```
The parser (`kirana_voice/parser.py`) is deliberately deterministic and offline: it handles Roman and Devanagari spellings, number words (*ek, do, dedh, dhai, aadha, paav*), units (*kilo, gram, litre, packet, dozen*), quantity before or after the item (*"do kilo chawal"* / *"chawal do kilo"*), and multi-turn baskets with confirm / cancel. Same input, same output, 13 unit tests.

## Quick start
```bash
pip install -r requirements.txt
cp .env.example .env && export GNANI_API_KEY=...        # key from app.gnani.ai/voice

python -m pytest                                          # offline parser tests
python -m kirana_voice.cli --text "do kilo chawal aur ek packet maggi" --text "haan"   # no API needed

python -m kirana_voice.cli call1.wav call2.wav --speak    # real audio in, spoken reply out (out/*.wav)
uvicorn kirana_voice.server:app --reload                  # HTTP API, try it at /docs
```

## Noise robustness (synthetic data only, no real calls or personal data)
```bash
python scripts/make_synthetic_calls.py                    # Timbre generates test calls
python scripts/add_noise.py samples/clean samples/noisy --snr 10   # 8 kHz telephony + noise
python scripts/benchmark.py samples/clean samples/noisy   # audio -> Prisma -> order accuracy
```
Results from my run (fill in after you run it):

| set | calls | exact order | item recall |
|---|---|---|---|
| clean 16 kHz | | | |
| noisy 8 kHz, 10 dB SNR | | | |

## Contributions
Solo build: design, parser, API client, server, evaluation, demo.

## Limits (honest)
Catalogue is 16 synthetic items; matching is alias-based, so unseen brands need adding to `catalog.py`. REST STT is capped at 30 s per turn; a production version would use the WebSocket stream (`wss://api.vachana.ai/stt/v3/stream`) for barge-in and lower latency.
