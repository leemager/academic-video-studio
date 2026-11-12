---
name: academic-voiceover
description: Register an academic's own voice and generate or refine local cloned narration in this studio, with prosody planning, transcript checks, immutable takes and browser auditions. Use for voice setup and narration revisions.
---

No voice is bundled. Use the speaker's original human recording and accurate matching transcript, following [voice setup](../../../docs/VOICE.md). An explicit request to clone their own voice supplies the necessary direction; ask only for missing inputs. Do not borrow another person's profile or use generated speech as the reference. Inspect the selected profile, both reference hashes and the speaker's saved preferences. Initial defaults are a starting point, not human approval.

On a new machine follow [runtime setup](../../../docs/SETUP.md), then benchmark one short passage. The original recording is small; generation still requires model inference. Report measured performance and whether CUDA, MPS or CPU actually worked. No unrequested remote/paid fallback. VoiceStudio integration is documented [here](../../../docs/VOICESTUDIO.md); the repository renderer uses public OmniVoice independently.

Before synthesis read [prosody guidance](references/prosody.md). Decide what the sentence means, which words carry contrast, which endings should remain neutral and which names need pronunciation preparation. `prosody` metadata documents intent; it is not an expressive control channel. The renderer speaks `tts_text` if supplied, otherwise `text`. Keep the approved academic text in `text` for captions and QA. Use only controls supported by the pinned engine; don't invent SSML.

Generate complete coherent passages with natural breaths. Never impose uniform sentence pauses, cut on ASR timestamps or splice inside a word or breath. If the passage sounds wrong, create one or two complete alternatives with meaningfully different phrasing/control or seed. Change wording only with academic approval when meaning or exact text matters. Preserve unaffected approved passages.

Run independent transcription and inspect discrepancies; names, numbers and punctuation can produce benign differences. Use [acoustic triage](references/acoustic-triage.md) for targeted focus/contour concerns. Acoustic measurements cannot infer intended meaning or guarantee accent/naturalness; they never override the speaker's approved take.

Use the [audition and assembly workflow](../../../docs/PRODUCTION.md) for alternatives. Each take gets a new folder and content-hash filename. Apply the selected WAV itself, not a regeneration with its seed. Rebuild timing/captions and confirm that the actual composition references the selected audio hash. Never restore an old whole master to undo a local edit.

Record confirmed pronunciation/prosody preferences in the ignored voice folder, with accepted/rejected hashes and context. Don't universalise one sentence into a dialect rule. After two unsuccessful focused rounds, offer a small approved rewrite or an imported human recording instead of endless auditions.

For translated narration set `language` per passage explicitly, keep the original human reference and use multilingual ASR. The default setup installs multilingual Whisper small. Validate translation separately; ASR does not certify native pronunciation. Add the necessary font coverage and check acronyms, names and display text. Do not claim fluency from a transcript match.
