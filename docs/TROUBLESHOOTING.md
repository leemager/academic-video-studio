# Troubleshooting

Ask Codex to inspect the precise error, preserve the failed output and solve it. Avoid starting over by deleting environments or approved media.

| Symptom | Next useful action |
| --- | --- |
| GitHub says 404/access denied | Check the repository URL, network connection and signed-in account. |
| Python/Node/npm not found | Use the OS entry point, then the absolute executables in `.runtime/local.json` through `tools/run.mjs`. |
| Windows refuses a script/installer | Use the direct Python entry point if already available, or ask IT for the supported installation route. |
| Studio starts but is blank | Open the exact printed URL/composition; inspect compile errors, missing assets and font load errors. Render one still. |
| Linux browser fails to launch | Inspect missing shared libraries and distro compatibility. Install only identified dependencies through an authorised system-package route. |
| Encoder fails with EPIPE inside a sandbox | Inspect the encoder/process error. The command may need the app's approval for local browser/encoder execution. |
| No voice registered | Give Codex the original recording. It transcribes it and registers the voice using the voice setup guide. |
| Reference hash changed | Check which reference changed. Preserve the original and register a new profile for an intentional replacement. |
| CUDA unavailable | Inspect installed wheels, driver and actual `torch.cuda.is_available()`. Benchmark CPU or fix the supported driver/wheel pairing. |
| MPS fails or runs out of memory | Keep the take; benchmark one shorter passage with `--device cpu` in a new folder. |
| Intel Mac cannot install voice dependencies | Use preview/render plus imported narration; local current PyTorch-based cloning is unsupported. |
| Voice speaks the wrong words | Read independent ASR differences. Fix the complete passage with context; don't cut at word timestamps. |
| Stress or accent feels wrong | Explain the intended contrast and speaker preference; generate one or two complete alternatives and present the audition UI. |
| Breaths/word ends sound chopped | Check whether model postprocessing is responsible. Try a new versioned profile with output postprocessing disabled, preserving all approved audio. Avoid artificial sentence pauses. |
| Preview still plays an old take | Read the UI selection record, assembled manifest and compiled `audioHash`; confirm the preview points at the new hash-named WAV. Refresh only after checking the wiring. |
| An audition page is missing | Re-run `npm run auditions -- <actual-slug>`; use the printed port. Alternatives live only on that computer. |
| Transcript differs on a number/name | Compare the actual sentence and context. ASR formatting is not necessarily a synthesis error. |
| Long video takes too long | Measure short synthesis and render performance separately. Try a shorter draft or discuss using a faster computer. |

Keep a separate backup of your voice recordings, source materials and chosen narration. Personal work is excluded from Git uploads by default.
