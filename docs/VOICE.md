# Set up your own cloned voice

Codex should carry out the commands. The academic supplies the recording and checks the short result.

## Reference recording

Use your own original speech, or a speaker whose voice use is authorised. Aim for 10–25 seconds of clean, natural speech with one speaker, no music and little room echo. Three to sixty seconds is accepted by the registration tool. Avoid a sentence cut halfway through a word or breath. An ordinary microphone or a clean excerpt from an existing recording can work.

Provide a UTF-8 text file containing the words actually spoken, including false starts if present. It is not the script you wish the recording contained. Codex can transcribe locally and ask you to verify uncertainties. Keep the original recording; any carefully selected excerpt becomes a separately versioned reference. Don't clone from generated output.

## Register the reference

After setup, place the files under `notes/voice-input/`, then run:

```sh
npm run register-voice -- --audio notes/voice-input/original.wav --transcript notes/voice-input/transcript.txt --name "Your name"
npm run voice -- --check
```

The helper copies the original, converts the complete recording to mono 24 kHz WAV without timing cuts, saves an accurate transcript, records both hashes and creates `voices/local/profile.json`. Existing profiles are never overwritten. Use `--id local-v2` for another reference and pass `--profile voices/local-v2/profile.json` to generation, or set `profile` in ignored `.runtime/local.json`. Use `--language fr` or another supported lowercase language code when appropriate.

The clone uses a reference at generation time; it is not a separately trained model. Future inference still needs the engine and model weights. The profile defaults are a starting point, not a promise of identity or perfect prosody.

## Benchmark before a long job

```sh
npm run voice -- --script projects/starter-demo/smoke-script.json --output voiceover/benchmark-001
```

Use a new output path each time. Read the actual device, duration and generation times from the manifest and scene records. Model loading and transcription add time beyond synthesis. Present the short WAV to the academic and inspect `transcription-qa.json`. If the result is unclear or the voice is wrong, improve the reference before making a long video.

Record confirmed accent, names and emphasis preferences in the voice folder's `preferences.json`. Never assume another speaker's preferences. For revisions use the [whole-passage audition workflow](PRODUCTION.md#voice-alternatives).

## Privacy and portability

`voices/`, `voiceover/` and `notes/` are ignored. Neither Git push nor the shared template backs these up. Keep a private, authorised backup of the original human recording, transcript, profiles, approved waveforms and selection records. The portable inputs are the original reference, transcript and settings; exact approved output files remain necessary to preserve approved delivery.

See [VoiceStudio](VOICESTUDIO.md) if you want a desktop recording/cloning interface. Use the original reference and transcript across both workflows. A VoiceStudio-generated WAV is an output, not the identity reference.
