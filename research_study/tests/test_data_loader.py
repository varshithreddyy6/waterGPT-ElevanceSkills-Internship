import json
from pathlib import Path
import pytest
from src.data_loader import load_jsonl,load_qrels

def test_jsonl_duplicate_rejected(tmp_path):
 p=tmp_path/'x.jsonl';p.write_text('{"_id":"a"}\n{"_id":"a"}\n')
 with pytest.raises(ValueError):load_jsonl(p)

def test_qrels_ids(tmp_path):
 p=tmp_path/'q.tsv';p.write_text('query-id\tcorpus-id\tscore\nq1\td1\t1\n')
 assert load_qrels(p)=={'q1':{'d1':1}}
