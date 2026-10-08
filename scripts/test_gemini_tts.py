import base64
import io
import json
import unittest
import urllib.error
from unittest.mock import patch
import wave

import gemini_tts as tts


class AudioTests(unittest.TestCase):
    def test_pcm_becomes_playable_wav(self):
        data = tts.as_wav(b"\x00\x00" * 2400, "audio/L16;rate=24000")
        with wave.open(io.BytesIO(data), "rb") as audio:
            self.assertEqual(audio.getframerate(), 24000)
            self.assertEqual(audio.getnframes(), 2400)
            self.assertEqual(audio.getnchannels(), 1)
        self.assertEqual(tts.as_wav(data, "audio/wav"), data)

    def test_rejects_empty_truncated_or_unknown_audio(self):
        for data, mime in [(b"", "audio/wav"), (b"x", "audio/L16"),
                           (b"RIFFxxxxWAVE", "audio/wav"), (b"abc", "audio/mpeg")]:
            with self.subTest(mime=mime), self.assertRaises(tts.TTSError):
                tts.as_wav(data, mime)

    def test_missing_key_never_connects(self):
        with patch("urllib.request.urlopen") as connect:
            with self.assertRaisesRegex(tts.TTSError, "GEMINI_API_KEY"):
                tts.request_audio("こんにちは", "", "Kore", "gemini-3.8-flash-tts", None)
            connect.assert_not_called()

    def test_rest_request_and_audio_part_after_text(self):
        result = {"candidates": [{"content": {"parts": [
            {"text": "metadata"}, {"inlineData": {
                "mimeType": "audio/L16;rate=24000", "data": base64.b64encode(b"\x00\x00").decode()}}
        ]}}]}
        with patch("urllib.request.urlopen", return_value=io.BytesIO(json.dumps(result).encode())) as connect:
            audio, mime, _ = tts.request_audio("こんにちは<laugh>", "cheerful", "Kore", "gemini-3.8-flash-tts", "test-key")
        request = connect.call_args.args[0]
        payload = json.loads(request.data)
        self.assertNotIn("test-key", request.full_url)
        self.assertEqual(request.get_header("X-goog-api-key"), "test-key")
        self.assertEqual(payload["contents"][0]["parts"][0], {"text": "こんにちは<laugh>", "speech_metadata": {"style": "cheerful"}})
        self.assertEqual(payload["generationConfig"]["speechConfig"]["voiceConfig"], {"voice": "Kore"})
        self.assertEqual(audio, b"\x00\x00")
        self.assertEqual(mime, "audio/L16;rate=24000")

    def test_http_errors_do_not_expose_response_or_key(self):
        error = urllib.error.HTTPError("https://example.invalid", 403, "secret-key", {}, io.BytesIO(b"secret-key"))
        with patch("urllib.request.urlopen", side_effect=error):
            with self.assertRaises(tts.TTSError) as caught:
                tts.request_audio("hello", "", "Kore", "gemini-3.8-flash-tts", "secret-key")
        self.assertIn("403", str(caught.exception))
        self.assertNotIn("secret-key", str(caught.exception))

    def test_missing_candidate_and_invalid_base64_fail(self):
        for result in [{}, {"candidates": [{"content": {"parts": [
            {"inlineData": {"mimeType": "audio/wav", "data": "!invalid!"}}
        ]}}]}]:
            with patch("urllib.request.urlopen", return_value=io.BytesIO(json.dumps(result).encode())):
                with self.assertRaises(tts.TTSError):
                    tts.request_audio("hello", "", "Kore", "gemini-3.8-flash-tts", "test-key")


if __name__ == "__main__":
    unittest.main()
