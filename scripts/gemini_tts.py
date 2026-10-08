"""Generate speech with Gemini's REST API. Python 3.11+, no dependencies."""
import argparse
import base64
import binascii
import io
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request
import wave


class TTSError(Exception):
    """An actionable error safe to show in CI logs."""


def request_audio(text, style, voice, model, key, timeout=180):
    if not key or not key.strip():
        raise TTSError("GEMINI_API_KEY is missing. Set the repository Actions secret.")
    if not text.strip():
        raise TTSError("Transcript must not be empty.")
    if not re.fullmatch(r"gemini-[a-zA-Z0-9.-]+", model):
        raise TTSError("Invalid Gemini model name.")
    if not voice.strip():
        raise TTSError("Voice must not be empty.")
    part = {"text": text}
    if style.strip():
        part["speech_metadata"] = {"style": style}
    payload = {
        "contents": [{"role": "user", "parts": [part]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"voice": voice}},
        },
    }
    request = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key.strip()},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        hints = {
            400: "Check transcript, voice ID, and request settings; also check API key validity.",
            401: "Check API key validity.",
            403: "Check API key restrictions and project/model access.",
            404: "Check model availability and voice ID.",
            429: "Check quota, rate limits, and billing. Retry manually later.",
        }
        # Never dump the response body, headers, key, or request into logs.
        raise TTSError(f"Gemini HTTP {exc.code}. " + hints.get(exc.code, "Service error; retry manually later.")) from None
    except (urllib.error.URLError, TimeoutError):
        raise TTSError("Gemini connection failed or timed out. Check network and retry manually.") from None
    except (ValueError, UnicodeError):
        raise TTSError("Gemini returned an invalid JSON response.") from None
    if not isinstance(result, dict):
        raise TTSError("Gemini returned an unexpected response structure.")
    candidates = result.get("candidates") or []
    if not candidates:
        raise TTSError("No audio candidate returned. Check content restrictions and model settings.")
    parts = candidates[0].get("content", {}).get("parts", [])
    audio_parts = [p["inlineData"] for p in parts if p.get("inlineData")]
    if len(audio_parts) != 1:
        raise TTSError("Expected one audio part; no complete single-speaker audio was returned.")
    inline = audio_parts[0]
    try:
        data = base64.b64decode(inline.get("data", ""), validate=True)
    except (ValueError, binascii.Error, TypeError):
        raise TTSError("Gemini returned invalid base64 audio.") from None
    return data, inline.get("mimeType", ""), result.get("usageMetadata", {})


def as_wav(data, mime_type):
    if not data:
        raise TTSError("Gemini returned empty audio.")
    if data[:4] == b"RIFF" and data[8:12] == b"WAVE":
        wav_data = data
    elif mime_type.lower().split(";", 1)[0] in ("audio/l16", "audio/pcm"):
        params = {}
        for item in mime_type.split(";")[1:]:
            if "=" in item:
                name, value = item.strip().split("=", 1)
                params[name.lower()] = value
        try:
            rate = int(params.get("rate", "24000"))
            channels = int(params.get("channels", "1"))
        except ValueError:
            raise TTSError("Invalid PCM sample rate or channel count.") from None
        if not 8000 <= rate <= 192000 or channels not in (1, 2) or len(data) % (2 * channels):
            raise TTSError("Invalid 16-bit PCM format or truncated audio.")
        # Gemini's PCM examples use little-endian samples; write a standard WAV header.
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as output:
            output.setnchannels(channels)
            output.setsampwidth(2)
            output.setframerate(rate)
            output.writeframes(data)
        wav_data = buffer.getvalue()
    else:
        raise TTSError("Unsupported audio format; expected WAV or 16-bit PCM.")
    try:
        with wave.open(io.BytesIO(wav_data), "rb") as audio:
            frames = audio.getnframes()
            frame_size = audio.getnchannels() * audio.getsampwidth()
            if frames == 0 or len(audio.readframes(frames)) != frames * frame_size:
                raise TTSError("Empty or truncated WAV audio.")
    except (wave.Error, EOFError):
        raise TTSError("Invalid WAV audio.") from None
    return wav_data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text")
    source.add_argument("--text-file", type=Path)
    parser.add_argument("--style", default=os.environ.get("TTS_STYLE", "Warm, friendly Japanese; natural conversational pace."))
    parser.add_argument("--voice", default=os.environ.get("TTS_VOICE", "Kore"))
    parser.add_argument("--model", default=os.environ.get("TTS_MODEL", "gemini-3.8-flash-tts"))
    parser.add_argument("--output", type=Path, default=Path("out/gemini-tts/output.wav"))
    args = parser.parse_args()
    try:
        text = args.text_file.read_text(encoding="utf-8") if args.text_file else args.text
        if text is None:
            text = os.environ.get("TTS_TEXT", "こんにちは。音声生成の接続テストです。")
        data, mime, usage = request_audio(text, args.style, args.voice, args.model, os.environ.get("GEMINI_API_KEY"))
        wav_data = as_wav(data, mime)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(wav_data)
        # No transcript, style, credentials, or raw API responses in the report.
        report = {"model": args.model, "voice": args.voice, "mime_type": mime,
                  "audio_bytes": len(wav_data), "usage": usage}
        args.output.with_suffix(".json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Audio saved: {args.output} ({len(wav_data)} bytes)")
        return 0
    except TTSError as exc:
        print(f"TTS error: {exc}", file=sys.stderr)
        return 1
    except OSError:
        print("TTS error: Unable to read the transcript or save output files.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
