# Software and model terms

This private starter supplies reusable orchestration code and documentation. It does not redistribute VoiceStudio, model weights, another person's voice or course material. Recipients may adapt the starter for their own academic productions; third-party components and contributed materials retain their own terms. The package's `private`/`UNLICENSED` settings prevent accidental npm publication and do not relicense dependencies.

Checked against upstream sources on **12 November 2026**. Recheck before a new institutional/commercial deployment. Software licensing, model licensing and ownership of supplied material are separate questions.

| Component | Source and terms to check |
| --- | --- |
| VoiceStudio desktop app (optional) | [Upstream repository and licence](https://github.com/debpalash/VoiceStudio), AGPL-3.0 application; no application source/binaries copied into this template. Follow its installed version's notices. |
| OmniVoice 0.2.1 Python code | [Upstream](https://github.com/k2-fsa/OmniVoice), Apache-2.0 code. The code licence is not the weights licence. |
| OmniVoice model weights | [Model card](https://huggingface.co/k2-fsa/OmniVoice) states **CC-BY-NC**. Do not assume all university, fee-funded or commercial activity qualifies as non-commercial. Check intended use and attribution with the institution/model licensor; choose a suitably licensed engine if needed. |
| Audio tokenizer and other downloaded models | Retain the model cards/licences in the pinned download. OmniVoice's tokenizer dependencies have their own terms. Don't infer permission from the Python package licence. |
| Remotion | [License FAQ](https://www.remotion.dev/docs/license/faq) and [terms](https://www.remotion.dev/docs/license). The current FAQ includes individuals/free categories but specifically says **educational institutions need written permission** to use the Free License. Do not assume an institution automatically qualifies because it is nonprofit. No licence purchase is automated. |
| AudioSeal | [Upstream](https://github.com/facebookresearch/audioseal), MIT according to upstream; generated narration is watermarked and identified as synthetic in manifests. |
| React | [Upstream](https://github.com/facebook/react), MIT. |
| PyTorch / torchaudio | [PyTorch](https://github.com/pytorch/pytorch), upstream notices and official platform wheels. |
| Transformers / Hugging Face Hub | [Transformers](https://github.com/huggingface/transformers), Apache-2.0; downloaded model terms are separate. |
| faster-whisper | [SYSTRAN](https://github.com/SYSTRAN/faster-whisper), MIT code; downloaded Whisper model provenance retained. |
| Parselmouth / Praat | [Parselmouth](https://github.com/YannickJadoul/Parselmouth), GPL-3.0 acoustic-analysis tooling. |
| FFmpeg / imageio-ffmpeg | [FFmpeg legal](https://ffmpeg.org/legal.html); actual binary build terms apply. Used through Remotion or imageio-ffmpeg. |
| Node / uv | [Node](https://nodejs.org/) and [uv](https://github.com/astral-sh/uv), official checksum-verified downloads with their upstream notices. |

Fonts and the effect are documented in [ASSET-CREDITS.md](ASSET-CREDITS.md). For real teaching/research videos, keep separate rights records for papers, lecture notes, photographs, diagrams, music and speaker consent. No paid service or public publication is enabled by default.
