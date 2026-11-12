# Academic video studio

Turn lecture notes, papers and other source material into reusable videos with your own cloned narration. **You are the academic director. Codex does the production.**

Use it for course introductions, prerequisite explanations, research summaries, methods walkthroughs or any stable information that benefits from being recorded once. Direct the work in ordinary language: change the argument, fix a pronunciation, simplify a diagram or ask for a different visual style.

![The included neutral Remotion example](docs/starter-preview.png)

## Start here

1. Get your own copy of this private template. The owner must grant you access first. Use **Use this template → Create a new repository**, choose **Private**, then clone it; or download a ZIP and extract it into your own folder. See [sharing and access](docs/SHARING.md).
2. Open that folder as a project in Codex. Paste [STARTER-PROMPT.txt](STARTER-PROMPT.txt). Codex will inspect your computer, set up the local tools and open the neutral example.
3. Provide a clean recording of **your own speaking voice**, ideally 10–25 seconds, plus the words you actually said. Codex will help create and test your voice profile. If you already use VoiceStudio, keep the original recording and transcript; a generated sample is not a new reference.
4. Add your lecture notes, papers or other sources under `notes/`, then describe what you want.

You do not need to learn video editing, Python or Remotion. The setup scripts and technical guides are for Codex to use on your behalf. Operating-system sign-in, installer or microphone prompts may still need your interaction.

After setup, try:

> I've added lecture notes and relevant papers in notes/my-topic. Please draft an outline for a five-minute introduction for first-year students, using my cloned voice. Show me the outline and script before producing it. Explain the central idea with one concrete example and leave a question for the seminar.

Or:

> Use the materials in notes/my-paper to propose a three-minute research explainer for an interdisciplinary audience. Keep the findings distinct from their limitations, and show me the source of each important claim.

## What is included

- Windows, macOS and Linux setup entry points, hardware checks and measured voice benchmarks.
- A [VoiceStudio guide](docs/VOICESTUDIO.md), plus a scripted local OmniVoice renderer for repeatable production.
- Voice registration, complete-passage retakes, A/B audition pages and exact selected-audio tracking.
- Production, voice and Remotion skills that travel with the repository.
- Transcript checks, captions, optional acoustic triage, reusable scene layouts and versioned MP4 exports.
- A neutral 20-second visual example, **StarterDemo**, that needs no voice setup. It contains no lecture content or personal assets.

No voice reference, real lecture, institution branding or model weights are distributed. Your notes, voice, generated audio and working projects are ignored by Git by default. Keep a separate private backup: ignored files are **not** backed up by a Git push.

## Computer expectations

| Computer | Video preview/render | New cloned narration |
| --- | --- | --- |
| Windows x64 | Supported setup | NVIDIA CUDA or slower CPU |
| Apple Silicon Mac | Supported setup | Integrated GPU via MPS; CPU fallback |
| Linux x64 | Supported setup; browser libraries may be needed | NVIDIA CUDA or slower CPU |
| Intel Mac | Preview/render and imported audio | Current pinned voice stack unsupported |
| Windows/Linux ARM or other accelerators | Inspect platform support first | Not validated by this template; don't assume support |

A discrete GPU is not mandatory on the supported CPU/Apple Silicon paths, but a small laptop may be slow or memory-constrained. First setup downloads several GB. Plan for at least 15 GB free for the scripted stack, more if installing the desktop app and saving renders. Codex should benchmark a short passage before estimating a long video.

## Guides

- [First-time setup](docs/SETUP.md) · [Your voice](docs/VOICE.md) · [VoiceStudio](docs/VOICESTUDIO.md)
- [Everyday direction and example prompts](docs/DIRECTING.md) · [Production commands](docs/PRODUCTION.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md) · [Sharing and private backups](docs/SHARING.md)
- [Software/model terms](THIRD-PARTY-NOTICES.md) · [Asset credits](ASSET-CREDITS.md) · [Validation record](docs/VALIDATION.md)

Local synthesis does not make material read by Codex private to your institution. Use your approved account and data policy. Upstream model and software terms also apply: the current OmniVoice model card describes non-commercial weights, and Remotion's FAQ has specific requirements for educational institutions. See the linked terms before institutional deployment or commercial reuse.
