# Academic video studio

The academic directs the content; Codex handles setup, source organisation, narration, visuals, previews, retakes, captions and export. Ask about academic choices and missing inputs, not routine implementation details. Give plain-language updates and concrete review links.

Read `.agents/skills/academic-video-production/SKILL.md` for video work, `.agents/skills/academic-voiceover/SKILL.md` for voice work, and `.agents/skills/remotion-studio/SKILL.md` for the edit. These skills are included in the repository. If discovery is unavailable, read them explicitly. Setup starts in `docs/SETUP.md` and voice registration in `docs/VOICE.md`.

This is an unpersonalised template. No human voice, lecture, institution or model weights are supplied. Never substitute a voice from another workspace. Ask for the user's own original recording and its accurate transcript, or an explicitly authorised speaker. The default active profile is `voices/local/profile.json`, ignored by Git. A saved clone is a reference and settings, not a portable GPU: synthesis still needs computation.

Inspect the actual OS, architecture, memory and GPU. Support Windows, macOS and Linux using the documented paths, with a short measured benchmark. Do not promise every architecture can run the local voice stack. Intel Macs and unsupported ARM configurations can edit/render and import narration. No cloud voice service, remote GPU upload, purchase or publication unless authorised by the user. Explain licensing constraints from THIRD-PARTY-NOTICES.md when relevant to intended deployment.

Use Remotion. VoiceStudio is the optional desktop interface for recording, testing and exporting a clone; the included scripted renderer uses its underlying public OmniVoice engine independently. Follow docs/VOICESTUDIO.md when installing or using that app. Do not require DaVinci Resolve, a paid TTS API, or a global skill installation.

An outline request means an outline for academic review. Ground claims in supplied sources with page/section references; mark gaps. Obtain script approval before a long narration unless the user already approved exact text or told you to proceed. Preserve exact supplied text separately from pronunciation cues. Keep course introductions, research explanations and other reusable information focused on stable content; mark facts that need future review.

Plan meaning and emphasis before synthesis. Generate coherent passages with natural breaths. Never cut at ASR word timestamps or insert uniform sentence pauses. Use whole-passage alternatives and the browser audition UI when needed. An approved waveform and hash are authoritative; preserve all other approved passages. Acoustic scores are triage, not proof of naturalness.

Use readable typography, purposeful imagery/diagrams, restrained transitions and occasional quiet effects. Avoid repeated corner labels, decorative micro-text and redundant taglines. No music by default; follow the academic's brief. Narration stays continuous across visual cuts. Keep asset provenance and licences.

Preserve source documents, references, approved audio, previous renders and audit records. Never permanently delete pre-existing generated/cache/ignored/untracked files without explicit approval. Disposable bounded task-owned temporary files may be cleaned; do not follow links or clean shared roots. Never weaken deletion hooks. Use unique take folders and versioned exports.

Personal notes, voice files, working projects, generated narration and local runtime config are ignored. Do not force-add them. A private GitHub repository is still a remote upload. Sharing a finished video and sharing a voice reference are separate choices. Local synthesis does not make the Codex conversation or connected services institutionally private.

Run the checks relevant to changes. Inspect actual rendered frames, selected audio hashes, transcript discrepancies, captions and export streams. State which hardware paths were exercised and which remain untested. Do not claim to hear subtle voice quality without a listening capability. Do not publish, invite collaborators or change repository visibility without user instruction.
