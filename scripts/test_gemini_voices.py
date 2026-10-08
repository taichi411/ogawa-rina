import io
import json
import unittest
import urllib.error
import urllib.parse
from unittest.mock import patch

import gemini_voices as voices
from gemini_tts import TTSError


class VoiceTests(unittest.TestCase):
    def test_pages_preserve_same_named_voices_and_strip_sensitive_fields(self):
        pages = [
            {"voices": [{"id": "voice_a", "display_name": "ogawa-rena 3", "key": "private", "sample_audio": {"data": "private"}}], "next_page_token": "next"},
            {"voices": [{"id": "voice_b", "displayName": "ogawa-rena 3"}]},
        ]
        with patch("urllib.request.urlopen", side_effect=[io.BytesIO(json.dumps(p).encode()) for p in pages]) as connect:
            result = voices.list_voices("secret-key", "ogawa")
        self.assertEqual([v["id"] for v in result], ["voice_a", "voice_b"])
        self.assertEqual(result[1]["display_name"], "ogawa-rena 3")
        self.assertNotIn("private", json.dumps(result))
        for call in connect.call_args_list:
            request = call.args[0]
            query = urllib.parse.parse_qs(urllib.parse.urlparse(request.full_url).query)
            self.assertEqual(query["type"], ["prompted", "replicated"])
            self.assertEqual(query["search"], ["ogawa"])
            self.assertNotIn("secret-key", request.full_url)
        self.assertEqual(query["page_token"], ["next"])

    def test_missing_key_never_connects(self):
        with patch("urllib.request.urlopen") as connect:
            with self.assertRaises(TTSError):
                voices.list_voices(None)
            connect.assert_not_called()

    def test_empty_list_and_repeated_page_token(self):
        with patch("urllib.request.urlopen", return_value=io.BytesIO(b"{}")):
            self.assertEqual(voices.list_voices("test-key", ""), [])
        pages = [io.BytesIO(b'{"nextPageToken":"repeat"}') for _ in range(2)]
        with patch("urllib.request.urlopen", side_effect=pages):
            with self.assertRaisesRegex(TTSError, "repeated"):
                voices.list_voices("test-key")

    def test_http_error_does_not_expose_key(self):
        error = urllib.error.HTTPError("https://example.invalid", 403, "secret-key", {}, None)
        with patch("urllib.request.urlopen", side_effect=error):
            with self.assertRaises(TTSError) as caught:
                voices.list_voices("secret-key")
        self.assertIn("403", str(caught.exception))
        self.assertNotIn("secret-key", str(caught.exception))

    def test_report_escapes_table_markup(self):
        record = {"display_name": "a|b\n<script>", "id": "voice_a", "type": "prompted", "language_code": "ja-JP", "expire_time": ""}
        report = voices.markdown_report([record])
        self.assertIn("a&#124;b &lt;script&gt;", report)
        self.assertNotIn("<script>", report)


if __name__ == "__main__":
    unittest.main()
