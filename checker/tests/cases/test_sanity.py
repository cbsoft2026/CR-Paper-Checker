import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).absolute().parent.parent))

from src.main import main

def test_infra_works():
    assert True
