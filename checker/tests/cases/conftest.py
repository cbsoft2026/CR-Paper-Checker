import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).absolute().parent.parent.parent))

from src.acmlike.acmlike_checker import ACMLikeChecker

@pytest.fixture()
def acm_checker():
    """
    Returns the default acm_like_checker
    """
    return ACMLikeChecker("sbes_26_rt")
