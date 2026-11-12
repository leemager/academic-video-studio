---
name: academic-voiceover
description: Register an academic's own voice and generate or refine local cloned narration in this studio, with prosody planning, transcript checks, immutable takes and browser auditions. Use for voice setup and narration revisions.
---

Ask for the speaker's original recording only. Use the local transcription command in [voice setup](../../../docs/VOICE.md) to produce its transcript, show the words for a quick check and resolve unclear names or phrases. Codex handles transcription setup; do not require the speaker to type a transcript. Then register the recording and checked text. The starter example contains finished narration; register a new voice from the academic's recording. Inspect the selected profile, both reference hashes and the speaker's saved preferences.

On a new machine follow [runtime setup](../../../docs/SETUP.md), then benchmark one short passage. Report measured performance and the working device: CUDA, MPS or CPU. VoiceStudio integration is documented [here](../../../docs/VOICESTUDIO.md); the repository renderer uses OmniVoice independently. Ask before using a paid or remote service.

Before synthesis read [prosody guidance](references/prosody.md). Decide what the sentence means, which words carry contrast, which endings should remain neutral and which names need pronunciation preparation. `prosody` metadata documents intent; it is not an expressive control channel. The renderer speaks `tts_text` if supplied, otherwise `text`. Keep the approved academic text in `text` for captions and QA. Use only controls supported by the pinned engine; don't invent SSML.

Generate complete coherent passages with natural breaths. Never impose uniform sentence pauses, cut on ASR timestamps or splice inside a word or breath. If the passage sounds wrong, create one or two complete alternatives with meaningfully different phrasing/control or seed. Change wording only with academic approval when meaning or exact text matters. Preserve unaffected approved passages.

Run independent transcription and inspect discrepancies; names, numbers and punctuation can produce benign differences. Use [acoustic triage](references/acoustic-triage.md) to shortlist passages with unexpected emphasis or pitch contours. Keep the speaker's chosen take when a measurement disagrees with it.

Use the [audition and assembly workflow](../../../docs/PRODUCTION.md) for alternatives. Each take gets a new folder and content-hash filename. Apply the selected WAV itself, not a regeneration with its seed. Rebuild timing/captions and confirm that the actual composition references the selected audio hash. Never restore an old whole master to undo a local edit.

Record confirmed pronunciation/prosody preferences in the ignored voice folder, with accepted/rejected hashes and context. Keep preferences specific to the speaker and sentence. After two unsuccessful focused rounds, offer a small rewrite or an imported human recording.

For translated narration set `language` per passage explicitly, keep the original human reference and use multilingual ASR. The default setup installs multilingual Whisper small. Check translation and pronunciation with a fluent reviewer, and include the necessary font coverage for names and display text.
