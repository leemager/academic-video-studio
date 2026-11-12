# VoiceStudio and this starter

[VoiceStudio](https://github.com/debpalash/VoiceStudio) is a local desktop interface for voice cloning and related audio tasks. This repository supplies a separate scripted production path using public OmniVoice, one of its engines. They can use the **same original human recording and accurate transcript**. The template does not depend on a particular private VoiceStudio installation or copy its application code.

## Install the desktop app when wanted

Codex should inspect the computer, read the matching current official guide, select the official release for that architecture and help the academic through any unavoidable installer/first-run prompts. Use the packaged stable release rather than building the app from source by default. The app's packaging changes; don't rely on old installer filenames in this template.

- [Official releases](https://github.com/debpalash/VoiceStudio/releases/latest)
- [Windows installation](https://github.com/debpalash/VoiceStudio/blob/main/docs/install/windows.md)
- [macOS installation](https://github.com/debpalash/VoiceStudio/blob/main/docs/install/macos.md)
- [Linux installation](https://github.com/debpalash/VoiceStudio/blob/main/docs/install/linux.md)

The current guides describe Windows x64, Apple Silicon macOS and Linux x64 desktop packages, plus some experimental configurations. Intel Mac local backends remain unsupported. Keep installed app/model versions and use the release's checksums/signatures where supplied. Don't disable OS protection or an institution's software controls to make an installer run. The repository-local scripted route remains available on its supported platforms if the GUI is unnecessary.

## Create and reuse a voice

1. Record/import a clean original clip in the app's voice-cloning workflow. Use only your own voice or an authorised speaker. Keep the original audio and correct transcript in your private project folder.
2. Choose OmniVoice for compatibility with this starter's default renderer. Generate a short, natural test; check identity, wording and accent. The app supports other engines, but their profiles and settings are not automatically interchangeable.
3. Give Codex the original clip and transcript. It runs this repository's registration command, creating an ignored profile. There is no need to train a new model or copy a desktop-app database.
4. Let Codex generate the production passages, inspect transcript QA, and show alternatives through the included browser audition page. All repeatable settings, selected hashes and output timing stay in the project.

If you prefer to generate narration in VoiceStudio itself, export whole passages as WAV and use `tools/import-narration.py` with an approved script and an ordered file list. This imports the actual audio, preserves originals and creates the timeline manifest. Do not pass a generated WAV to `register-voice.py` as a new reference. Re-rendering with the same seed/settings can still differ across app/engine versions.

The desktop app and scripted runtime may each download models and use separate caches. Allow extra disk space; don't silently repoint or remove an existing application cache. No cloud worker is enabled by this template. If local performance is inadequate, an explicitly agreed other machine or a human recording is a valid production route.

VoiceStudio's application licence, the selected engine's model licence and the audio tokenizer's terms are separate. Read [the notices](../THIRD-PARTY-NOTICES.md). Calling software “local” describes where it runs, not blanket rights to every possible use.
