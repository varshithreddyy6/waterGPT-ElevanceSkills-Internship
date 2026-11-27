#!/usr/bin/env python3
"""Download the official BEIR SciFact archive; verified GitHub mirror fallback."""
from __future__ import annotations
import argparse, hashlib, logging, zipfile
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in __import__('sys').path: __import__('sys').path.insert(0,str(ROOT))
from src.data_loader import validate_dataset
URL='https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/scifact.zip'
MIRROR='https://github.com/liyongkang123/extended_beir_datasets/releases/download/beir_v1.0/scifact.zip'
# Original BEIR archive MD5 published in the BEIR dataset listing. SHA-256 is also recorded locally.
EXPECTED_MD5='5f7d1de60b170fc8027bb7898e2efca1'

def file_hash(path,algorithm='sha256'):
 h=hashlib.new(algorithm)
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def download(url,path):
 with requests.get(url,stream=True,timeout=(30,180)) as response:
  response.raise_for_status()
  with path.open('wb') as out:
   for chunk in response.iter_content(1024*1024):
    if chunk:out.write(chunk)

def main():
 p=argparse.ArgumentParser();p.add_argument('--raw-dir',type=Path,default=ROOT/'data/raw');p.add_argument('--force',action='store_true');a=p.parse_args()
 logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s');a.raw_dir.mkdir(parents=True,exist_ok=True);archive=a.raw_dir/'scifact.zip'
 if not a.force and archive.exists() and file_hash(archive,'md5')==EXPECTED_MD5:
  logging.info('Using previously downloaded archive with expected BEIR MD5.')
 else:
  last_error=None
  for url in (URL,MIRROR):
   try:
    logging.info('Downloading %s',url);download(url,archive)
    md5=file_hash(archive,'md5')
    if md5!=EXPECTED_MD5:raise ValueError(f'Archive MD5 mismatch: expected {EXPECTED_MD5}, got {md5}')
    logging.info('Verified official BEIR archive MD5: %s; SHA-256: %s',md5,file_hash(archive));break
   except Exception as exc:
    last_error=exc;logging.warning('Download source failed: %s',exc)
    archive.unlink(missing_ok=True)
  else:raise RuntimeError('Could not retrieve verified SciFact archive from official host or fallback mirror') from last_error
  root=a.raw_dir.resolve()
  with zipfile.ZipFile(archive) as z:
   for info in z.infolist():
    target=(root/info.filename).resolve()
    if root not in target.parents and target!=root:raise ValueError('Unsafe archive member')
   z.extractall(root)
 metadata=validate_dataset(a.raw_dir,ROOT/'results/metadata/dataset.json');metadata['archive']={'filename':'scifact.zip','md5':file_hash(archive,'md5'),'sha256':file_hash(archive),'retrieval_source':'official BEIR host when available; otherwise checksum-verified mirror of original archive'}
 (ROOT/'results/metadata/dataset.json').write_text(__import__('json').dumps(metadata,indent=2)+'\n',encoding='utf-8')
 print(f"Validated official BEIR SciFact archive: {metadata['counts']}; archive/file checksums recorded.")
if __name__=='__main__':main()
