# Acoustic checks are triage

`tools/voice/prosody_preflight.py` uses Praat/Parselmouth to inspect F0 and voiced RMS, compare annotated focus pairs and flag some terminal contours. Run `npm run python -- tools/voice/prosody_preflight.py --help` for the JSON format and arguments. It reports uncertainty and never changes audio.

Specify intended focus from meaning first. Pitch alone is not emphasis: intensity, duration, spectral shape, lexical stress and phrase-final lengthening all contribute. Raw durations of different words are not directly comparable. Missing voicing, octave errors, repeated words or unstable alignment mean uncertainty. Small timestamp shifts can change a result, so inspect boundary sensitivity.

Use acoustic flags to shortlist a few passages for listening, not to approve or reject the whole voice. A human-approved waveform remains authoritative even if a score flags it. ASR can identify omitted/repeated words but cannot reliably prove a particular vowel or consonant realisation.

[Wavelet Prosody Toolkit](https://github.com/asuni/wavelet_prosody_toolkit) combines pitch, energy and duration; [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/) can improve phone/word alignment. Neither is installed by this starter. Add complexity only after testing a small speaker-labelled set of accepted/rejected examples. Alignment to an expected pronunciation does not prove that pronunciation occurred.
