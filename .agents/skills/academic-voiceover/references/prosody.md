# Meaning before synthesis

A quoted prompt is usually an example, not direct address. An ordinary final pronoun need not carry strong stress. In a contrast such as “consumer plan” versus “institutional plan”, the distinguishing adjective may carry the focus while “plan” stays light. New information, genuine contrast and definitions may deserve emphasis; terminal position alone does not.

Optional editorial metadata:

```json
{"prosody":{"function":"explain a contrast","focus_words":["consumer"],"unstressed_words":["plan"],"ending":"neutral_fall","preserve_natural_breaths":true}}
```

This metadata does not drive OmniVoice. Start with natural text, full context and correct punctuation. A rogue comma can create a continuing contour instead of a complete sentence. Capitalisation and phonetic respelling can change vowels or accent as well as emphasis. Prefer supported pronunciation controls only after checking the pinned engine's documentation. Keep hints in `tts_text`, not captions, and review pronunciation and emphasis separately.

Use the original human reference throughout. A synthetic favourite is not a replacement identity reference. Seeds are useful records but do not guarantee the same waveform on different software or hardware; store approved audio and its hash.

Default OmniVoice postprocessing can trim quiet edges and shorten silences. If a breath or phoneme sounds clipped, compare a new whole-passage take with `postprocess_output: false` in a versioned profile. Preserve the failed and approved takes. Raw output may have noisy or long edges; assess it before choosing. Never blanket-replace a whole approved narration to test one problematic passage.

Uniform inserted pauses and ASR-based cutting have caused mid-breath jumps and boundaries inside words. Keep generated passages intact. If the speaker wants slower delivery, test a modestly lower generation speed on a new complete passage. Only add an inter-passage gap when the actual boundary needs it.

For retakes, choose a complete short unit containing enough context. Prefer one or two purposeful candidates over many random seeds. Keep pronunciation preferences speaker-specific; do not assume a British/American vowel, glottal stop or speech rhythm from another person's feedback.
