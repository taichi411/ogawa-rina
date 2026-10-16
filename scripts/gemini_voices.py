"""List stored custom Gemini voice IDs without generating or modifying voices."""
import argparse
import html
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request

from gemini_tts import TTSError


def list_voices(key, search="ogawa"):
    if not key or not key.strip():
        raise TTSError("GEMINI_API_KEY is missing. Set the repository Actions secret.")
    if len(search.encode("utf-8")) > 2048:
        raise TTSError("Search must be at most 2048 UTF-8 bytes.")
    voices = []
    token = ""
    seen_tokens = set()
    for _ in range(100):
        params = [("type", "prompted"), ("type", "replicated"), ("page_size", "100")]
        if search:
            params.append(("search", search))
        if token:
            params.append(("page_token", token))
        request = urllib.request.Request(
            "https://generativelanguage.googleapis.com/v1beta/voices?" + urllib.parse.urlencode(params),
            headers={"x-goog-api-key": key.strip()},
            method="GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                result = json.load(response)
        except urllib.error.HTTPError as exc:
            raise TTSError(f"Voices API HTTP {exc.code}. Check key permissions, project access, quota and API availability.") from None
        except (urllib.error.URLError, TimeoutError):
            raise TTSError("Voices API connection failed or timed out.") from None
        except (ValueError, UnicodeError):
            raise TTSError("Voices API returned invalid JSON.") from None
        if not isinstance(result, dict) or not isinstance(result.get("voices", []), list):
            raise TTSError("Voices API returned an unexpected response structure.")
        for voice in result.get("voices", []):
            if not isinstance(voice, dict) or not isinstance(voice.get("id"), str) or not voice["id"]:
                raise TTSError("Voices API returned a voice without a usable ID.")
            # Whitelist metadata. Never save key, sample audio or the raw response.
            voices.append({
                "id": voice["id"],
                "display_name": voice.get("display_name", voice.get("displayName", "")),
                "type": voice.get("type", ""),
                "language_code": voice.get("language_code", voice.get("languageCode", "")),
                "expire_time": voice.get("expire_time", voice.get("expireTime", "")),
            })
        token = result.get("next_page_token", result.get("nextPageToken", ""))
        if not token:
            return voices
        if not isinstance(token, str) or token in seen_tokens:
            raise TTSError("Voices API returned an invalid or repeated page token.")
        seen_tokens.add(token)
    raise TTSError("Voices API pagination exceeded the safety limit; narrow the search.")


def markdown_report(voices):
    def cell(value):
        return html.escape(str(value)).replace("|", "&#124;").replace("\n", " ").replace("\r", " ").replace("`", "&#96;")
    lines = ["# Gemini custom voices", "", f"Found {len(voices)} stored custom voices.", ""]
    if voices:
        lines.extend(["| Display name | Voice ID | Type | Language | Expiry |",
                      "|---|---|---|---|---|"])
        lines.extend("| " + " | ".join(cell(v[k]) for k in
                     ("display_name", "id", "type", "language_code", "expire_time")) + " |" for v in voices)
        lines.extend(["", "Same display name does not mean same voice. Audition candidate IDs before choosing."])
    else:
        lines.append("No matches. Retry with an empty search; then check the account/project used in AI Studio and key access. An empty result does not prove the AI Studio voice was deleted.")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--search", default=os.environ.get("VOICE_SEARCH", "ogawa"))
    parser.add_argument("--output-dir", type=Path, default=Path("out/gemini-voices"))
    args = parser.parse_args()
    try:
        voices = list_voices(os.environ.get("GEMINI_API_KEY"), args.search)
        report = markdown_report(voices)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "voices.json").write_text(json.dumps(voices, ensure_ascii=False, indent=2), encoding="utf-8")
        (args.output_dir / "voices.md").write_text(report, encoding="utf-8")
        summary = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary:
            with open(summary, "a", encoding="utf-8") as output:
                output.write(report)
        print(f"Found {len(voices)} custom voices. Metadata saved in {args.output_dir}.")
        return 0
    except TTSError as exc:
        print(f"Voice listing error: {exc}", file=sys.stderr)
        return 1
    except OSError:
        print("Voice listing error: Unable to save output files.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
