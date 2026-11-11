#!/usr/bin/env python3
"""Generate a small deterministic theme music bed and four generic WAV cues."""

from __future__ import annotations

import argparse
import wave
from pathlib import Path

import numpy as np

SAMPLE_RATE = 44_100


def write_wav(path: Path, samples: np.ndarray, channels: int = 1) -> None:
    samples = np.clip(samples, -1.0, 1.0)
    if channels == 2 and samples.ndim == 1:
        samples = np.stack([samples, samples * 0.98], axis=1)
    pcm = (samples * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(channels)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(pcm.tobytes())


def tone(freq: float, length: float, amp: float, decay: float) -> np.ndarray:
    size = int(SAMPLE_RATE * length)
    t = np.arange(size) / SAMPLE_RATE
    env = np.minimum(1.0, t / 0.012) * np.exp(-decay * t)
    return amp * env * np.sin(2 * np.pi * freq * t)


def place(target: np.ndarray, sample: np.ndarray, start: float) -> None:
    begin = int(start * SAMPLE_RATE)
    end = min(len(target), begin + len(sample))
    if begin < len(target):
        target[begin:end] += sample[: end - begin]


def make_bgm(duration: float) -> np.ndarray:
    n = int(SAMPLE_RATE * duration)
    t = np.arange(n) / SAMPLE_RATE
    track = np.zeros(n)
    chords = [146.83, 185.00, 220.00, 130.81, 164.81, 196.00]
    for index, start in enumerate(np.arange(0, duration, 4.5)):
        end = min(duration, start + 4.5)
        mask = (t >= start) & (t < end)
        local = t[mask] - start
        env = np.minimum(1.0, local / 0.55) * np.minimum(1.0, (end - t[mask]) / 0.7)
        for freq in chords[index % 3 : index % 3 + 3]:
            track[mask] += 0.034 * env * np.sin(2 * np.pi * freq * local)
    beat = 60.0 / 112.0
    motif = [293.66, 329.63, 369.99, 440.00, 369.99, 329.63]
    for index, start in enumerate(np.arange(0.4, duration, beat)):
        delta = t - start
        hit = delta >= 0
        env = np.where(hit, np.exp(-7.5 * np.maximum(delta, 0)), 0)
        track += 0.06 * env * np.sin(2 * np.pi * motif[index % len(motif)] * np.maximum(delta, 0))
    fade = np.minimum(1.0, t / 0.8) * np.minimum(1.0, (duration - t) / 1.2)
    return np.tanh(track * fade * 1.35)


def make_sfx() -> dict[str, np.ndarray]:
    alarm = np.zeros(int(SAMPLE_RATE * 1.8))
    for index, start in enumerate(np.arange(0, 1.44, 0.24)):
        place(alarm, tone(880 if index % 2 == 0 else 660, 0.18, 0.34, 9.0), start)

    footsteps = np.zeros(int(SAMPLE_RATE * 4.7))
    for index, start in enumerate(np.arange(0.10, 4.65, 0.48)):
        place(footsteps, tone(92 + (index % 2) * 11, 0.16, 0.28, 25.0), start)
        place(footsteps, tone(1450 + (index % 3) * 90, 0.055, 0.12, 55.0), start)

    card = np.zeros(int(SAMPLE_RATE * 0.55))
    place(card, tone(1250, 0.12, 0.32, 18.0), 0.02)
    place(card, tone(1680, 0.12, 0.32, 18.0), 0.20)

    duration = 4.65
    t = np.arange(int(SAMPLE_RATE * duration)) / SAMPLE_RATE
    arrival = 0.18 * np.sin(2 * np.pi * (48 * t + 6 * t * t))
    arrival *= np.minimum(1.0, t / 0.8) * np.minimum(1.0, (duration - t) / 0.55)
    arrival += 0.07 * np.sin(2 * np.pi * (220 + 900 * np.minimum(1.0, t / 3.2)) * t)
    for start, freq in [(3.24, 784.0), (3.45, 988.0), (3.68, 1174.0)]:
        delta = t - start
        hit = delta >= 0
        arrival += 0.16 * np.where(hit, np.exp(-7.5 * np.maximum(delta, 0)), 0) * np.sin(2 * np.pi * freq * np.maximum(delta, 0))
    return {"sfx-alarm.wav": alarm, "sfx-footsteps.wav": footsteps, "sfx-card-beep.wav": card, "sfx-metro-arrival.wav": arrival}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=Path("assets"))
    parser.add_argument("--duration", type=float, default=27.0)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_wav(args.out_dir / "theme-bgm.wav", make_bgm(args.duration), channels=2)
    names = {
        "sfx-alarm.wav": "sfx-start.wav",
        "sfx-footsteps.wav": "sfx-action.wav",
        "sfx-card-beep.wav": "sfx-transition.wav",
        "sfx-metro-arrival.wav": "sfx-result.wav",
    }
    for name, samples in make_sfx().items():
        name = names[name]
        write_wav(args.out_dir / name, samples)
    print(f"generated theme audio in {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
