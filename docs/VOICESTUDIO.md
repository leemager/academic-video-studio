# VoiceStudio and this starter

[VoiceStudio](https://github.com/debpalash/VoiceStudio) is a desktop app for voice cloning and audio production. This starter also includes a scripted renderer using OmniVoice, one of its engines, so Codex can generate narration directly. Both use the same original recording and transcript.

## Install the desktop app

Ask Codex to help install the stable release for your computer. It will follow the appropriate guide and explain any installer prompts:

- [Official releases](https://github.com/debpalash/VoiceStudio/releases/latest)
- [Windows](https://github.com/debpalash/VoiceStudio/blob/main/docs/install/windows.md)
- [macOS](https://github.com/debpalash/VoiceStudio/blob/main/docs/install/macos.md)
- [Linux](https://github.com/debpalash/VoiceStudio/blob/main/docs/install/linux.md)

You can also use the starter's scripted workflow without installing the desktop app.

## Create and reuse your voice

1. Give Codex a clean recording of your voice. It transcribes the clip locally and shows you the words for a quick check. Keep that original audio and checked transcript for VoiceStudio's voice-cloning workflow.
2. Choose OmniVoice to use the same engine as this starter. Generate a short sample and check the reading.
3. Codex registers the original clip and its checked transcript for use across your video projects.
4. Let Codex generate the narration and show alternative readings in the browser audition page whenever you want a retake.

If you prefer to generate narration in VoiceStudio itself, export complete passages as WAV files. Codex can import them with `tools/import-narration.py` and build the video around their timing. Other VoiceStudio engines may have different settings; use their exported audio with the import workflow.

The desktop app and scripted runtime may download separate model files, so allow extra disk space if you install both.

Read the [notices](../THIRD-PARTY-NOTICES.md) for more information about permitted uses.
