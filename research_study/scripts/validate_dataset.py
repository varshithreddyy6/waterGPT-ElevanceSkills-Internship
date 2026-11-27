#!/usr/bin/env python3
"""Validate required SciFact records and write integrity metadata."""
import argparse,json,logging
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from src.data_loader import validate_dataset

def main():
 p=argparse.ArgumentParser(); p.add_argument('--data-dir',type=Path,default=Path(__file__).resolve().parents[1]/'data/raw'); a=p.parse_args(); logging.basicConfig(level=logging.INFO)
 out=Path(__file__).resolve().parents[1]/'results/metadata/dataset.json'; m=validate_dataset(a.data_dir,out); print(json.dumps(m,indent=2))
if __name__=='__main__':main()
