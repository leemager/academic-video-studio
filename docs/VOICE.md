# Set up your own cloned voice

Give Codex an MP3 recording of your voice, around 15 seconds long. Use one speaker, a quiet room and no background music. An ordinary microphone or a clean excerpt from an existing recording can work.

Codex transcribes the recording automatically and shows you the words for a quick check, particularly names or specialist terms. You only need to supply the audio. Keep the original recording for future use.

## For Codex: transcribe the recording

Place the original under `notes/voice-input/` and run:

```sh
npm run transcribe-reference -- --audio notes/voice-input/original.mp3 --output notes/voice-input/transcript.txt --language en
```

Use the recording's language code, or omit `--language` for detection. This uses local faster-whisper on the CPU; it needs no GPU, plugin or API key. The full setup includes the multilingual Whisper small model. The command can also download that pinned model on first use or use an existing model with `--model-dir`.

Show the transcript for a quick check and clarify unclear names or phrases. The `.asr.json` alongside it contains word timings and confidence for inspection. Keep the words actually spoken, including grammatical slips; the reference transcript must match the audio. Then register the checked transcript below.

For an audio-only installation, Codex should install `faster-whisper==1.2.1` into the interpreter recorded in `.runtime/local.json` using the local uv installer. If that package is unavailable for the machine, set up a compatible local transcription engine, such as whisper.cpp. Produce the same UTF-8 transcript file; the academic still only supplies the recording.

## For Codex: register the reference

After checking the generated transcript:

```sh
npm run register-voice -- --audio notes/voice-input/original.mp3 --transcript notes/voice-input/transcript.txt --name "Your name"
npm run voice -- --check
```

The tool accepts 3–60 seconds of speech. It copies the original, converts the complete recording to mono 24 kHz WAV, and creates `voices/local/profile.json` with reference hashes and generation settings. Use the original human recording as input.

For a different reference, use `--id local-v2`, then pass `--profile voices/local-v2/profile.json` to generation or set `profile` in `.runtime/local.json`. Use `--language fr` or another supported code as appropriate.

## Try a short sample

```sh
npm run voice -- --script projects/starter-demo/smoke-script.json --output voiceover/benchmark-001
```

Present the audio, inspect `transcription-qa.json`, and read the device and generation time from the output records. Use a new take folder for each alternative. Save pronunciation preferences in the voice folder's `preferences.json`.

For revisions, use the [audition workflow](PRODUCTION.md#voice-alternatives). The academic chooses a reading and Codex applies that exact audio.

## Keep the voice for future projects

Back up the original recording, transcript, profile and selected narration along with the editable projects. These personal files are excluded from Git uploads by default.

The same original recording and transcript can be used in the [VoiceStudio desktop app](VOICESTUDIO.md) and this studio's scripted renderer.
