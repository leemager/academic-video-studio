# Starter guide

[Watch the video on YouTube](https://youtu.be/Bbgd8lJnOZ8) · [Subtitles](../../docs/starter-demo.srt)

A 90-second introduction to the studio, narrated in Lee Mager's cloned voice, with German, Italian and Russian examples.

## Edit the guide

- `script.json`: narration text and delivery notes.
- `narration-release.json`: audio filename, hash and timing.
- `captions.words.json` and `starter-demo.srt`: captions with video timing.
- `../../src/data/starter-demo.json`: scene timing and waveform data.
- `../../src/starter/`: the guide's dark-themed visuals and transitions.

The guide uses custom visuals over one continuous narration track. Its audio begins at frame 14 (about 0.467 seconds). Edit its source components and timeline directly.

For a new topic, use `npm run new-video` and the [production workflow](../../docs/PRODUCTION.md). That workflow provides reusable layouts and compiles one visual scene per narration passage.
