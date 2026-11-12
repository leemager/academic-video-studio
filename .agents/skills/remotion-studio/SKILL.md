---
name: remotion-studio
description: Build, preview and render Remotion compositions in the academic video studio, with narration-led timing, readable layouts, deterministic animation and versioned exports. Use for the visual edit and video rendering.
---

Use this repository's pinned React/Remotion project, not a second scaffold. Read [production commands](../../../docs/PRODUCTION.md) and inspect package.json and existing scene code before editing. All Remotion packages must share one version. Keep existing projects and selected audio.

Animation must be deterministic from `useCurrentFrame()`, `interpolate()` or `spring()`. Don't rely on CSS animations, timers or unseeded randomness. Put assets under `public/`, use `staticFile()`, Remotion image components and `Audio`/`Video` from `@remotion/media`. Keep fonts local or ensure they finish loading before render. Don't expose implementation details in the video.

Create a topic folder with `npm run new-video`. After voice approval, `tools/prepare-video.mjs` compiles actual passage duration into `src/data/` and updates the registry. `visuals.json` maps passage IDs to layouts; it must not override timing or source text. Narration is one continuous master independent of scene cuts. Chosen transitions are visual overlays and do not subtract time from the audio.

Use clear hierarchy and generous safe margins. For 1080p, begin around 36–48 px body text and 80–130 px headings, then inspect the actual frame and adapt. Don't force every idea into cards or a text slide. Use data-driven charts only with sourced values. A meaningful image or diagram can carry an explanation with less text. Avoid redundant corner labels and small decorative copy.

Run `npm run dev` and open the exact printed URL and composition ID. Inspect actual output; a running process isn't proof of a loaded scene. Use `npm run frames -- <slug>` for representative PNGs and inspect transition frames when changed. Export with `npm run render -- <slug>`; use `--preview` for a smaller copy. Exports get new filenames. Run lint and relevant tests, verify duration/audio, and produce caption timing with the actual lead-frame offset.

For APIs or layouts beyond the included examples, use [official Remotion documentation](https://www.remotion.dev/docs/) and its [official agent skills](https://www.remotion.dev/docs/ai/skills). Those can supplement this self-contained project skill; they are not needed to start. Check current instructions before installing additional skills. Do not install a global plugin silently or replace this project's settings.
