"""FastAPI server: POST an audio turn, get transcript + basket + spoken reply.
Run: uvicorn kirana_voice.server:app --reload   then open http://localhost:8000/docs"""
import base64, tempfile, os, uuid
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Header
from .assistant import Session
from .gnani import GnaniClient

app = FastAPI(title="Kirana Voice", description="Hinglish phone orders on Gnani AI Prisma v3.0 + Timbre v2.5")
SESSIONS = {}
_client = None


def client():
    global _client
    _client = _client or GnaniClient()
    return _client


@app.post("/turn")
async def turn(audio: UploadFile = File(...), session_id: Optional[str] = Header(default=None)):
    sid = session_id or uuid.uuid4().hex
    s = SESSIONS.setdefault(sid, Session())
    suffix = os.path.splitext(audio.filename or "a.wav")[1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(await audio.read())
    try:
        stt = client().transcribe(f.name)
    finally:
        os.unlink(f.name)
    reply = s.handle(stt["transcript"])
    wav = client().synthesize(reply)
    return {
        "session_id": sid, "transcript": stt["transcript"],
        "detected_language": stt.get("detected_language_code"),
        "basket": [{"item": l.item.name, "qty": l.qty, "unit": l.unit, "amount": l.total}
                   for l in s.basket.values()],
        "total": s.total(), "reply_text": reply,
        "reply_audio_wav_b64": base64.b64encode(wav).decode(),
    }
