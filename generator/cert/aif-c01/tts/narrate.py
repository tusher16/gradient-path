"""Record the reels narration with Kokoro-82M (Apache 2.0, runs on CPU).

Reads tts/script.json (written by `node generator/cert/aif-c01/build.js`) and writes one
MP3 per segment to audio/aif-c01/, named <topic>-<n>-<hash>.mp3. Files that already exist
are skipped, and files no longer in the script are deleted, so re-running after a caption
edit records only what changed. Run build.js again afterwards so the page picks them up.

  generator/cert/aif-c01/tts/.venv/bin/python generator/cert/aif-c01/tts/narrate.py [--force]

Setup, once (the venv is git-ignored):
  brew install espeak-ng
  uv venv --python 3.12 generator/cert/aif-c01/tts/.venv
  uv pip install --python generator/cert/aif-c01/tts/.venv/bin/python kokoro soundfile
  # Kokoro's English front end needs spaCy's small model; a uv venv has no pip, so install it directly
  uv pip install --python generator/cert/aif-c01/tts/.venv/bin/python \
    "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl"
"""
import json
import pathlib
import re
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]   # tts -> aif-c01 -> cert -> generator -> repo root
OUT = ROOT / 'audio' / 'aif-c01'
RATE = 24000          # Kokoro's native sample rate
SPEED = 1.0

# Spoken forms only; the page text is untouched. Kokoro spells out all-caps words, which is
# right for AWS, IAM or PII but wrong for the ones people say as words.
SAY = [
    (r'≠', ' is not '), (r'→', ' to '), (r'·', ', '), (r'\+1\b', 'plus one'),
    (r'\s⊃\s', ' contains '), (r'\s=\s', ', '), (r'\s\+\s', ' plus '),   # hook shorthand
    (r'\b(\d+)/(\d+)\b', r'\1 out of \2'), (r'\b1 GB\b', 'one gigabyte'), (r'\bms\b', 'milliseconds'),
    (r'\be\.g\.', 'for example'), (r'\bBERTScore\b', 'bert score'), (r'\bROUGE\b', 'rouge'),
    (r'\bBLEU\b', 'blue'), (r'\bRAG\b', 'rag'), (r'\bSaaS\b', 'sass'), (r'\bGenAI\b', 'Gen AI'),
    (r'\bAIF-C01\b', 'A I F, C zero one'), (r'\bKiro\b', 'Keero'),
    (r'([a-z])([A-Z])', r'\1 \2'),   # SageMaker -> Sage Maker, CloudTrail -> Cloud Trail
]


def spoken(text):
    for pat, rep in SAY:
        text = re.sub(pat, rep, text)
    return re.sub(r'\s+', ' ', text).strip()


def main():
    force = '--force' in sys.argv
    script = json.loads((HERE / 'script.json').read_text())
    voice, segs = script['voice'], script['segments']
    OUT.mkdir(parents=True, exist_ok=True)
    wanted = {s['file'] for s in segs}
    for old in OUT.glob('*.mp3'):
        if old.name not in wanted:
            old.unlink()
            print('removed stale', old.name)
    todo = [s for s in segs if force or not (OUT / s['file']).exists()]
    print(f'{len(segs)} segments, {len(todo)} to record with {voice}')
    if not todo:
        return
    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline
    pipe = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')   # 'a' = American English
    total = 0.0
    with tempfile.TemporaryDirectory() as tmp:
        for n, s in enumerate(todo, 1):
            chunks = [a for _, _, a in pipe(spoken(s['text']), voice=voice, speed=SPEED)]
            audio = np.concatenate(chunks)
            wav = pathlib.Path(tmp) / 'seg.wav'
            sf.write(wav, audio, RATE)
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(wav), '-ac', '1', '-ar', str(RATE),
                            '-codec:a', 'libmp3lame', '-b:a', '48k', str(OUT / s['file'])], check=True)
            secs = len(audio) / RATE
            total += secs
            print(f'[{n}/{len(todo)}] {secs:5.1f}s  {s["file"]}')
    print(f'recorded {total / 60:.1f} min of audio')


if __name__ == '__main__':
    main()
