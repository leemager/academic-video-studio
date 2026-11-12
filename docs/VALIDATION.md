# Validation record

This template is being verified on Windows x64. Platform-routing tests cover Windows/Linux x64, Apple Silicon, Intel Mac and unsupported ARM cases. Those tests do not constitute running synthesis or the installers on another operating system.

Run `npm run lint` and `npm run test:template` after relevant code changes. The latter uses the configured voice Python and tests reference registration, source preservation, imported-audio manifests, immutable selected waveforms, archive boundaries, documentation links and platform routing. Audio tests use generated tones, never personal voice data. They don't test subjective voice quality.

The neutral demo can be rendered without a voice reference or model download. On a recipient's actual machine, setup is complete only after the preview loads and a short registered-voice benchmark succeeds (or an explicit imported-audio route is chosen).

## Packaging checks — 12 November 2026

- Windows PowerShell entry point exercised for preview-only and audio-only setup: verified portable downloads, managed Python, local Node, dependency installation, browser installation and first-run doctor passed.
- Eight automated checks passed, including reference/transcript hashes, original-file preservation, immutable selections, rejection of changed resume profiles and profile-free imported-audio transcription dispatch.
- The audition protocol test passed creation, audio hash verification, range requests, no-cache headers, rejection of unauthorised selection requests and exact selection recording. Fixtures were artificial signals; no personal voice is packaged.
- TypeScript/ESLint, Python compilation, JavaScript syntax and all three skill validators passed. Node dependency audit reported zero vulnerabilities after the documented overrides.
- Representative rendered frames were visually inspected. A 600-frame neutral demo exported successfully: 1920×1080, 30 fps H.264, 48 kHz stereo AAC, approximately 20 seconds. Its only sound is a brief quiet transition effect.
- Git-index sharing checks passed with no personal voice, lecture, institution-specific assets, local runtime, notes, generated project or machine-specific paths staged.

The local Windows sandbox allowed still rendering but its video encoder failed with EPIPE; the same render succeeded when local browser/encoder execution was permitted outside that sandbox. If this occurs, inspect the actual process error and use the normal authorised execution route; do not weaken security controls.

No macOS or Linux machine was available for execution. Their installation routes were source-reviewed and platform planning was tested; actual hardware performance remains a first-run check. No new person's voice is bundled or claimed to have been perceptually verified. The narration adapter retains the previously exercised OmniVoice generation path, with new registration/provenance/retake checks. A recipient must still register and listen to their own short benchmark.
