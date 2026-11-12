# Setup instructions for Codex

Inspect the OS, architecture, RAM, free disk, GPU and existing installations. Install tools inside this project and use a native ARM shell on Apple Silicon. Allow at least 15 GB free, plus space for source material and renders.

## Entry points

Run from the repository root. An extracted ZIP works as well as a Git checkout.

| OS | Command | Prerequisites |
| --- | --- | --- |
| Windows 10/11 x64 | `powershell -File tools/setup-windows.ps1` | No preinstalled Python needed. For managed execution-policy restrictions, use an existing Python or the institution's installation route. |
| macOS | `/bin/bash tools/setup-mac.sh` | curl, tar and shasum; no Homebrew needed. |
| Linux x64, glibc distribution | `/bin/bash tools/setup-linux.sh` | curl, tar, sha256sum and browser system libraries. |
| Python 3.9+ already installed | `python tools/bootstrap.py` | Use `python3` where appropriate. Add `--dry-run` to inspect the plan without downloading. |

Shell entry points install a small Python launcher before forwarding dry-run options. Use the direct Python command for a download-free plan.

Setup downloads verified Node and uv releases, Python 3.11, pinned packages, Remotion's browser and public model weights. Paths are saved in `.runtime/local.json`.

## Choose the setup mode

- **Full studio:** the default on Windows/Linux x64 and Apple Silicon.
- **Preview and rendering:** `-PreviewOnly` on Windows or `--preview-only` on macOS/Linux.
- **Imported narration:** `-AudioOnly` / `--audio-only` installs lightweight audio tools without TTS models. Intel Macs use this route automatically.

Windows/Linux ARM skip the pinned voice stack; check browser and engine compatibility for the specific machine.

## GPU and CPU

On Windows/Linux x64, a working `nvidia-smi` selects PyTorch 2.8.0 CUDA 12.8 wheels. Otherwise setup uses CPU wheels. Choose explicitly with `-TorchBackend cpu` or `-TorchBackend cuda` on Windows, or `--torch-backend cpu|cuda` with the Python/Linux entry point. Check the NVIDIA driver and `torch.cuda.is_available()` if acceleration is unavailable.

Apple Silicon uses MPS with float32 and eager attention. If it fails, retain the take and test `--device cpu` in a new folder. Intel Macs can preview/render and import audio, but cannot run this pinned cloning stack locally. Other accelerators, including ROCm, need a separately configured engine; the default Windows/Linux fallback is CPU.

## Run the tools

If Node/npm are already available, use `npm run doctor` and `npm run dev`. Otherwise use the absolute Node path recorded in `.runtime/local.json`:

```text
<local-node> tools/run.mjs run doctor
<local-node> tools/run.mjs run dev
```

`npm run python -- <script> ...` runs a helper with the configured audio/voice interpreter. No global PATH change is needed.

Open the exact Studio URL printed by the process, normally `http://localhost:3020/StarterDemo`, and check that the example plays. On Linux, install any identified missing browser libraries through the distribution's supported package route.

Follow [VOICE.md](VOICE.md) to register the user's recording and generate a short sample. Measure the time before estimating a longer video. “No voice registered” is expected before this step. For the desktop interface, see [VOICESTUDIO.md](VOICESTUDIO.md).

## Maintenance

Setup preserves existing environments and backs up runtime configuration. It uses `npm install`; use `npm ci` only in a disposable clean checkout because it removes node_modules. For an isolated experiment, use a new folder.

Keep Remotion packages on matching versions. Zod 4.6.6 and Minimatch 11.0.1 are security overrides in package.json. Remotion may print a Zod version warning; this project does not use Zod composition schemas. Run lint, tests and a sample render before changing these dependencies. Model snapshots are pinned in `tools/voice/download-models.py`.
