"""Checks preservation, first-run setup planning and the neutral template; no GPU/model download."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
import zipfile

ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


class TemplateChecks(unittest.TestCase):
    def test_reference_transcription_preserves_recording_and_existing_text(self):
        transcriber=load('reference_transcriber',ROOT/'tools/voice/transcribe_reference.py')
        folder=ROOT/'.work';folder.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='owned-transcription-test-',dir=folder) as tmp:
            temp=Path(tmp);transcriber.ROOT=temp
            audio=temp/'recording.mp3';audio.write_bytes(b'original recording fixture')
            before=sha(audio);output=temp/'transcript.txt'
            model_dir=temp/'model';model_dir.mkdir();(model_dir/'model.bin').write_bytes(b'fixture')
            word=SimpleNamespace(word=' Bonjour.',start=0.0,end=1.0,probability=.92)
            segment=SimpleNamespace(start=0.0,end=1.0,text=' Bonjour.',words=[word])
            asr=Mock(return_value=(iter([segment]),SimpleNamespace(language='fr',language_probability=.99)))
            model=SimpleNamespace(model=SimpleNamespace(is_multilingual=True),transcribe=asr)
            factory=Mock(return_value=model)
            with patch.dict(sys.modules,{'faster_whisper':SimpleNamespace(WhisperModel=factory)}):
                result=transcriber.transcribe_reference(audio,output,model_dir=model_dir)
                self.assertEqual(result['text'],'Bonjour.')
                self.assertEqual(output.read_text(encoding='utf-8'),'Bonjour.\n')
                self.assertEqual(read(output.with_suffix('.asr.json'))['audio_sha256'],before)
                self.assertEqual(asr.call_args.kwargs['task'],'transcribe')
                self.assertIsNone(asr.call_args.kwargs['language'])
                self.assertTrue(factory.call_args.kwargs['local_files_only'])
                with self.assertRaises(FileExistsError):
                    transcriber.transcribe_reference(audio,output,model_dir=model_dir)
                self.assertEqual(factory.call_count,1)
                self.assertEqual(output.read_text(encoding='utf-8'),'Bonjour.\n')
                self.assertEqual(sha(audio),before)

    def test_resume_rejects_changed_profile(self):
        renderer=load('renderer',ROOT/'tools/voice/render.py')
        folder=ROOT/'.work';folder.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='owned-resume-test-',dir=folder) as tmp:
            t=Path(tmp);script=[{'id':'one','text':'Reviewed.'}];context={'profile_sha256':'original'}
            (t/'script.json').write_text(json.dumps(script),encoding='utf-8')
            (t/'run-context.json').write_text(json.dumps(context),encoding='utf-8')
            renderer.verify_resume(t,script,context)
            with self.assertRaisesRegex(RuntimeError,'profile/runtime'):
                renderer.verify_resume(t,script,{'profile_sha256':'changed'})

    def test_imported_asr_branch_needs_no_clone_profile(self):
        renderer=load('renderer',ROOT/'tools/voice/render.py')
        folder=ROOT/'.work';folder.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='owned-asr-test-',dir=folder) as tmp:
            t=Path(tmp);(t/'narration.wav').write_bytes(b'fixture')
            (t/'manifest.json').write_text(json.dumps({'narration_sha256':sha(t/'narration.wav')}),encoding='utf-8')
            with patch.object(sys,'argv',['render.py','--transcribe-only','--output',str(t)]),patch.object(renderer,'runtime',return_value={}),patch.object(renderer,'setup_imports'),patch.object(renderer,'transcribe') as asr:
                renderer.main();asr.assert_called_once()

    def test_platform_routes(self):
        b=load('bootstrap',ROOT/'tools/bootstrap.py')
        for system,machine in [('Windows','AMD64'),('Linux','x86_64'),('Darwin','arm64')]:
            self.assertTrue(b.platform_plan(system,machine)['voice_install'])
        for system,machine in [('Darwin','x86_64'),('Windows','ARM64'),('Linux','aarch64')]:
            self.assertFalse(b.platform_plan(system,machine)['voice_install'])
        self.assertEqual(b.platform_plan('Windows','AMD64',nvidia=True)['torch_backend'],'cuda')
        self.assertEqual(b.platform_plan('Windows','AMD64')['torch_backend'],'cpu')
        self.assertEqual(b.platform_plan('Darwin','arm64')['torch_backend'],'mps')
        self.assertFalse(b.platform_plan('Windows','AMD64',preview_only=True)['voice_install'])
        with self.assertRaises(ValueError):b.platform_plan('Linux','i686')
        with self.assertRaises(ValueError):b.platform_plan('Darwin','arm64',backend='cuda')

    def test_document_links(self):
        paths=[ROOT/'README.md',ROOT/'AGENTS.md',*list((ROOT/'docs').glob('*.md')),*list((ROOT/'.agents').rglob('*.md'))]
        for p in paths:
            for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
                if '://' in link or link.startswith('#'):continue
                self.assertTrue((p.parent/link.split('#')[0]).exists(),f'{p}: {link}')

    def test_demo_audio_and_timing(self):
        d=read(ROOT/'src/data/starter-demo.json')
        release=read(ROOT/'projects/starter-demo/narration-release.json')
        self.assertEqual(sha(ROOT/'public'/d['audio']),release['sha256'])
        self.assertEqual(d['audioHash'],release['sha256'])
        self.assertLessEqual(d['audioFromFrames']/d['fps']+release['duration_seconds'],d['durationInFrames']/d['fps'])
        self.assertEqual(d['scenes'][0]['from'],d['leadFrames'])
        for a,b in zip(d['scenes'],d['scenes'][1:]):self.assertEqual(a['from']+a['durationInFrames'],b['from'])
        self.assertLessEqual(d['scenes'][-1]['from']+d['scenes'][-1]['durationInFrames'],d['durationInFrames'])
        self.assertTrue(all(p.name=='README.txt' for p in (ROOT/'voices').iterdir() if not p.is_dir()))

    def test_archive_escape_rejected(self):
        b=load('bootstrap',ROOT/'tools/bootstrap.py')
        folder=ROOT/'.work';folder.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='owned-archive-test-',dir=folder) as tmp:
            archive=Path(tmp)/'bad.zip'
            with zipfile.ZipFile(archive,'w') as z:z.writestr('../escaped.txt','bad')
            with self.assertRaises(ValueError):b.safe_unpack(archive,Path(tmp)/'output')
            self.assertFalse((Path(tmp)/'escaped.txt').exists())

    def test_voice_registration_and_import_preserve_inputs(self):
        import numpy as np
        import soundfile as sf
        register=load('register',ROOT/'tools/register-voice.py')
        folder=ROOT/'.work';folder.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='owned-voice-test-',dir=folder) as tmp:
            temp=Path(tmp);(temp/'voices').mkdir();original=temp/'input.wav';transcript=temp/'input.txt'
            sf.write(original,np.sin(np.arange(96000)*.03)*.1,24000,subtype='PCM_16')
            transcript.write_text('A synthetic test signal, never a real voice.',encoding='utf-8')
            before=sha(original);register.ROOT=temp
            result=register.register(original,transcript,'Automated test fixture')
            profile=read(Path(result['profile']))
            self.assertEqual(profile['reference_sha256'],sha(temp/'voices/local/reference.wav'))
            self.assertEqual(profile['reference_text_sha256'],sha(temp/'voices/local/reference.txt'))
            self.assertEqual(before,sha(original))
            with self.assertRaises(FileExistsError):register.register(original,transcript,'Automated test fixture')
            script=temp/'script.json';spec=temp/'files.json'
            script.write_text(json.dumps([{'id':'one','text':'A complete test passage.'}]),encoding='utf-8')
            spec.write_text(json.dumps([{'id':'one','file':str(original)}]),encoding='utf-8')
            output=temp/'imported'
            command=[sys.executable,str(ROOT/'tools/import-narration.py'),'--script',str(script),'--files',str(spec),'--output',str(output)]
            result=subprocess.run(command,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            manifest=read(output/'manifest.json')
            self.assertFalse(manifest['synthetic']);self.assertIsNone(manifest['reference_sha256'])
            self.assertEqual(manifest['scenes'][0]['original_sha256'],before)
            self.assertAlmostEqual(manifest['duration_seconds'],4.0,places=4)
            final=sha(output/'narration.wav')
            again=subprocess.run(command,capture_output=True,text=True)
            self.assertNotEqual(again.returncode,0);self.assertEqual(final,sha(output/'narration.wav'))

    def test_selected_waveform_is_exact_and_immutable(self):
        import numpy as np
        import soundfile as sf
        folder=ROOT/'.work';folder.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='owned-assembly-test-',dir=folder) as tmp:
            temp=Path(tmp);base=temp/'base';(base/'scenes').mkdir(parents=True)
            sf.write(base/'scenes/one.wav',np.sin(np.arange(24000)*.01)*.1,24000,subtype='PCM_16')
            replacement=temp/'alternative.wav';sf.write(replacement,np.cos(np.arange(12000)*.02)*.1,24000,subtype='PCM_16')
            (base/'manifest.json').write_text(json.dumps({'sample_rate':24000,'scenes':[{'id':'one','text':'Reviewed text.','file':'scenes/one.wav','sha256':sha(base/'scenes/one.wav'),'pause_after':0}]}),encoding='utf-8')
            s={'passageId':'one','text':'Reviewed text.','file':replacement.relative_to(ROOT).as_posix(),'sha256':sha(replacement)}
            chosen=temp/'choice.json';chosen.write_text(json.dumps(s),encoding='utf-8')
            output=temp/'assembled';command=[sys.executable,str(ROOT/'tools/voice/assemble.py'),'--base',str(base),'--output',str(output),'--selection',str(chosen)]
            result=subprocess.run(command,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(sha(output/'scenes/one.wav'),s['sha256'])
            before=sha(output/'narration.wav')
            again=subprocess.run(command,capture_output=True,text=True);self.assertNotEqual(again.returncode,0)
            self.assertEqual(before,sha(output/'narration.wav'))


if __name__=='__main__':unittest.main(verbosity=2)
