#!/usr/bin/env python3
"""Check a rendered MP4's dimensions, duration, codecs, and audio presence."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--ffprobe", default="ffprobe")
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--max-duration", type=float, required=True)
    args = parser.parse_args()

    if not args.video.exists():
        raise SystemExit(f"missing video: {args.video}")

    command = [
        args.ffprobe,
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=codec_type,codec_name,width,height",
        "-of",
        "json",
        str(args.video),
    ]
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
    except FileNotFoundError as exc:
        raise SystemExit(f"ffprobe not found: {args.ffprobe}") from exc
    payload = json.loads(result.stdout)
    streams = payload.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    duration = float(payload.get("format", {}).get("duration", 0))
    errors: list[str] = []
    if not video:
        errors.append("no video stream")
    else:
        if video.get("width") != args.width or video.get("height") != args.height:
            errors.append(f"dimensions {video.get('width')}x{video.get('height')} != {args.width}x{args.height}")
        if video.get("codec_name") != "h264":
            errors.append(f"video codec {video.get('codec_name')} != h264")
    if not audio:
        errors.append("no audio stream")
    elif audio.get("codec_name") != "aac":
        errors.append(f"audio codec {audio.get('codec_name')} != aac")
    if duration <= 0 or duration > args.max_duration:
        errors.append(f"duration {duration:.3f}s exceeds {args.max_duration:.3f}s")

    print(json.dumps({"video": video, "audio": audio, "duration": duration}, ensure_ascii=False, indent=2))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("render check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
