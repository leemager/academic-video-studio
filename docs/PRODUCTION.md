# Production commands — for Codex

Use `npm run ...` below or the recorded local Node with `tools/run.mjs run ...`. Commands run from the repository root. New takes/exports are immutable; use unique paths. The academic should normally direct the result without running these commands.

## Sources, script and project

```sh
npm run new-video -- my-topic "An introduction to my topic"
```

The new `projects/my-topic/` contains an outline, sources list, script and visual spec. Ground the outline and script in materials under `notes/`. Keep approved script text intact. A script is an array of complete passages:

```json
[{"id":"opening","text":"The approved words to speak.","pause_after":0,"seed":42,"speed":1.0,"language":"en","prosody":{"function":"introduce the question","ending":"neutral_fall"}}]
```

Optional `tts_text` contains only reviewed pronunciation/reading variants; QA/captions use `text`. Prosody metadata records editorial intent and does not directly control the engine. Keep passages coherent and short enough for targeted retakes. Don't split every sentence mechanically.

## Generate and check

```sh
npm run voice -- --script projects/my-topic/script.json --output voiceover/my-topic/take-01
```

Read `manifest.json`, `transcription-qa.json` and the scene records. Speech should be finite, intelligible, complete and unclipped. ASR differences are flags to inspect, not automatic failures. `--no-transcribe` is for quick auditions; final narration needs transcription. `--resume` may only resume an incomplete take with identical inputs; new wording/settings require a new folder. `--device cpu` is available for a separately benchmarked fallback.

The renderer writes original passage WAVs, a raw assembled master, a loudness-normalised master, manifest and word/caption data. It never trims internal words or imposes sentence gaps. New human or desktop-app narration can be imported without a GPU:

```json
[{"id":"opening","file":"notes/exported/opening.wav"}]
```

Save that list as `projects/my-topic/imports.json`, then:

```sh
npm run python -- tools/import-narration.py --script projects/my-topic/script.json --files projects/my-topic/imports.json --output voiceover/my-topic/import-01 --synthetic
```

Omit `--synthetic` for a real human recording. Import needs the audio utilities from the voice or audio-only Python environment, but no inference/model weights. On an Intel Mac the bootstrap automatically installs the lightweight audio environment. On another machine use `--audio-only` (`-AudioOnly` on Windows) if that is all you need. This does not fabricate a clone/reference provenance.

## Voice alternatives

Generate one or two whole-passage retakes into fresh folders. Prepare an audition specification:

```json
{"slug":"opening-01","title":"Opening: a more neutral ending","passageId":"opening","text":"The approved words to speak.","takes":[{"file":"voiceover/my-topic/retake-a/scenes/01-opening.wav","label":"Take A","note":"Neutral ending"},{"file":"voiceover/my-topic/retake-b/scenes/01-opening.wav","label":"Take B","note":"Alternative phrasing"}]}
```

```sh
node tools/create-audition.mjs projects/my-topic/audition-01.json
npm run auditions -- opening-01
```

Open the printed loopback URL in Codex. The UI plays complete WAVs, uses hash-named assets, disables caching and saves the chosen hash under `voiceover/selections/`. A saved choice is not automatically installed in the video. Apply it explicitly:

```sh
npm run python -- tools/voice/assemble.py --base voiceover/my-topic/take-01 --output voiceover/my-topic/take-02 --selection voiceover/selections/CHOSEN-FILE.json
npm run voice -- --output voiceover/my-topic/take-02 --transcribe-only
```

Read the actual chosen filename from the UI/selection folder; `CHOSEN-FILE.json` is illustrative. Assembly preserves each chosen passage byte-for-byte and leaves other selected passages untouched. Changed academic text requires an explicitly reviewed script update and a new narration take. Never pretend an older selected waveform says revised words.

## Visuals and timing

Edit `visuals.json`, keyed by passage ID:

```json
{"opening":{"kind":"statement","title":"One clear idea","detail":"A useful explanation","beats":["A concrete example"],"transition":false}}
```

Layouts: `statement`, `text`, `names`, `book`, `network` (three beats), `contrast`, `growth` (label|numeric value), `timeline`, `hero`, `photo`, `portrait`, `quote`, `closing`. Image layouts require an explicit path under `public/`, e.g. `my-topic/images/photo.jpg`; no implicit institution assets exist. Adapt or add layouts when the idea needs them. Keep on-screen text concise. Put licences in the project's source/asset list.

Set the academic's name, credits, title and optional `leadFrames`/`tailFrames` in `project.json`. Then:

```sh
node tools/prepare-video.mjs my-topic voiceover/my-topic/take-02
npm run dev
```

The helper checks the master hash, uses measured timing, writes a content-hash-named public audio file, saves previous compiled edits, and registers the composition. Open the exact composition URL from Studio, normally `/MyTopic`. Check the selected audio in the composition itself. A wipe/swoosh is opt-in per scene with `transition:true`; narration continues uninterrupted.

## Captions and export

```sh
npm run lint
npm run frames -- my-topic
npm run render -- my-topic --preview
npm run render -- my-topic
npm run python -- tools/voice/export-captions.py --take voiceover/my-topic/take-02 --alignment voiceover/my-topic/take-02 --output renders/my-topic-v1.srt --offset 1.5
```

The caption offset must be `leadFrames / fps`, not always 1.5. Use a unique SRT name and rename/copy it alongside its matching MP4. The exporter uses approved spelling and ASR timing, recording approximate spans. Review those spans and specialist names. It is never an audio cutting tool. For imported audio without ASR, transcribe with a supported local transcription tool and create verified captions; don't invent precise timing.

Inspect representative frames and transitions with an image viewer. Probe the final file using FFprobe (if installed) or Remotion's media inspection; verify dimensions, duration, audio stream, clipping/levels and playback. Be explicit when only machine checks were possible. Keep the final editable sources, captions and asset/source list. Ask the academic for final content/listening review where needed; don't publish automatically.
