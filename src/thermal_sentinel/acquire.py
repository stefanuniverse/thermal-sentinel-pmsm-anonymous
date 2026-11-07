"""Acquire the separately licensed dataset; never embed it in a Git commit."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import urllib.request
import zipfile
from .data import ROOT

URL='https://www.kaggle.com/api/v1/datasets/download/wkirgsn/electric-motor-temperature?datasetVersionNumber=3'
ZIP_SHA256='10e49e6220fa3c8a9d22c8bab8280ffe2d5e1e3380a6a18bcfc64ea2e8b56b92'
CSV_SHA256='78f3d150f0f2ad9c5dc7ff24dd12c00d386ad530f48c1589ad24fcd88867d3ad'

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def verify(path):
    if sha256(path)!=ZIP_SHA256:
        raise ValueError('Dataset version/hash mismatch; do not train on unverified data.')
    h=hashlib.sha256()
    with zipfile.ZipFile(path) as z:
        if z.namelist()!=['measures_v2.csv']:
            raise ValueError('Unexpected archive layout')
        with z.open('measures_v2.csv') as f:
            for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    if h.hexdigest()!=CSV_SHA256:
        raise ValueError('CSV checksum mismatch')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,help='Reuse an already downloaded official v3 ZIP after both hash checks')
    ap.add_argument('--download',action='store_true',help='Download official Kaggle v3; may require manual Kaggle login')
    args=ap.parse_args()
    dest=ROOT/'data/kaggle-pmsm.zip'
    dest.parent.mkdir(exist_ok=True)
    if args.source:
        verify(args.source)
        if not dest.exists():shutil.copyfile(args.source,dest)
    elif args.download and not dest.exists():
        partial=dest.with_suffix('.download')
        try:
            with urllib.request.urlopen(URL,timeout=60) as r,partial.open('wb') as f:
                shutil.copyfileobj(r,f)
            verify(partial)
            partial.replace(dest)
        except Exception as exc:
            raise SystemExit('Official download failed; obtain v3 manually from Kaggle and use --source. No data substituted. '+type(exc).__name__)
    elif not dest.exists():
        raise SystemExit('Use --download or --source OFFICIAL_V3_ZIP; see docs/DATA.md.')
    verify(dest)
    metadata=dict(currentVersionNumber=3,licenseName='CC BY-SA 4.0',lastUpdated='2021-04-26',
        source='https://www.kaggle.com/datasets/wkirgsn/electric-motor-temperature')
    (ROOT/'data/kaggle-metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    print('Official v3 ZIP and CSV hashes matched. Raw data remain local and gitignored.')

if __name__=='__main__':main()
