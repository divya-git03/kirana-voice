"""Thin client for Gnani AI's Vachana API: Prisma v3.0 (STT) and Timbre v2.5 (TTS)."""
import os
import requests

BASE = "https://api.vachana.ai"


class GnaniError(RuntimeError):
    pass


class GnaniClient:
    def __init__(self, api_key=None, timeout=60):
        self.api_key = api_key or os.environ.get("GNANI_API_KEY")
        if not self.api_key:
            raise GnaniError("Set GNANI_API_KEY (see .env.example).")
        self.timeout = timeout

    @property
    def _h(self):
        return {"X-API-Key-ID": self.api_key}

    def transcribe(self, audio_path, language_code="indic-auto", model="prisma-v3.0"):
        """Speech to text. Prisma v3.0 auto-detects Indian languages and code-mixed speech.
        REST limits: <= 30 s, 8-44.1 kHz."""
        with open(audio_path, "rb") as f:
            r = requests.post(
                f"{BASE}/stt/v3",
                headers=self._h,
                files={"audio_file": (os.path.basename(audio_path), f)},
                data={"model": model, "language_code": language_code},
                timeout=self.timeout,
            )
        if r.status_code != 200:
            raise GnaniError(f"STT failed [{r.status_code}]: {r.text[:300]}")
        return r.json()

    def synthesize(self, text, voice="Nalini", language="hi-IN", sample_rate=16000):
        """Text to speech with Timbre v2.5. Returns WAV bytes."""
        payload = {
            "text": text, "voice": voice, "model": "timbre-v2.5",
            "language": language, "speed": 1.0,
            "audio_config": {"sample_rate": sample_rate, "num_channels": 1,
                             "sample_width": 2, "encoding": "linear_pcm",
                             "container": "wav"},
        }
        r = requests.post(f"{BASE}/api/v1/tts/inference",
                          headers={**self._h, "Content-Type": "application/json"},
                          json=payload, timeout=self.timeout)
        if r.status_code != 200:
            raise GnaniError(f"TTS failed [{r.status_code}]: {r.text[:300]}")
        return r.content
