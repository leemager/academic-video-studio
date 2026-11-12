# Troubleshooting

Ask Codex to inspect the precise error, preserve the failed output and solve it. Avoid starting over by deleting environments or approved media.

| Symptom | Next useful action |
| --- | --- |
| GitHub says 404/access denied | This is a private repo. Confirm the correct signed-in GitHub account and that the owner invited it. Don't paste a token into chat. |
| Python/Node/npm not found | Use the OS entry point, then the absolute executables in `.runtime/local.json` through `tools/run.mjs`. |
| Windows refuses a script/installer | Respect institutional execution policy; use the direct Python entry point if already available or ask IT for the supported route. Don't disable protection. |
| Studio starts but is blank | Open the exact printed URL/composition; inspect compile errors, missing assets and font load errors. Render one still. |
| Linux browser fails to launch | Inspect missing shared libraries and distro compatibility. Install only identified dependencies through an authorised system-package route. |
| Encoder fails with EPIPE inside a sandbox | Inspect the encoder/process error. The same command may need the app's normal approval for local browser/encoder execution. Don't disable protection or alter the deletion hook. |
| No voice registered | Expected in a clean template. Register an original recording and transcript; there is no bundled voice. |
| Reference hash changed | Preserve files and register a new profile after reviewing the intended change. Don't rewrite a stored hash to hide an accidental change. |
| CUDA unavailable | Inspect installed wheels, driver and actual `torch.cuda.is_available()`. Benchmark CPU or fix the supported driver/wheel pairing. |
| MPS fails or runs out of memory | Keep the take; try one shorter passage with `--device cpu` in a new folder. Don't promise a long video before measuring. |
| Intel Mac cannot install voice dependencies | Use preview/render plus imported narration; local current PyTorch-based cloning is unsupported. |
| Voice speaks the wrong words | Read independent ASR differences. Fix the complete passage with context; don't cut at word timestamps. |
| Stress or accent feels wrong | Explain the intended contrast and speaker preference; generate one or two complete alternatives and present the audition UI. |
| Breaths/word ends sound chopped | Check whether model postprocessing is responsible. Try a new versioned profile with output postprocessing disabled, preserving all approved audio. Avoid artificial sentence pauses. |
| Preview still plays an old take | Read the UI selection record, assembled manifest and compiled `audioHash`; confirm the preview points at the new hash-named WAV. Refresh only after checking the wiring. |
| An audition page is missing | Re-run `npm run auditions -- <actual-slug>`; use the printed port. Alternatives live only on that computer. |
| Transcript differs on a number/name | Compare the actual sentence and context. ASR formatting is not necessarily a synthesis error. |
| Long video takes too long | Measure short synthesis and render performance separately. Shorten the draft or use an explicitly agreed other machine; no silent remote upload. |

Approved waves, reference identity, source text and selection history are recovery assets. Git intentionally excludes personal work, so keep a separate authorised backup.
