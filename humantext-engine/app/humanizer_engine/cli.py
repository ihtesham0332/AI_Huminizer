from __future__ import annotations
import argparse, json, os, sys

from .pipeline import HumanizerEngine
from .providers import AnthropicProvider, MockProvider


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="humanize", description="Humanizer Engine CLI")
    ap.add_argument("file", help="text file, or - for stdin")
    ap.add_argument("--level", type=int, default=3)
    ap.add_argument("--tone", default="standard")
    ap.add_argument("--voice", help="file containing a sample of your own writing")
    ap.add_argument("--provider", choices=["mock", "anthropic"],
                    default="anthropic" if os.environ.get("ANTHROPIC_API_KEY") else "mock")
    ap.add_argument("--json", action="store_true", help="print full JSON result")
    a = ap.parse_args(argv)

    text = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    voice = open(a.voice, encoding="utf-8").read() if a.voice else None
    provider = AnthropicProvider() if a.provider == "anthropic" else MockProvider()
    res = HumanizerEngine(provider).humanize_sync(text, level=a.level, tone=a.tone, voice_sample=voice)
    print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False) if a.json else res.text)
    print("\n--- report ---\n" + json.dumps(res.report, indent=2), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
