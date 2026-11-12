# First setup — Codex carries this out

Read AGENTS.md and inspect the real operating system, CPU architecture, RAM, free disk, GPU and existing installations. Prefer repository-local tools; never reinstall or remove someone else's environment to force setup. Use native ARM shells on Apple Silicon, not Rosetta. Check the intended use against [third-party terms](../THIRD-PARTY-NOTICES.md).

## Entry points

Run from this repository root. Git is only needed to clone/push; a downloaded and extracted ZIP also works for production.

| OS | Entry point | Notes |
| --- | --- | --- |
| Windows 10/11 x64 | `powershell -File tools/setup-windows.ps1` | Downloads a verified portable uv and managed Python; no preinstalled Python needed. Respect managed execution policy; don't disable security controls. |
| macOS | `/bin/bash tools/setup-mac.sh` | Uses curl/tar/shasum. Relaunches natively on Apple Silicon if needed. No Homebrew required. |
| Linux x64 (glibc distribution) | `/bin/bash tools/setup-linux.sh` | Requires curl, tar, sha256sum and desktop/browser system libraries. No automatic sudo. |
| Any supported OS with Python 3.9+ already installed | `python tools/bootstrap.py --dry-run`, then `python tools/bootstrap.py` | On Unix the command may be `python3`. Dry-run does not download anything. |

Shell entry points must install their small Python launcher before they can forward `--dry-run`/`-DryRun`. Use the direct Python dry-run for a strictly download-free plan.

For video-only setup, add `-PreviewOnly` on Windows or `--preview-only` on macOS/Linux. For imported narration without model downloads, use `-AudioOnly` / `--audio-only`; this creates `.venv-audio` and wires it into the local config. Intel Macs automatically take this lightweight audio route unless preview-only is selected. Windows/Linux ARM skip the pinned voice stack. Browser/render support must still be checked on the actual architecture; this is not a claim that every ARM platform is supported by Chrome Headless Shell.

Setup downloads checksum-verified Node 24.15.0 and uv 0.8.22, managed Python 3.11, pinned package dependencies, Remotion's browser and public model snapshots. Public model downloads do not upload your recording. Expect several GB; reserve 15 GB or more for the scripted stack and extra space for the desktop app/renders. Models are downloaded only on a voice-supported path.

## GPU and CPU selection

The installer detects a working `nvidia-smi` on Windows/Linux x64 and installs PyTorch 2.8.0 with CUDA 12.8 wheels from PyTorch's official index. Otherwise it installs CPU wheels. Use `-TorchBackend cpu` on Windows or `--torch-backend cpu` with Python/Linux for an explicit CPU setup; `cuda` is also available. Drivers remain the machine owner's responsibility. Inspect `torch.cuda.is_available()` after installation; do not claim CUDA from the package name alone.

On Apple Silicon, use native PyTorch MPS, float32 and eager attention. On MPS failure, preserve the failed take and benchmark `--device cpu` in a new folder. CPU inference may be slow. On an Intel Mac this pinned voice stack cannot be installed; use imported human narration or narration generated on another explicitly authorised machine. The template does not silently upload to a remote GPU.

AMD/Intel accelerators and ROCm are not configured by this lightweight bootstrap. Windows/Linux x64 CPU is the baseline. VoiceStudio has other engines and hardware routes; use its current platform guide and benchmark separately if a user needs them. Do not pretend the direct renderer supports every VoiceStudio engine.

## Run the installed tools

Setup writes ignored `.runtime/local.json` with absolute paths. If Node/npm are not already on PATH, Codex should use the recorded `node` executable:

```text
<local-node> tools/run.mjs run doctor
<local-node> tools/run.mjs run dev
<local-node> tools/run.mjs run register-voice -- --audio notes/voice-input/original.wav --transcript notes/voice-input/transcript.txt --name "Your name"
```

With ordinary Node/npm available, use `npm run doctor`, `npm run dev`, etc. `npm run python -- <script> ...` calls the configured voice interpreter. No global PATH edits are necessary.

Open the exact Studio URL printed by the process, normally `http://localhost:3020/StarterDemo`. The neutral example has no narration and one quiet transition effect. Verify it actually loads. On Linux, missing browser shared libraries require the distribution's supported package route; report the exact dependencies and obtain any necessary administrator help instead of issuing broad system changes.

Then follow [VOICE.md](VOICE.md) to register the academic's original reference and benchmark one short passage. A first-run doctor reporting “No voice registered” is expected. If the user wants the desktop app, follow [VOICESTUDIO.md](VOICESTUDIO.md).

## Recovery and reproducibility

Setup preserves environments and backs up its runtime config. It uses `npm install` rather than `npm ci` in an existing working folder because `npm ci` deletes node_modules. Failed archives and takes stay available for diagnosis. Never remove a shared cache or bypass a deletion hook. For a clean experiment, use a new bounded folder.

The Node lockfile pins the front-end stack. Python direct dependencies and the Apple Silicon resolved environment are pinned; transitive Windows/Linux dependencies may still evolve. All model snapshots are explicit in `tools/voice/download-models.py`. The default ASR is multilingual Whisper small. Runtime flags can improve compatibility but only a real generation verifies the local machine.

Keep Remotion package versions aligned. This compatible baseline overrides Zod to 4.6.6 for an earlier audit fix; Remotion may print a version warning. This project uses no Zod composition schemas. Minimatch is overridden to 11.0.1 for the current glob-amplification advisory in lint dependencies. Validate lint and an actual render before changing versions. See [VALIDATION.md](VALIDATION.md) for the tested scope rather than treating cross-platform instructions as cross-platform execution evidence.
