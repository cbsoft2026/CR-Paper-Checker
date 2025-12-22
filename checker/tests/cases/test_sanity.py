"""
Basic sanity checks on testing infra.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from src.parsed_paper import ParsedPaper

def test_infra_works():
    assert True
