# Academic video studio

The academic directs the content; Codex handles setup, source organisation, narration, visuals, previews, retakes, captions and export. Ask about academic choices and missing inputs, not routine implementation details. Give plain-language updates and concrete review links.

Read `.agents/skills/academic-video-production/SKILL.md` for video work, `.agents/skills/academic-voiceover/SKILL.md` for narration, and `.agents/skills/remotion-studio/SKILL.md` for the edit. Setup is in `docs/SETUP.md`; voice registration is in `docs/VOICE.md`. Read these files directly if skill discovery is unavailable.

Inspect the OS, architecture, memory and GPU, then follow the relevant setup route. Benchmark one short passage before estimating production time. Intel Macs use the audio-import route. Use Remotion for editing and the included OmniVoice renderer for repeatable narration. VoiceStudio is an optional desktop interface. See THIRD-PARTY-NOTICES.md for usage terms. Work locally unless the user asks for a remote service or publication.

Each user supplies their own original recording. Codex transcribes it locally with `npm run transcribe-reference`, shows the resulting words for a quick check and resolves unclear names or phrases before registration. Do not ask the user to write a transcript. Follow `docs/VOICE.md`; the default profile is `voices/local/profile.json`. The example's generated narration is for playback, not cloning. Preserve reference hashes and the speaker's pronunciation preferences.

For an outline request, draft the outline first, grounded in the supplied materials. Map substantive claims to source pages or sections and flag gaps. Review the script with the academic before long narration unless they have already approved the text or asked you to proceed. Keep source wording separate from pronunciation cues. Identify facts that may need updating in future editions.

Plan emphasis from meaning before synthesis. Generate coherent passages with natural breaths. Use whole-passage retakes, not cuts at ASR timestamps or uniform sentence pauses. Present alternatives in the audition UI when needed and apply the exact selected audio. Preserve all other approved passages.

Use readable typography, purposeful imagery and diagrams, restrained transitions and occasional quiet effects. Avoid repeated corner labels, decorative micro-text and redundant taglines. Music is off by default. Keep narration continuous across visual cuts and record asset credits.

Preserve source documents, references, selected audio and previous renders. Create new take folders and versioned exports; delete pre-existing files only when requested. Personal notes, voices and working projects are ignored by Git. Keep them in a separate backup. Before sharing template code, run `npm run check-share`; the tracked registry must import only included projects.

Run checks relevant to the change: `npm run lint`, `npm run test:template`, rendered frames, transcript differences, caption spelling, selected audio hashes and export streams. Open the preview for the academic to review, then deliver the requested video and subtitles.
