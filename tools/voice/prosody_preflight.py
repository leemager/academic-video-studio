"""Compare acoustic cues with editorial focus; never certify or alter prosody.

Requires numpy, soundfile and praat-parselmouth. Sentences must be editorially
defined in segments JSON (or manifest scenes), not inferred from ASR punctuation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import numpy as np
import soundfile as sf


def normalise_word(text):
    return re.sub(r"[^\w']", '', text.casefold().replace('\u2019', "'"))


def resolve_selector(selector, words):
    """Resolve one caption token; repeated words need a 1-based occurrence."""
    if isinstance(selector, str):
        text, occurrence = selector, None
    elif isinstance(selector, dict):
        text, occurrence = selector.get('text', ''), selector.get('occurrence')
    else:
        return None, 'invalid_selector'
    key = normalise_word(text)
    matches = [i for i, word in enumerate(words) if normalise_word(word['text']) == key]
    if not key or not matches:
        return None, 'missing_word'
    if occurrence is None:
        return (matches[0], None) if len(matches) == 1 else (None, 'ambiguous_word')
    if type(occurrence) is not int or not 1 <= occurrence <= len(matches):
        return None, 'invalid_occurrence'
    return matches[occurrence - 1], None


def analyse(audio, rate, words, segments, floor=60, ceiling=350):
    import parselmouth
    sound = parselmouth.Sound(audio, sampling_frequency=rate)
    pitch = sound.to_pitch_ac(time_step=.01, pitch_floor=floor, pitch_ceiling=ceiling)
    times = pitch.xs()
    hz = pitch.selected_array['frequency']
    # Frame RMS used only to compare voiced material within this recording.
    rms = np.array([np.sqrt(np.mean(audio[max(0,int((t-.015)*rate)):min(len(audio),int((t+.015)*rate))]**2)+1e-12) for t in times])
    results = []

    def measure(a, b):
        mask = (times >= a) & (times <= b) & (hz > 0)
        h, r = hz[mask], rms[mask]
        if len(h) < 5:
            return None
        return {'median_hz':float(np.median(h)), 'p90_hz':float(np.percentile(h,90)),
                'db':float(20*np.log10(np.median(r)+1e-10)), 'voiced_frames':int(len(h)),
                'first_hz':float(np.median(h[:max(2,len(h)//3)])),
                'last_hz':float(np.median(h[-max(2,len(h)//3):])),
                'octave_jump':bool(np.any(np.abs(12*np.log2(h[1:]/h[:-1])) > 8))}

    def word_measure(word, shift=0):
        return measure(word['startMs']/1000 + shift, word['endMs']/1000 + shift)

    def word_profile(word):
        measured = word_measure(word)
        return {'text':word['text'].strip(), 'startMs':word['startMs'],
                'endMs':word['endMs'], 'duration_ms':word['endMs']-word['startMs'],
                'acoustics':measured}

    def compare_focus(intent, selected):
        focus = intent.get('focus_words', [])
        # Accept the singular spelling used in this project's earlier manifests.
        if not focus and intent.get('focus_word'):
            focus = [intent['focus_word']]
        unstressed = intent.get('unstressed_words', [])
        if not isinstance(focus, list) or not isinstance(unstressed, list):
            return [], ['invalid_focus_metadata']
        comparisons, notices = [], []
        for focused in focus:
            fi, error_f = resolve_selector(focused, selected)
            for unmarked in unstressed:
                ui, error_u = resolve_selector(unmarked, selected)
                item = {'focus':focused, 'unstressed':unmarked, 'flags':[]}
                if error_f or error_u:
                    item.update(status='alignment_uncertain',
                                selector_errors={'focus':error_f, 'unstressed':error_u})
                    item['flags'].append('focus_alignment_uncertain')
                elif fi == ui:
                    item.update(status='invalid_intent')
                    item['flags'].append('conflicting_focus_metadata')
                else:
                    probes = []
                    # A small boundary shift can assign another word's pitch to
                    # this one. Treat unstable results as timing uncertainty.
                    for shift in (-.06, 0, .06):
                        fm, um = word_measure(selected[fi], shift), word_measure(selected[ui], shift)
                        valid = bool(fm and um and not fm['octave_jump'] and not um['octave_jump'])
                        probe = {'alignment_shift_ms':round(shift*1000), 'usable_pitch':valid}
                        if valid:
                            pitch_diff = float(12*np.log2(um['median_hz']/fm['median_hz']))
                            level_diff = float(um['db']-fm['db'])
                            probe.update(unstressed_minus_focus_st=round(pitch_diff,3),
                                         unstressed_minus_focus_db=round(level_diff,3),
                                         competing_pitch_and_level=pitch_diff > 1.2 and level_diff > 2)
                        probes.append(probe)
                    item['probes'] = probes
                    if not all(p['usable_pitch'] for p in probes):
                        item.update(status='acoustic_evidence_uncertain')
                        item['flags'].append('focus_pitch_evidence_uncertain')
                    else:
                        candidates = [p['competing_pitch_and_level'] for p in probes]
                        pitch_span = np.ptp([p['unstressed_minus_focus_st'] for p in probes])
                        level_span = np.ptp([p['unstressed_minus_focus_db'] for p in probes])
                        if pitch_span > 2 or level_span > 3:
                            item.update(status='alignment_sensitive')
                            item['flags'].append('focus_alignment_sensitive')
                        elif all(candidates):
                            item.update(status='review_candidate')
                            item['flags'].append('possible_focus_mismatch')
                        elif any(candidates):
                            item.update(status='alignment_sensitive')
                            item['flags'].append('focus_alignment_sensitive')
                        else:
                            item.update(status='no_clear_pitch_level_conflict')
                    # Duration is reported, never used as a stress score across
                    # words of different phonetic/ syllabic composition.
                    item['focus_duration_ms'] = selected[fi]['endMs']-selected[fi]['startMs']
                    item['unstressed_duration_ms'] = selected[ui]['endMs']-selected[ui]['startMs']
                comparisons.append(item)
                notices.extend(item['flags'])
        return comparisons, list(dict.fromkeys(notices))

    words = sorted(words, key=lambda w: (w['startMs'], w['endMs']))
    for index, segment in enumerate(segments):
        start, end = segment['start_seconds'], segment['end_seconds']
        selected = [w for w in words if start <= (w['startMs']+w['endMs'])/2000 < end]
        if not selected:
            results.append({'id':segment['id'],'flags':['missing_word_alignment']})
            continue
        last = selected[-1]
        last_start, last_end = last['startMs']/1000, last['endMs']/1000
        terminal = measure(last_start, last_end)
        preceding = measure(max(start,last_start-.8),last_start-.02)
        intent = segment.get('prosody',{})
        expected = intent.get('ending','question' if segment.get('text','').rstrip().endswith('?') else 'neutral_fall')
        flags=[]
        metrics={}
        reliable = terminal is not None and preceding is not None
        if reliable and (terminal['octave_jump'] or preceding['octave_jump']):
            reliable=False
            flags.append('pitch_tracking_uncertain')
        if reliable:
            metrics = {
                'terminal_rise_st':round(12*np.log2(terminal['last_hz']/terminal['first_hz']),3),
                'terminal_vs_preceding_st':round(12*np.log2(terminal['median_hz']/preceding['median_hz']),3),
                'terminal_peak_vs_preceding_st':round(12*np.log2(terminal['p90_hz']/preceding['median_hz']),3),
                'terminal_level_difference_db':round(terminal['db']-preceding['db'],3),
                'terminal_duration_ms':round((last_end-last_start)*1000),
                'terminal_voiced_frames':terminal['voiced_frames'],
            }
            if expected == 'neutral_fall' and metrics['terminal_rise_st'] > 1.5:
                flags.append('possible_continuation_ending')
            # Multiple cues, plus an explicit editorial intent, before flagging stress.
            if intent.get('deemphasize_last',False) and (
                metrics['terminal_peak_vs_preceding_st'] > 3 or
                (metrics['terminal_vs_preceding_st'] > 1.2 and metrics['terminal_level_difference_db'] > 2)):
                flags.append('possible_unwanted_final_prominence')
        elif not terminal or not preceding:
            flags.append('insufficient_voiced_pitch_evidence')
        gap = None
        if index+1 < len(segments):
            nxt = segments[index+1]
            next_words=[w for w in words if nxt['start_seconds'] <= (w['startMs']+w['endMs'])/2000 < nxt['end_seconds']]
            if next_words:
                gap=(next_words[0]['startMs']-last['endMs'])/1000
                # Natural pacing is the default. Only flag a gap when the
                # editor has explicitly requested a minimum for this sentence.
                if 'minimum_pause_seconds' in intent and gap < intent['minimum_pause_seconds']:
                    flags.append('short_sentence_gap')
        comparisons, focus_flags = compare_focus(intent, selected)
        flags.extend(focus_flags)
        elapsed=max(.1,last_end-selected[0]['startMs']/1000)
        results.append({'id':segment['id'],'text':segment.get('text'), 'ending':last['text'].strip(),
                        'expected':expected,'reliable_pitch':reliable,'metrics':metrics,
                        'focus_comparisons':comparisons,
                        'word_profiles':[word_profile(w) for w in selected],
                        'gap_to_next_seconds':None if gap is None else round(gap,3),
                        'words_per_minute_including_internal_pauses':round(len(selected)/elapsed*60),
                        'flags':flags})
    return {'method':'Praat autocorrelation; relative F0 and voiced RMS, editorial sentence/focus intent and approximate word alignment',
            'thresholds':'Unvalidated triage heuristics: terminal rise >1.5 st; explicit final de-emphasis plus peak >3 st, or median >1.2 st and level >2 dB. A focus mismatch candidate needs both median >1.2 st and level >2 dB on an explicitly unmarked word, stable under +/-60 ms alignment probes. Probe spans >2 st or >3 dB are treated as alignment-sensitive. Gap thresholds are opt-in only.',
            'limitation':'Flags are review candidates, not diagnoses. No clear pitch/level conflict does not establish correct emphasis, pronunciation or naturalness. Raw duration differs with phonemes, syllables and phrase position and is not scored. Pitch, energy, duration, spectral cues and meaning contribute; alignment, octave errors and accent can mislead. The alignment probes do not establish correct boundaries. Never use this report as an audio edit decision list.',
            'sentences':results}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--audio',type=Path,required=True)
    p.add_argument('--captions',type=Path,required=True)
    p.add_argument('--segments',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--praat-dir',type=Path)
    p.add_argument('--pitch-floor',type=float,default=60)
    p.add_argument('--pitch-ceiling',type=float,default=350)
    args=p.parse_args()
    if args.praat_dir:
        sys.path.insert(0,str(args.praat_dir.resolve()))
    if args.output.exists():
        raise FileExistsError('Keep the previous report; choose a new output path.')
    data,rate=sf.read(args.audio)
    if data.ndim>1:
        data=data.mean(axis=1)
    assert np.isfinite(data).all()
    segments=json.loads(args.segments.read_text(encoding='utf-8-sig'))
    if isinstance(segments,dict):
        segments=segments.get('segments',segments.get('scenes'))
    words=json.loads(args.captions.read_text(encoding='utf-8-sig'))
    report=analyse(data,rate,words,segments,args.pitch_floor,args.pitch_ceiling)
    report.update(audio_sha256=hashlib.sha256(args.audio.read_bytes()).hexdigest(),
                  peak=float(np.max(np.abs(data))),sample_rate=rate)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'sentences':len(report['sentences']), 'flags':[{'id':s['id'],'flags':s['flags']} for s in report['sentences'] if s['flags']], 'report':str(args.output)},indent=2))

if __name__=='__main__':
    main()
