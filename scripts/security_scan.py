"""Review candidate files only. Do not print matched credentials or raw lines."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
SKIP={'.git','.venv','.tools','.local','node_modules','__pycache__','.pytest_cache'}
PATTERNS={
 'github_token':r'gh[pousr]_[A-Za-z0-9]{25,}',
 'provider_key':r'sk-(?:proj-)?[A-Za-z0-9_-]{25,}',
 'private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
 'jwt':r'eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}',
 'credential_url':r'https?://[^\s/@:]+:[^\s/@]+@',
 'private_user_path':r'[A-Z]:[\\/]Users[\\/][A-Za-z0-9_~-]+[\\/]',
}

def files_for_release():
    paths=[]
    for p in ROOT.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(ROOT)
        if any(v in SKIP or v.endswith('.egg-info') for v in rel.parts):continue
        if rel.parts[0] in {'data','results'} and rel.as_posix() not in {'data/README.md','results/README.md'}:continue
        paths.append(p)
    return sorted(paths)

def scan(paths):
    findings=[]
    for path in paths:
        rel=path.relative_to(ROOT).as_posix()
        if path.name.startswith('.env') or path.suffix.lower() in {'.pem','.key','.pt','.pth','.zip','.h5','.hdf5','.mat','.ipynb','.log'}:
            findings.append(dict(file=rel,type='disallowed-file'));continue
        if path.stat().st_size>2_000_000:findings.append(dict(file=rel,type='large-file'))
        if path.suffix.lower() in {'.png','.pdf'}:continue
        text=path.read_text(encoding='utf-8',errors='replace')
        for name,pattern in PATTERNS.items():
            for m in re.finditer(pattern,text):findings.append(dict(file=rel,type=name,line=text[:m.start()].count('\n')+1))
    return findings

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--staged',action='store_true');args=ap.parse_args()
    if args.staged:
        r=subprocess.run(['git','-c',f'safe.directory={ROOT.as_posix()}','diff','--cached','--name-only','-z'],cwd=ROOT,capture_output=True,check=True)
        paths=[ROOT/p.decode() for p in r.stdout.split(b'\0') if p]
    else:paths=files_for_release()
    findings=scan(paths)
    result=dict(passed=not findings,file_count=len(paths),bytes=sum(p.stat().st_size for p in paths),
        findings=findings,scope='Candidate release files only; raw data/weights/environments/history excluded.',
        limitations='Pattern scan is not a proof of absence. No old Git history is imported or asserted credential-free.')
    (ROOT/'.local').mkdir(exist_ok=True)
    (ROOT/'.local/security-scan.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
    sys.exit(0 if result['passed'] else 1)

if __name__=='__main__':main()
