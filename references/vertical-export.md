# 9:16 portrait export

Use a separate composition under `compositions/vertical.html`. Keep the same scene IDs, audio cue times, and landmark asset so the portrait cut remains the same story, then add a portrait override stylesheet.

## Layout rules

- Set the root metadata to `data-width="1080" data-height="1920"`.
- Size the composition with `width: min(100vw, 56.25vh)` and `height: min(100vh, 177.7778vw)` when it is previewed in a browser.
- Let background images bleed 2–4% outside the scene and use `background-size: cover`; this avoids edge gaps when the camera nudges.
- Keep captions within roughly 8–92% of the width and reserve the lower 15–18% for the caption plate.
- Make the hero subject or landmark large enough to read on the title card. Keep its center and whole silhouette visible.
- Put important scene labels or signs near the upper safe zone, with no text closer than 7% to a side edge.
- Reposition characters to the lower third and keep props from crossing the caption plate.
- Use larger type than the landscape version; a portrait caption normally needs 30–58px at 1080px width.

## Render

```bash
npm run render:vertical
```

The render wrapper should call HyperFrames with `--composition compositions/vertical.html --resolution portrait --fps 30 --quality delivery --low-memory-mode`. Probe the result for 1080×1920 and extract frames at 0s, 3s, 6s, 12s, 18s, 21s, 24s, and 26.5s.

## Common fixes

- If a landmark is clipped, reduce its width before reducing its opacity or detail.
- If captions wrap into three or more lines, shorten the copy or reduce letter spacing before shrinking the font.
- If the scene appears to have a black edge, increase the background bleed rather than scaling the whole scene.
- If a portrait composition is placed under `compositions/`, use project-root asset paths (`assets/foo.png`); parent traversal paths such as `../assets/foo.png` are rejected by HyperFrames lint.
